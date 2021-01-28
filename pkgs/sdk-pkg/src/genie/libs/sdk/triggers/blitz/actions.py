import json
import time
import json
import logging
from datetime import datetime

# from genie
from genie.libs import sdk
from genie.utils.diff import Diff
from genie.ops.utils import get_ops_exclude
from genie.harness.standalone import run_genie_sdk

# from pyats
from pyats.easypy import runtime
from pyats.log.utils import banner
from pyats.utils.secret_strings import SecretString

from .maple import maple, maple_search
from .yangexec import run_netconf, run_gnmi, notify_wait
from .actions_helper import configure_handler, api_handler, learn_handler,\
                            parse_handler, execute_handler,_get_exclude,\
                            _condition_validator, rest_handler, bash_console_handler

log = logging.getLogger(__name__)


# decorator for pyATS Health Check
# result with data will be added to pyATS extra field
def add_result_as_extra(func):
    def wrapper(*args, **kwargs):
        # adding extra is done only when it's pyATS health
        if kwargs['self'].__class__.__name__ == 'Health':
            extra_action_result = {}

            section = kwargs['section']
            extra_action_result.setdefault('health_name', kwargs['name'])
            extra_action_result.setdefault('action', func.__name__)

            extra_action_result.setdefault(
                'section',
                json.loads(json.dumps(section.uid, default=lambda a: str(a))))
            extra_action_result.setdefault(
                'section_parent',
                json.loads(
                    json.dumps(section.parent.uid, default=lambda a: str(a))))
            extra_action_result.setdefault('job', runtime.job.uid)
            # action start time
            action_start = datetime.now()

            # execute action for Health class
            action_output = func(*args, **kwargs)

            # action stop time
            action_stop = datetime.now()
            # calculate delta (action_stop - action_start)
            action_runtime = str(action_stop - action_start)
            # date format change
            action_start = action_start.isoformat()
            action_stop = action_stop.isoformat()

            extra_action_result.setdefault('starttime', action_start)
            extra_action_result.setdefault('stoptime', action_stop)
            extra_action_result.setdefault('runtime', action_runtime)
            extra_action_result.setdefault('steps_result',
                                           kwargs['steps'].result.name)

            # encode any action to protect contents such as password
            if 'reply' in kwargs:
                for reply in kwargs['reply']:
                    for key, value in reply.items():
                        if key == 'action':
                            reply['action'] = '%ENC{{{action}}}'.format(
                                action=SecretString.from_plaintext(value).data)

            # added `data` and `output` to ret_dict
            extra_action_result.setdefault(
                'kwargs',
                json.loads(json.dumps(kwargs, default=lambda a: str(a))))
            extra_action_result.setdefault('output', action_output)

            # add extra to testsuite
            extra_args = {
                'pyats_health_{action_start}'.format(action_start=action_start):
                extra_action_result
            }

            # add extra to processor
            section.reporter.client.add_extra(**extra_args)

            log.debug('extra:\n' +
                      json.dumps(extra_args, indent=2, sort_keys=True))
        else:
            # execute action for Blitz class
            action_output = func(*args, **kwargs)

        return action_output

    return wrapper

@add_result_as_extra
def configure(self,
              device,
              steps,
              section,
              name,
              command,
              alias=None,
              expected_failure=False,
              continue_=True,
              processor='',
              health_uids=None,
              health_groups=None,
              health_sections=None,
              **kwargs):

    # default output set to none in case of an exception
    output = None
    with steps.start("Configuring '{device}'".\
                    format(device=device.name), continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'command': command,
                       'expected_failure': expected_failure})

        output = configure_handler(**kwargs)

    notify_wait(steps, device)

    return output

@add_result_as_extra
def configure_dual(self,
                   device,
                   steps,
                   section,
                   name,
                   command,
                   alias=None,
                   expected_failure=False,
                   continue_=True,
                   processor='',
                   health_uids=None,
                   health_groups=None,
                   health_sections=None,
                   **kwargs):

    # default output set to none in case of an exception
    output = None
    with steps.start("Configuring '{device}' in (config-dual-stage) prompt".\
                    format(device=device.name), continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'command': command,
                       'action': 'configure_dual',
                       'expected_failure': expected_failure})

        output = configure_handler(**kwargs)

    notify_wait(steps, device)

    return output

