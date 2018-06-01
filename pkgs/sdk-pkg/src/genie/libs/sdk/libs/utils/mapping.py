import re
import copy
import logging
import itertools
import importlib
import functools
from operator import attrgetter
from collections import OrderedDict, defaultdict

from genie.utils.diff import Diff
from ats.utils.objects import find, R, Operator
from ats.aetest.utils import format_filter_exception

from genie.conf.base import Base as ConfBase
from genie.ops.base import Base as OpsBase
from genie.utils.timeout import Timeout

from genie.libs import ops
from genie.libs.sdk.libs.utils.triggeractions import Configure
from genie.libs.sdk.libs.utils.normalize import GroupKeys, _to_dict

from genie.abstract import Lookup

log = logging.getLogger(__name__)

# TODO: Better handling of Errors vs Failures


class Mapping(object):
    def __init__(self, config_info=None, verify_ops=None, requirements=None,
                 verify_conf=None, num_values=None,  **kwargs):
        self.config_info = config_info or {}
        self._verify_ops_dict = verify_ops or {}
        self.verify_conf = verify_conf or {}
        self.num_values = num_values or {}
        for key, value in kwargs.items():
            setattr(self, key, value)

        # if no requirement or requirements is an OrderedDict then use it
        if not requirements or isinstance(requirements, OrderedDict):
            self.requirements = requirements or {}
        # else sort by requirements
        else:
            ordereddict = OrderedDict()
            delayed_keys = []
            for k, v in requirements.items():
                # if there is requirement item needs to be populated, move it
                # to delayed list
                if self._should_populate(v.get('requirements', [])):
                    delayed_keys.append(k)
                    continue

                ordereddict[k] = v
            # add the content from delayed list
            for key in delayed_keys:
                ordereddict[key] = requirements.get(key, {})

            self.requirements = ordereddict

    def _learn_base(self, device, name, step, abstracted_base, is_ops, base,
            requirements, verify=False, verify_find=None, **kwargs):

        try:
            # Populate the kwargs
            kwargs.update(requirements.get('kwargs', {}))
            requirements_ = requirements.get('requirements', [])
            exclude = requirements.get('exclude', [])
            all_keys = requirements.get('all_keys', False)

            if requirements_:
                # Populate the keys into R object
                # Useful if want to learn from previously learnt requirements
                requirements_ = self._populate_path(requirements_, device,
                                                    keys=self.keys)

            # process ops requirements
            if is_ops:
                o = abstracted_base(device=device, **kwargs)
                learn_poll = {}

                if not verify:
                    if not verify_find:
                        verify_find = self._verify_find

                    # First time we learn, no need to loop
                    learn_poll['attempt'] = 1
                    learn_poll['sleep'] = 0
                    learn_poll['verify'] = verify_find
                    learn_poll['all_keys'] = all_keys
                    learn_poll['requirements'] = requirements_
                else:
                    learn_poll = {'timeout': self.timeout}
                    if not verify_find:
                        verify_find = self._verify_same
                    name = o.__class__ if hasattr(o, '__class__') else o
                    log.info("Learning '{n}' feature".format(n=name))

                    learn_poll['initial'] = self._ops_ret[base]
                    learn_poll['verify'] = verify_find
                    learn_poll['exclude'] = self._populate_exclude(exclude)

                    learn_poll.update(kwargs)

                    # skip the learning for verify
                    if base not in self._ops_ret:
                        return o

                # Learn and verify the ops
                o.learn_poll(**learn_poll)
                return o

            # process conf requirements
            else:
                # import conf module
                ## get conf class
                cls = abstracted_base
                if issubclass(cls, ConfBase):
                    if verify:
                        name = cls.__name__ if hasattr(cls, '__name__') else cls
                        log.info("Learning '{n}' feature".format(n=name))
                        # skip the learning for verify
                        if base not in self._conf_ret:
                            return

                    # learn conf with show running-config
                    o = cls.learn_config(device=device)
                    # convert from conf instance to dictionary
                    o = [_to_dict(item) for item in o]

                    if verify:
                        # sort both list
                        initial = sorted(self._conf_ret[base])[:1]
                        restore = sorted(o)[:1]
                        # compare lengh to begin with
                        len_initial = len(initial)
                        len_restore = len(restore)
                        if len_initial != len_restore:
                            raise Exception("Current ops is not equal "
                                            "to the initial Snapshot "
                                            "taken\n{} != {}".format(
                                              len_initial, len_restore))
                        # zip and verify whether they are the same
                        for before, after in zip(initial, restore):
                            # verify conf
                            self._verify_same(after, before, exclude)
                    else:
                        for item in o:
                            # verify requirements
                            self._verify_find(item, requirements_, all_keys)
                    return o[:1]
        except Exception as e:
            raise

    def learn_ops(self, device, abstract, steps, timeout, **kwargs):
        '''Learn Ops object and populate the keys'''

        # Holds Ops object
        self._ops_ret = {}
        # Holds Conf object
        self._conf_ret = {}

        # How the keys learnt - Those are the regex values
        self.keys = []
        # TODO: Remove this
        self.req_list_flag = {}

        self.timeout = timeout

        # Loop over each requirement
        all_requirements = []

        # store hardcode values if provided
        # pop out the provided_values to leave the ops path only
        provided_values = self.requirements.pop('provided_values') \
            if 'provided_values' in self.requirements else {}

        for base, requirements in self.requirements.items():
            name = base.split('.')[-1]

            # Instantiate the abstracted base object
            # Create attrgetter for abstract which would find the right base
            # object
            abstracted_base = attrgetter(base)(abstract)
            is_ops = issubclass(abstracted_base, OpsBase)
            type_ = 'Ops' if is_ops else 'Conf'

            with steps.start("Learning '{n}' {t}".format(n=name,
                                                         t=type_)) as step:

                # Modify requirements so everything is learn
                if 'requirements' in requirements:
                    req = requirements.copy()
                    del req['requirements']
                try:
                    o = self._learn_base(device, name, step, abstracted_base,
                                         is_ops, base, req)
                except StopIteration as e:
                    step.failed("Could not learn '{n}'".format(n=name),
                                from_exception=e)
                if o:
                    # process ops requirements
                    if is_ops:
                        self._ops_ret[base] = o
                    # process conf requirements
                    else:
                        self._conf_ret[base] = o

            with steps.start('Verifying requirements') as step:

                # print out the log to show which are the hardcode values
                if provided_values:
                    log.info('Updating the requirements with the information provided: {}'
                        .format(provided_values))

                reqs = requirements['requirements']

                if not any(isinstance(el, list) for el in reqs[0]):
                    reqs_list = [reqs]
                    self.req_list_flag[base] = False
                else:
                    reqs_list = reqs
                    self.req_list_flag[base] = True

                ret_reqs = []

                for reqs in reqs_list:
                    # Needed for [[ ]] requirements

                    if isinstance(reqs[0], list):
                        all_requirements.extend(reqs)
                    req_msg = '\n'.join([str(re) for re in reqs])
                    log.info("Requirements pattern to "
                             "verify:\n{r}\n\n".format(r=req_msg))

                    # To populate the path first with hardcode values
                    # to only store the attributes that contains the hardcoded values
                    reqs = self._populate_path(reqs, device, keys=[provided_values])

                    # Populate the keys into R object
                    # Useful if want to learn from previously learnt requirements
                    reqs = self._populate_path(reqs, device, keys=self.keys, device_only=True)

                    all_keys = requirements.get('all_keys', False)

                    # Check if the requirements is [Operator('info')]
                    # if so, it will check if the ops output is empty
                    # TODO - this particular case will be enhanced in find
                    expect_empty = False
                    for i in reqs:
                        if len(i) < 2:
                            attr = i[0] if isinstance(i[0], str) else i[0].value
                            if not hasattr(o, attr):
                                expect_empty = True
                                step.passed('The ops attribute {} is empty as expected'
                                    .format(attr))

                    rs = [R(requirement) for requirement in reqs]

                    if not isinstance(o, list):
                        o = [o]
                    for item in sorted(o)[:1]:
                        # exclude the managemnet interface from the selected
                        # interfaces
                        find_obj = self.exclude_management_interface(device,
                            requirements, item)
                        ret = find([find_obj], *rs, filter_=False, all_keys=all_keys)

                        if not ret:
                            # Requirements are not satisfied
                            err_msg = '\n'.join([str(re) for re in reqs])
                            step.skipped("Following requirements were not satisfied "
                                        "for '{n}':\n{e}".format(n=name, e=err_msg))

                        group_keys = GroupKeys.group_keys(
                                        reqs=reqs,
                                        ret_num={},
                                        source=ret,
                                        all_keys=all_keys)

                        temp_keys = []
                        for key in group_keys:
                            temp_keys.extend(GroupKeys.merge_all_keys(self.keys, [], key))
                        self.keys = temp_keys.copy()

        with steps.start('Merge requirements') as step:
            # update the self.keys with hardcode values for following needs
            if not self.keys:
                self.keys.append(provided_values)
            else:
                for item in self.keys:
                    item.update(provided_values)

            self.keys = GroupKeys.max_amount(self.keys, self.num_values)
            req = self._populate_path(all_requirements, device, keys=self.keys)

            if not req:
                step.skipped('Could not merge the requirements '
                             'together\n{k}'.format(k=self.keys))
            ret_reqs.extend(req)

            # Requirements were satisfied
            msg = '\n'.join([str(re) for re in ret_reqs])
            log.info("\n\nFound the following requirements:\n{e}".format(n=name, e=msg))

            # Search if any regex remaining.
            for item in ret_reqs:
                for elem in item:
                    # expect_empty useage reason:
                    # When requirements is [Operator('info')]
                    # the ops output is empty, the full path won't be populated
                    # it could contain ('(?P<'), in this case pass the step
                    # TODO - will remove expect_empty when find is enhanced
                    if isinstance(elem, str) and elem.startswith('(?P<') and not expect_empty:
                        step.skipped('Could not satisfy all requirement\n{k}'
                                         .format(k=self.keys))

        return self._ops_ret

    def verify_with_initial(self, device, abstract, steps,
                            **kwargs):
        '''Verify a snapshot with initial snapshot'''
        # For each ops object, take a new snapshot
        # And compare with initial one taken in learn_ops
        # Store the new ops object
        current_ops = {}

        # Get Timeout Object for recovery section
        if 'timeout_recovery' in kwargs and \
            kwargs['timeout_recovery'] and \
           'max_time' in kwargs['timeout_recovery'] and\
           'interval' in kwargs['timeout_recovery']:
            self.timeout = \
                      Timeout(max_time=kwargs['timeout_recovery']['max_time'],
                              interval=kwargs['timeout_recovery']['interval'])
        else:
            # use default value
            self.timeout = Timeout(max_time=180, interval=15)

        for base, requirements in self.requirements.items():

            name = base.split('.')[-1]
            with steps.start("Verifying '{n}' is back to original "
                             "state".format(n=name),
                             continue_=True) as step:
                # Create attrgetter for abstract which would find the right base
                # object
                abstracted_base = attrgetter(base)(abstract)
                is_ops = issubclass(abstracted_base, OpsBase)

                try:
                    o = self._learn_base(device, name, step, abstracted_base,
                                         is_ops, base, requirements,
                                         verify=True, **kwargs)
                except StopIteration as e:
                    step.failed("'{n}' is not back to original "
                                "state".format(n=name), from_exception=e)

                if o and is_ops:
                    current_ops[base] = o

                log.info('{n} is identical to the original '
                         'snapshot'.format(n=name))

        return current_ops

    def _verify_find(self, ops, requirements, missing=False, all_keys=False,
                     **kwargs):
        '''Verify the ops response to the requirements'''
        if not requirements:
            return
        rs = [R(requirement) for requirement in requirements]
        ret = find([ops], *rs, filter_=False, all_keys=all_keys)
        # If missing is True, then we expect it to be missing, aka ret empty
        if not ret and not missing:
            raise Exception("'{req}' does not exists in "
                            "'{o}'".format(req=requirements, o=ops))
        if ret and missing:
            # It should be missing
            raise Exception("'{req}' exists in "
                            "'{o}' and it should not "
                            "exists".format(req=requirements, o=ops))

    def _verify_finds(self, ops, requirements, missing=False, all_keys=False):
        '''Verify multiple requirements for ops'''
        for req in requirements:
            self._verify_find(ops, [req], missing, all_keys)

    def _verify_finds_ops(self, ops, requirements, missing=False, all_keys=False,
                          obj_mod=None, org_req=None):
        '''Verify multiple requirements for ops'''
        for req in requirements:
            self._verify_find(ops, [req], missing, all_keys)

        # Each requirement can produce many populate_reqs (Many vrfs
        # for example) so loop over them
        for populate_req in requirements:

            # Let's modify the ops value to be equal to the original
            # snapshot. This will allow for comparing the otherk keys
            if obj_mod in self._ops_ret:
                try:
                    self._modify_ops_snapshot(original=self._ops_ret[obj_mod],
                                              current=ops, path=populate_req)
                except Exception as e:
                    log.warning("No comparison will be done between "
                                "original snapshot and snapshot after "
                                "configuration\n{e}".format(e=str(e)))
                    return

        # Alright now compare
        if obj_mod in self._ops_ret:
            # add handle for modify_exclude and exclude
            exclude = self._populate_exclude(org_req['exclude'])

            diff = Diff(self._ops_ret[obj_mod], ops,
                        exclude=exclude + ['callables'])
            diff.findDiff()

            if str(diff):
                raise Exception("The output is not same with diff\n{}"
                                .format(str(diff)))

    def _verify_same(self, ops, initial, exclude, **kwargs):
        diff = Diff(initial, ops, exclude=exclude + ['callables'])
        diff.findDiff()
        if diff.diffs:
            raise Exception("Current ops is not equal to the initial Snapshot "
                            "taken\n{e}".format(e=str(diff)))

    def _populate_exclude(self, exclude):
        kwargs = defaultdict(list)

        for item in self.keys:
            for key, value in item.items():
                kwargs[key].append(value)

        modified_exclude = []
        for exc in exclude:
            if callable(exc):
                partial = functools.partial(exc, **kwargs)
                modified_exclude.append(partial)
            elif exc.startswith('(?P<'):
                exc_temp = self._populate_path([[exc]], '', self.keys)
                # Flatten the list
                modified_exclude.extend(itertools.chain(*exc_temp))
            else:
                modified_exclude.append(exc)

        return modified_exclude

    def learn_configure(self):
        '''Populate the mapping keys via Conf'''
        # TODO Same as learn_ops, will populate keys
        pass

    def verify_missing_ops(self, *args, **kwargs):
        '''Make sure some attributes are missing from ops object'''
        self.verify_ops(missing=True, *args, **kwargs)


    def verify_ops(self, device, abstract, steps, missing=False, **kwargs):
        '''Verify that the key with correct value is populated correctly and
        other values are equal to initial snapshot
        '''

        # Requirement to verify for a specific Ops object
        for obj, requirements in self._verify_ops_dict.items():
            name = obj.split('.')[-1]
            # reset the missing depending on settings from trigger mapping file
            # when attributes missing when doing triggers using the verify_ops
            # in this, users don't have to overwrite the subsection
            missing = missing if 'missing' not in requirements else requirements['missing']
            with steps.start("Verifying '{n}' state with {obj}"
                             .format(n=name, obj=obj)) as step:
                # Create attrgetter for abstract which would find the right obj
                # object
                abstracted_obj = attrgetter(obj)(abstract)

                # seperate callable path and list path
                reqs = {}
                reqs['list'] = []
                reqs['callable'] = []
                for item in requirements['requirements']:
                    if callable(item[0]):
                        reqs['callable'].append(item)
                    elif isinstance(item[0], str):
                        reqs['list'].append(item)

                # Instantiate the abstracted Ops object
                kwargs = self._populate_kwargs(device, requirements)
                reqs['list'] = self._populate_path(reqs['list'], device, self.keys)

                msg = '\n'.join([str(re) for re in reqs['list']])
                log.info("Verifying the following requirements "
                         "are {condition}\n{rs}".format(rs=msg,
                            condition='not presented' if missing else 'satisfied'))

                if not kwargs:
                    try:
                        if issubclass(abstracted_obj, OpsBase):
                            instantiated_object = abstracted_obj(device=device)
                            self._verify_ops(device, instantiated_object,
                                             reqs, missing, obj,
                                             requirements)
                        elif issubclass(abstracted_obj, ConfBase):
                            self._verify_conf_2(device, abstracted_obj, reqs,
                                                missing, obj, requirements)
                    except Exception as e:
                        step.failed('Issue verifying the states',
                            from_exception=e)
                else:
                    failures = []
                    for kwarg in kwargs:
                        try:
                            if issubclass(abstracted_obj, OpsBase):
                                instantiated_object = abstracted_obj(device=device, **kwargs)
                                self._verify_ops(device, instantiated_object,
                                                 reqs, missing, obj,
                                                 requirements)
                            elif issubclass(abstracted_obj, ConfBase):
                                self._verify_conf_2(device, abstracted_obj, reqs,
                                                    missing, obj, requirements)
                        except Exception as e:
                            failures.append([kwarg, e])

                    if failures:
                        failures_text = ''
                        for kwarg, e in failures:
                            text = format_filter_exception(\
                                       exc_type=type(e),
                                       exc_value=e,
                                       tb=e.__traceback__)
                            failures_text += '{n} - {k}:\n\n{t}\n\n'.\
                                             format(n=obj, k=kwargs, t=text)
                        step.failed('Issue verifying the states\n{f}'.\
                                    format(f=failures_text))

                log.info('{n} has been verified and is valid'
                            .format(n=name))

    def _verify_conf_2(self, device, verify_conf, reqs, missing, ops,
                       requirements):
        o = verify_conf.learn_config(device=device)

        # convert from conf instance to dictionary
        o = [_to_dict(item) for item in o]

        # Make sure that configured path is correctly configured
        try:
            self._verify_finds_ops(ops=o[0], requirements=reqs['list'],
                                   missing=missing, obj_mod=ops,
                                   org_req=requirements)
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception("Could not verify the configuration was "
                            "applied correctly as per the exception: "
                            "{e}".format(e=e))

    def _verify_ops(self, device, o, reqs, missing, ops, requirements):

        # verify the ops paths values
        try:
            o.learn_poll(verify=self._verify_finds_ops,
                         requirements=reqs['list'],
                         timeout=self.timeout,
                         missing=missing,
                         obj_mod=ops,
                         org_req=requirements)
            # add to self to provide access for parent 
            # that can get information from the learned ops object
            self.verify_ops_object = o
        except Exception as e:
            raise e

        # verify callable if requirements path
        # contains customized verify functions
        if reqs.get('callable', None):
            for item in reqs['callable']:
                try:
                    o.learn_poll(verify=item[0].func,
                                 timeout=self.timeout, **item[0].keywords)
                except Exception as e:
                    raise e

    def _modify_ops_snapshot(self, original, current, path):
        # First does path exists in original, except the value
        r = R(path[:-1] + ['(.*)'])
        ret = find([original], r, filter_=False)
        if not ret:
            raise Exception("'{p}' does not exists on original "
                            "snapshot".format(p=path))
        self._modify_value(current, path[:-1], ret[0][0])

    def _modify_value(self, snapshot, path, value):
        for p in path[:-1]:
            try:
                snapshot = snapshot[p]
            except (TypeError):
                snapshot = getattr(snapshot, p)
        if isinstance(snapshot, dict):
            snapshot[path[-1]] = value
        else:
            setattr(snapshot, path[-1], value)

    def _should_populate(self, requirements):
        '''Determine whether the requirement item needs to be updated'''
        for req in requirements:
            for path in req:
                if isinstance(path, str) and path.startswith('{'):
                    return True

    def _populate_path(self, path, device, keys, _cur_path=None, _first=True, device_only=False):
        '''Create the multiple paths out of the paths'''
        if not path:
            return path
        if _cur_path is None:
            _cur_path = []

        if device_only or not keys:
            # Just so it goes through the loop below
            keys = [None]

        paths = []
        for key in keys:
            for p in path:
                loc = []
                for item in p:
                    # Only do uut
                    if device_only:
                        if isinstance(item, Operator):
                            loc.append(item)
                            continue
                        # TODO: Make this..more unique
                        if callable(item):
                            item = item(self.keys)
                        if item == '{uut}' or\
                           hasattr(item, 'value') and item.value == '{uut}':
                            loc.append(device.name)
                        else:
                            loc.append(item)
                        continue

                    if not key:
                        if isinstance(item, Operator):
                            loc.append(item)
                            continue

                        if item == '{uut}' or\
                           (hasattr(item, 'value') and item.value == '{uut}'):
                            loc.append(device.name)
                        else:
                            loc.append(item)
                        continue

                    if isinstance(item, Operator):
                        if not isinstance(item.value, str):
                            loc.append(item.value)
                            continue
                        if item.value == '{uut}':
                            loc.append(device.name)
                            continue
                        if item.regex and item.value.startswith('(?P<'):
                            # Get the variable name
                            var = list(item.regex.groupindex)[0]
                            # Does var exists in key?
                            if var not in key:
                                # So key does not exists
                                # just keep doing with this as a value
                                loc.append(item.value)
                            else:
                                # This mean var is in key
                                vkeys = key[var]
                                if not item == str(vkeys):
                                    break
                                loc.append(vkeys)
                            continue
                        loc.append(item.value)
                        continue

                    # TODO: Make this..more unique
                    if callable(item):
                        item = item(self.keys)
                    if not isinstance(item, str):
                        loc.append(item)
                        continue
                    elif item == '{uut}':
                        loc.append(device.name)
                        continue
                    elif item.startswith('(?P<'):
                        # Modify it with an item of key
                        try:
                            com = re.compile(item)
                        except Exception as e:
                            raise ValueError("'{item}' is not a valid regex "
                                             "expression".format(item=item))\
                                             from e

                        # Get the variable name
                        var = list(com.groupindex)[0]
                        # Does var exists in key?
                        if var not in key:
                            # So key does not exists
                            # just keep doing with this as a value
                            loc.append(item)
                        else:
                            # This mean var is in key
                            vkeys = key[var]
                            if not com.match(str(vkeys)):
                                break
                            loc.append(vkeys)
                            continue
                    else:
                        loc.append(item)
                        continue
                else:
                    paths.append(loc)

        try:
            paths.sort()
        except Exception:
            # best effort to keep things consistent
            pass
        return list(k for k,_ in itertools.groupby(paths))

    def exclude_management_interface(self, device, requirements, ops_obj):
        '''Exclude the management interface from the trigger interfaces'''
        # exclude the managemnet interface from the interfaces
        # learned for the trigger action. Unless specified
        # by the user to include the management interafce
        # "user specifies include_management_interface as True"
        if 'include_management_interface' in requirements and \
            requirements['include_management_interface']:
            # management interface will be considered in the
            # trigger action
            return ops_obj
        else:
            Interface_ops_obj = Lookup.from_device(device).ops.interface.interface.Interface(device)
            new_dict = {}
            if isinstance(ops_obj, type(Interface_ops_obj)) and \
                device.management_interface:
                new_dict['info'] = {}
                for key in ops_obj.info.keys():
                    if device.management_interface != key:
                        new_dict['info'][key] = ops_obj.info[key]
            # management interface will be excluded from the trigger action
            if new_dict:
                return new_dict
            else:
                return ops_obj

    def _one_to_many_path(self, paths, device, many_keys, standard_keys):
        '''Create the one to many paths out of the paths'''
        if not paths:
            return paths
        ret = []
        for path in paths:
            temp_path=[]
            for item in path:
                # item is find.operator
                if isinstance(item, Operator):
                    if not isinstance(item.value, str):
                        temp_path = self._append_to_many(temp_path, item.value)
                        continue
                    if item.value == '{uut}':
                        temp_path = self._append_to_many(temp_path, device)
                        continue
                    if item.regex and item.value.startswith('(?P<'):
                        # Get the variable name
                        var = list(item.regex.groupindex)[0]
                        # Does var exists in key?
                        if var not in key:
                            # So key does not exists
                            # just keep doing with this as a value
                            temp_path = self._append_to_many(temp_path,
                                                             item.value)
                        else:
                            # This mean var is in key
                            vkeys = key[var]
                            if not item == str(vkeys):
                                break
                            temp_path = self._append_to_many(temp_path, vkeys)
                        continue
                    temp_path = self._append_to_many(temp_path, item.value)
                    continue
                if not isinstance(item, str):
                    temp_path = self._append_to_many(temp_path, item)
                    continue
                if item == '{uut}':
                    temp_path = self._append_to_many(temp_path, device)
                    continue
                if not item.startswith('(?P<'):
                    temp_path = self._append_to_many(temp_path, item)
                    continue
                # Modify it with an item of key
                try:
                    com = re.compile(item)
                except Exception as e:
                    raise ValueError("'{item}' is not a valid regex "
                                     "expression".format(item=item)) from e
                # Get the variable name
                var = list(com.groupindex)[0]
                if var in standard_keys:
                    # This mean var is in key
                    vkeys = standard_keys[var]
                    if not com.match(str(vkeys)):
                        break
                    temp_path = self._append_to_many(temp_path, vkeys)
                    continue

                # So key does not exists
                # just keep doing with this as a value
                if var not in many_keys:
                    temp_path=self._append_to_many(temp_path, item)
                    continue

                vkeys = [key for key in list(many_keys[var]) \
                                                         if com.match(str(key))]
                if not vkeys:
                    break
                temp_path=self._append_to_many(temp_path, vkeys, multiply=True)
            else:
                ret.extend(temp_path)
        return ret

    def _append_to_many(self, path, value, multiply=False):

        ret = path
        if not len(path) > 0 or not isinstance(path[0], list):
            ret = [ ret ]

        if multiply:
            ret = ret * len(value)
            ret = [ one + [v] for one, v in zip(ret, value) ]
        else:
            ret = [ one + [value] for one in ret ]

        return ret


    def unconfigure(self, *args, **kwargs):
        return self.configure(unconfig=True, *args, **kwargs)

    def _config(self, conf_obj, configures, device, name_,
                unconfig=False, one_to_many=None, standard_keys=None):
        paths = []
        if 'requirements' in configures:
            # Take the path and populate the keys if possible
            paths = self._path_population(configures['requirements'], device,
                                        one_to_many=one_to_many,
                                        standard_keys=standard_keys)

            config = '\n'.join([str(conf_path) for conf_path in paths])
            log.info('With following configuration:\n{c}'
                     .format(n=name_, c=config))

        Configure.conf_configure(device=device,
                                 conf=conf_obj,
                                 conf_structure=paths,
                                 unconfig=unconfig)

    def _populate_kwargs(self, device, configures):
        kwargs = []
        if 'kwargs' not in configures:
            return []
        if 'mandatory' not in configures['kwargs']:
            return configures['kwargs']

        # Populate the mandatory keys
        kwargs_wanted = []
        keys_wanted = []
        for key, path in configures['kwargs']['mandatory'].items():
            kwargs_wanted.append(path)
            keys_wanted.append(key)

        # Take the path and populate the keys if possible
        paths = self._path_population([kwargs_wanted], device)

        for path in paths:
            kwargs.append({k:v for k, v in zip(keys_wanted, path)})
        return kwargs

    def configure(self, device, abstract, steps, unconfig=False, verify=False,
                  **kwargs):

        # initial conf mandatory key dictionary
        self.conf_mandatory_key = {}

        for conf, configures in self.config_info.items():
            # Create attrgetter for abstract which would find the right conf
            # object
            abstracted_ops = attrgetter(conf)(abstract)
            # Instantiate the abstracted Ops object

            name = conf.split('.')[-1]
            if not unconfig:
                word = 'Configuring'
            else:
                word = 'Unconfiguring'
            with steps.start("{w} '{n}'".format(w=word, n=name)) as step:
                kwargs = self._populate_kwargs(device, configures)

                # We need to build the conf object after collecting all the
                # kwargs. Multiple kwargs can be passed as mandatory keys.
                self.conf_mandatory_key[conf] = kwargs
                if not kwargs:
                    self._configure(device, conf, abstracted_ops, configures,
                                    unconfig, name)
                else:
                    for kwarg in kwargs:
                        self._configure(device, conf, abstracted_ops, configures,
                                        unconfig, name, **kwarg)

    def _configure(self, device, conf, abstracted_ops, configures, unconfig, name_, **kwargs):
        self.conf_mandatory_key[conf] = kwargs
        if not kwargs:
            co = abstracted_ops(device=device)
        else:
            co = abstracted_ops(device=device, **kwargs)

        if 'requirements' in configures and\
            configures['requirements'] and\
            callable(configures['requirements'][0][0]):
            # Call this callable then
            configures['requirements'][0][0](device=device, conf_obj=co,
                                             configures=configures,
                                             unconfig=unconfig, self=self)
        else:
            self._config(device=device, conf_obj=co,
                         configures=configures,
                         name_=name_, unconfig=unconfig)


    def _path_population(self, paths, device,
                         one_to_many=None, standard_keys=None):
        '''Populate path either one_to_many or standard search and replace'''
        # TODO: I Think we can remove this is one to many is removed
        if not paths:
            return paths
        # apply one_to_many dictionary
        if one_to_many:
            return self._one_to_many_path(paths, device, one_to_many,
                                          standard_keys)
        # call the usual _populate_path
        paths = self._populate_path(paths, device, keys=self.keys)

        return paths

    def _verify_conf(self, conf, conf_paths, unconfig):
        '''Verify that the configuration was applied correctly'''
        # TODO: Enhancement needed for Unconfig
        # Lines are missing,
        err_msg = []
        # If unconfig, then, its valid for some path to not exists
        for conf_path in conf_paths:
            c = conf
            if isinstance(c, list):
                c = c[0]
            # Get to the right location
            for item in conf_path[:-2]:
                try:
                    c = getattr(c, item)
                except (TypeError, AttributeError):
                    c = c[item]

            # Verify the value
            # Not sure if getattr or getitem
            try:
                value = getattr(c, conf_path[-2])
            except AttributeError:
                value = c[conf_path[-2]]

            if value != conf_path[-1]:
                # Not the same!
                err_msg.append("'{c}' is not configured correctly.\n"
                               "Value expected: {e}\n"
                               "Value found: {f}".format(c=conf_path[:-1],
                                                         e=conf_path[-1],
                                                         f=value))
        if err_msg:
            raise ValueError('\n'.join(err_msg))