@add_result_as_extra
def parse(self,
          device,
          steps,
          section,
          name,
          command,
          expected_failure=False,
          alias=None,
          include=None,
          exclude=None,
          max_time=None,
          check_interval=None,
          continue_=True,
          processor='',
          health_uids=None,
          health_groups=None,
          health_sections=None,
          *args,
          **kwargs):

    # action parse
    output = {}
    with steps.start("Parsing '{c}' on '{d}'".\
                    format(c=command, d=device.name), continue_=continue_) as step:

        arguments = kwargs.get('arguments', None)
        handler_kwargs = {'step': step,
                          'device': device,
                          'command': command,
                          'include': include,
                          'exclude': exclude,
                          'max_time': max_time,
                          'check_interval': check_interval,
                          'continue_': continue_,
                          'expected_failure': expected_failure,
                          'arguments': arguments}

        output = parse_handler(**handler_kwargs)

    notify_wait(steps, device)

    return output


@add_result_as_extra
def execute(self,
            device,
            steps,
            section,
            name,
            command,
            expected_failure=False,
            alias=None,
            include=None,
            exclude=None,
            max_time=None,
            check_interval=None,
            continue_=True,
            processor='',
            health_uids=None,
            health_groups=None,
            health_sections=None,
            **kwargs):

    # action execute
    output = None
    with steps.start("Executing '{c}' on '{d}'".\
                    format(c=command, d=device.name), continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'command': command,
                       'include': include,
                       'exclude': exclude,
                       'max_time': max_time,
                       'check_interval': check_interval,
                       'continue_': continue_,
                       'expected_failure': expected_failure})

        output = execute_handler(**kwargs)

    notify_wait(steps, device)

    return output


@add_result_as_extra
def api(self,
        steps,
        section,
        name,
        function,
        device=None,
        expected_failure=False,
        arguments=None,
        include=None,
        exclude=None,
        max_time=None,
        check_interval=None,
        continue_=True,
        processor='',
        health_uids=None,
        health_groups=None,
        health_sections=None,
        alias=None,
        **kwargs):

    # action api
    output = None

    if not device:
        msg = "Calling API {f}".format(f=function)
    else:
        msg = "Calling API '{f}' on '{d}'".format(f=function, d=device.name)

    with steps.start(msg, continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'command': function,
                       'include': include,
                       'exclude': exclude,
                       'max_time': max_time,
                       'check_interval': check_interval,
                       'continue_': continue_,
                       'arguments': arguments,
                       'expected_failure': expected_failure,
                       'blitz_obj': self})

        output = api_handler(**kwargs)

    notify_wait(steps, device)

    log.debug('api return value: {o}'.format(o=output))
    return output

@add_result_as_extra
def learn(self,
          device,
          steps,
          section,
          name,
          feature,
          alias=None,
          include=None,
          exclude=None,
          max_time=None,
          check_interval=None,
          expected_failure=False,
          continue_=True,
          processor='',
          health_uids=None,
          health_groups=None,
          health_sections=None):

    # action learn
    output = None
    with steps.start("Learning '{f}' on '{d}'".\
                    format(f=feature, d=device.name), continue_=continue_) as step:

        kwargs = {'step': step,
                  'device': device,
                  'command': feature,
                  'include': include,
                  'exclude': exclude,
                  'max_time': max_time,
                  'check_interval': check_interval,
                  'continue_': continue_,
                  'expected_failure': expected_failure}

        output = learn_handler(**kwargs)

    return output

@add_result_as_extra
def compare(self,
            steps,
            section,
            name,
            items,
            continue_=True,
            alias=None,
            processor='',
            health_uids=None,
            health_groups=None,
            health_sections=None):

    # action compare
    if not items:

        steps.failed('No item is provided for comparision')

    for comp_item in items:
        with steps.start("Verifying the following comparison request {}"\
                        .format(comp_item), continue_=continue_) as step:

            condition = _condition_validator(comp_item)
            result = 'passed' if condition else 'failed'
            getattr(step, result)('The following arithmetic statement {} is {}'.
                                   format(comp_item,condition))

@add_result_as_extra
def sleep(self,
          steps,
          section,
          name,
          sleep_time,
          continue_=True,
          processor='',
          health_uids=None,
          health_groups=None,
          health_sections=None,
          *args,
          **kwargs):

    log.info('Sleeping for {s} seconds'.format(s=sleep_time))
    time.sleep(float(sleep_time))

@add_result_as_extra
def rest(self,
         device,
         method,
         steps,
         section,
         name,
         expected_failure=False,
         continue_=True,
         include=None,
         exclude=None,
         max_time=None,
         check_interval=None,
         connection_alias='rest',
         processor='',
         health_uids=None,
         health_groups=None,
         health_sections=None,
         *args,
         **kwargs):

    # action rest
    output = None
    with steps.start("Submitting a '{m}' call to a REST API on '{d}'".\
                    format(m=method, d=device.name), continue_=continue_) as step:

        kwargs.update({'device': device,
                       'method': method,
                       'step': step,
                       'expected_failure':expected_failure,
                       'continue_':continue_,
                       'include':include,
                       'exclude':exclude,
                       'max_time':max_time,
                       'check_interval':check_interval,
                       'connection_alias':connection_alias})

        output = rest_handler(**kwargs)

    return output

@add_result_as_extra
def yang(self,
         device,
         steps,
         section,
         name,
         protocol,
         datastore,
         content,
         operation,
         continue_=True,
         connection=None,
         returns=None,
         alias=None,
         processor='',
         health_uids=None,
         health_groups=None,
         health_sections=None,
         *args,
         **kwargs):

    if connection:
        device = getattr(device, connection)
        # Verify that we are connected
        # TODO
        # I think all our connection implementation (unicon, rest, yang)
        # should have an isconnected which does an action on the device, example show
        # clock for cli, to verify.  Right now, we don't have this, we have
        # connected but we all know its of no use.
    if returns is None:
        returns = {}
    if protocol == 'netconf':
        result = run_netconf(operation=operation,
                             device=device,
                             steps=steps,
                             datastore=datastore,
                             rpc_data=content,
                             returns=returns,
                             **kwargs)
    elif protocol == 'gnmi':
        result = run_gnmi(operation=operation,
                          device=device,
                          steps=steps,
                          datastore=datastore,
                          rpc_data=content,
                          returns=returns,
                          **kwargs)
    if not result:
        steps.failed('Yang action has failed')

    if operation != 'subscribe':
        notify_wait(steps, device)

    return result

@add_result_as_extra
def configure_replace(self,
                      device,
                      steps,
                      section,
                      name,
                      config,
                      continue_=True,
                      alias=None,
                      iteration=2,
                      interval=30,
                      processor='',
                      health_uids=None,
                      health_groups=None,
                      health_sections=None):
    restore = sdk.libs.abstracted_libs.restore.Restore(device=device)

    # lib.to_url is normally saved via restore.save_configuration()
    # but since we only want the os abstraction and we are providing
    # a config - Just set the to_url equal to the config path provided
    restore.lib.to_url = config

    restore.restore_configuration(
        device=device,
        abstract=None,
        method='config_replace',
        iteration=iteration,
        interval=interval,
        delete_after_restore=False,
    )


@add_result_as_extra
def save_config_snapshot(self,
                         device,
                         steps,
                         section,
                         name,
                         alias=None,
                         continue_=True,
                         processor='',
                         health_uids=None,
                         health_groups=None,
                         health_sections=None):
    # setup restore object for device
    if not hasattr(self, 'restore'):
        self.restore = {}
    if device not in self.restore:
        self.restore[device] = sdk.libs.abstracted_libs.restore.Restore(
            device=device)

    # Get default directory
    save_dir = getattr(self.parent, 'default_file_system')
    if not save_dir:
        self.parent.default_file_system = {}

    # learn default directory
    if device.name not in save_dir:
        self.parent.default_file_system.update({
            device.name: self.restore[device].abstract.sdk.libs.abstracted_libs.\
                subsection.get_default_dir(device=device)})

    self.restore[device].save_configuration(
        device=device,
        abstract=None,
        method='config_replace',
        default_dir=self.parent.default_file_system)

    # To keep track of snapshots (whether they are deleted or not)
    self.restore[device].snapshot_deleted = False

@add_result_as_extra
def restore_config_snapshot(self,
                            device,
                            steps,
                            section,
                            name,
                            continue_=True,
                            delete_snapshot=True,
                            alias=None,
                            processor='',
                            health_uids=None,
                            health_groups=None,
                            health_sections=None):

    if not hasattr(self, 'restore') or device not in self.restore:
        steps.errored("Must use action 'save_config_snapshot' first.\n\n")

    # If the snapshot file was deleted - error
    if self.restore[device].snapshot_deleted:
        steps.errored(
            "If you want to restore with the same snapshot "
            "multiple times then you must pass 'delete_snapshot=False' "
            "to previous uses of this action. Otherwise the "
            "snapshot will be deleted on the first usage.")

    try:
        self.restore[device].restore_configuration(
            device=device,
            abstract=None,
            method='config_replace',
            delete_after_restore=delete_snapshot)
    except Exception as e:
        steps.failed(str(e))

    # To keep track of snapshots (whether they are deleted or not)
    if delete_snapshot:
        self.restore[device].snapshot_deleted = True