class FilterFindValue():
    ''' Filter the outputs from base output with some control R objects.'''

    @classmethod
    def find_value(self, ops, values, r, path, **kwargs):

        # get the values for group_keys
        for key in values:
            sub_key = list(values[key].keys())[0]
            if sub_key:
                values = values[key]
            else:
                values = {key: values[key][sub_key]}
        keys = []
        # find required info from ops obj
        for r_obj in r:
            ret = find([ops], r_obj, filter_=False)
            if not ret:
                # Could not find anything satisfying
                return {}

            ret = GroupKeys.group_keys(ret_num=values, source=ret,
                                       reqs=path)

            # To Modify to support more than 1 conf object
            key = {}
            for v in values:
                if v not in ret[0]:
                    raise Exception("'{v} could not be found in previously "
                                    "learnt keys".format(v=v))
                key[v] = ret[0][v]
            keys.append(key)
            # TODO: To modify for multiple conf object
            return keys
        return keys

    @classmethod
    def verify(self, r):
        '''For now hardcoded for learnpolldiff.ops_diff'''

        self.ops_obj.learn_poll(verify=LearnPollDiff.ops_diff,
                                sleep=sleep_time,
                                attempt=attempt,
                                exclude=self.exclude,
                                ops_modified=self.ops_Verify,
                                ops_compare=self.pre_snap)


class Different(object):
    def __init__(self, regex):
        regex = regex
        com = re.compile(regex)
        self.value = list(com.groupindex)[0]

    def __call__(self, keys):
        # Look for regex groupindex and build negative lookahead regex.
        list_values = []
        for key in keys:
            if self.value in key:
                list_values.append(key[self.value])
        regexes = '|'.join([str(i) for i in list_values])
        ret = '(?P<{name}>^(?!{regexes}$).*$)'.format(name='not_'+self.value,
                                                      regexes=regexes)
        return ret