@add_result_as_extra
def bash_console(self,
                 device,
                 steps,
                 section,
                 name,
                 commands,
                 expected_failure=False,
                 include=None,
                 exclude=None,
                 max_time=None,
                 check_interval=None,
                 continue_=True,
                 alias=None,
                 processor='',
                 health_uids=None,
                 health_groups=None,
                 health_sections=None,
                 **kwargs):

    # action bash_console
    output = None
    with steps.start("Executing bash commands on '{d}'".\
                    format(d=device.name), continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'commands': commands,
                       'include': include,
                       'exclude': exclude,
                       'max_time': max_time,
                       'check_interval': check_interval,
                       'continue_': continue_,
                       'expected_failure': expected_failure})

        output = bash_console_handler(**kwargs)

    return output

@add_result_as_extra
def genie_sdk(self,
              steps,
              section,
              name,
              continue_=True,
              processor='',
              health_uids=None,
              health_groups=None,
              health_sections=None,
              **kwargs):

    # This is to remove the uut dependency of genie standalone.
    # Since the device we are running the sdk on is in the
    # kwargs we just pass the first device found as the 'uut'
    uut = 'uut'
    for _, params in kwargs.items():
        uut = params.get('devices', ['uut'])[0]
        break

    sdks = list(kwargs.keys())
    run_genie_sdk(self, steps, sdks, uut=uut, parameters=kwargs)

@add_result_as_extra
def print_(self,
          steps,
          section,
          name,
          continue_=True,
          processor='',
          health_uids=None,
          health_groups=None,
          health_sections=None,
          *args,
          **kwargs):

    if 'steps' in kwargs:
        kwargs.pop('steps')

    for key, value in kwargs.items():
        if value.get('type') == 'banner':

            print_value = 'printing message: {k}\n{v}'.format(
                k=key, v=banner(str(value['value'])))
        else:
            print_value = 'The value of {k}: {v}'.format(k=key,
                                                         v=value['value'])

        log.info(print_value)


@add_result_as_extra
def diff(self,
         steps,
         section,
         name,
         device,
         pre,
         post,
         alias=None,
         continue_=True,
         fail_different=False,
         command=None,
         exclude=None,
         processor='',
         health_uids=None,
         health_groups=None,
         health_sections=None,
         feature=None,
         mode=None):

    with steps.start("Perform Diff for '{device}'".format(device=device.name),
                     continue_=continue_) as step:
        exclude_items = _get_exclude(command, device)
        # if feature is given, get exclude from the Ops
        if feature:
            try:
                exclude_items.extend(get_ops_exclude(feature, device))
            except LookupError:
                log.warning(
                    "No Ops for {feature} was found. Couldn't retrieve exclude list."
                    .format(feature=feature))
        # check given mode
        if mode and mode not in ['add', 'remove', 'modified']:
            log.warning(
                "Wrong mode '{mode}' was given. Ignored.".format(mode=mode))
        if exclude and isinstance(exclude, list):
            exclude_items.extend(exclude)
            log.debug('exclude: {exclude}'.format(exclude=exclude_items))

        try:
            diff = Diff(pre, post, exclude=exclude_items, mode=mode)
        except Exception as e:
            step.failed(str(e))

        diff.findDiff()
        # check content of diff
        if str(diff):
            log.info(diff)
            if fail_different:
                step.failed('{pre} and {post} are not '
                            'identical'.format(pre=pre, post=post))
        else:
            step.passed('{pre} and {post} are identical'.format(pre=pre,
                                                                post=post))

actions = {
    'configure': configure,
    'configure_dual': configure_dual,
    'parse': parse,
    'execute': execute,
    'api': api,
    'tgn': api,
    'sleep': sleep,
    'yang': yang,
    'learn': learn,
    'print': print_,
    'rest': rest,
    'configure_replace': configure_replace,
    'save_config_snapshot': save_config_snapshot,
    'restore_config_snapshot': restore_config_snapshot,
    'run_genie_sdk': genie_sdk,
    'maple': maple,
    'compare': compare,
    'maple_search': maple_search,
    'diff': diff,
    'bash_console': bash_console
}
