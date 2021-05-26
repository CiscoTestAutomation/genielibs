import re
import copy
import json
import logging

# pyATS
from pyats.easypy import runtime
from pyats.results import Passed, Passx, Errored
from pyats.aetest.steps import Steps

# Genie
from genie.utils import Dq
from genie.conf.utils.converter import Converter
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.parser.utils.common import format_output
from genie.libs.sdk.triggers.blitz.markup import _load_saved_variable

log = logging.getLogger(__name__)


class Health(Blitz):

    def _find_item_by_search_keyword(self, section, data, arg_name,
                                     search_keyword):
        """
        This function will be called when `health_sections`, `health_uids` or
        `health_groups` is given to pyats run command.
        Search `search_keyword` in item based on givin arg_name such as
        `health_sections`, `health_uids` and `health_groups` in search_keyword

        Arguments:
            section (`obj`) : Aetest Subsection object.
            data (`dict`) : data of section 
            arg_name (`str`) : one the way to narrow down such as 
                                    `health_sections`, `health_uids` or 
                                    `health_groups` 
            search_keyword (`str`) : keyword to search which supports regex

        Returns:
            data (`dict`) : item if search_keyword can be found in item
                            Otherwise, return empty dict
        """
        # arg health_sections given
        if arg_name == 'health_sections':
            if re.search(search_keyword, section.uid):
                return data
        # arg health_uids given
        elif arg_name == 'health_uids':
            if re.search(search_keyword, section.uid) or re.search(
                    search_keyword, section.parent.uid):
                return data
        # arg health_groups given
        elif arg_name == 'health_groups':
            # groups location is different depending on
            # where the section is in commonSetup/Cleanup or Testcase
            # check `section.groups` first, if not, check `section.parent.groups`
            try:
                for grp in section.groups:
                    if re.search(search_keyword, grp):
                        return data
            except AttributeError:
                for grp in section.parent.groups:
                    if re.search(search_keyword, grp):
                        return data
        return {}

    def _select_health(self, section, data, search_keywords, arg_name):
        """
        check if pyATS Health Check processor meets criteria 
        via `health_sections`, `health_uids` and `health_groups`

        Arguments:
            section (`obj`) : Aetest Subsection object.
            data (`dict`) : data of section
            search_keywords (`list`) :  list of search keywords
            arg_name (`str`) : `health_sections`, `health_uids` or 
                               `health_groups` 

        Returns:
            new_data (`list`) : Updated data which meets args criteria
                                Otherwise, return empty list
        """
        # initialize
        new_data = []
        search_target = ''

        # replicate search_keywords for further loop
        search_keywords = copy.deepcopy(search_keywords)

        for search_keyword in search_keywords:
            # save original `search_keyword` in `pre_search_keyword`
            # which has `%VARIABLES{}`
            pre_search_keyword = search_keyword
            # load `%VARIABLES{} and replace in `search_keyword`
            _, search_keyword = _load_saved_variable(self, section=section, val=search_keyword)
            # get search_target such as section.uid, section.groups from section
            search_target = self._find_search_target(section, arg_name,
                                                     search_keyword,
                                                     search_keywords)
            log.debug('search_target: {st}'.format(st=search_target))
            if re.search(search_keyword, search_target):
                # when args exist, don't need to do `contains` because
                # args will affect to all items in pyATS Health
                if getattr(runtime.args, arg_name):
                    dq_item = self._find_item_by_search_keyword(
                        section, data, arg_name, search_target)
                else:
                    # in `data`, %VARIABLES doesn't need to be converted
                    # so, need to use `pre_search_keyword`
                    data_dq = Dq(data)
                    dq_item = data_dq.contains(pre_search_keyword,
                                                regex=True,
                                                level=1).reconstruct()
                    # for the case regex is used. need to do exact match
                    # without `regex=True`
                    if not dq_item:
                        dq_item = data_dq.contains(pre_search_keyword,
                                                    level=1).reconstruct()
                if dq_item and dq_item not in new_data:
                    new_data.append(dq_item)

        log.debug("new_data: {}".format(new_data))
        return new_data

    def _get_actions(self, data):
        """
        get action items only from any Blitz sections such as parallel and loop

        Arguments:
            data   (`dict`) : data of section

        Returns:
            (`dict`): only actions from data

        """
        if data:
            if isinstance(data, list):
                # parallel
                if 'parallel' in data[0]:
                    return data[0]['parallel']
                # run_condition
                elif 'run_condition' in data[0]:
                    return data[0]['run_condition']['actions']
                # normal action
                else:
                    return data
            elif isinstance(data, dict):
                # loop
                if Dq(data).contains('actions'):
                    return Dq(data).get_values('actions')

        # for case section doesn't have loop/parallel
        # return data as is.
        return data

    def _get_device_names(self, data, each_data):
        """
        Check if %VARIABLES in device field and then resolve the device name

        Arguments:
            data        (`list`) : data of section
            each_data   (`dict`) : each of data element

        Returns:
            device_list (`list`): list of devices
        """
        device_list = []
        for device in Dq(each_data).get_values('device'):
            m = re.search('%VARIABLES{(?P<var_name>.*)}',
                          device.name if hasattr(device, 'name') else device)
            if m:
                var_name = m.groupdict()['var_name']
                if isinstance(data, dict) and 'loop_variable_name' in data and 'value' in data:
                    # loop with list
                    if var_name == data['loop_variable_name']:
                        for dev in data['value']:
                            if dev not in device_list:
                                device_list.append(dev)
                    # loop with dict for _keys/_values
                    elif (var_name == data['loop_variable_name'] +
                          '._keys') or (var_name
                                        == data['loop_variable_name'] +
                                        '._values'):
                        if data['value']:
                            for item in data['value']:
                                for dev in item.keys():
                                    if dev not in device_list:
                                        device_list.append(dev)
                else:
                    if Dq(each_data).contains('loop_variable_name') and Dq(each_data).contains('value'):
                        # loop with list
                        if var_name == Dq(each_data).get_values('loop_variable_name', 0):
                            loop_value = Dq(each_data).get_values('value', 0)
                            m = re.search('%VARIABLES{(?P<dev_var_name>.*)}', loop_value)
                            if m:
                                dev_var_name = m.groupdict()['dev_var_name']
                                # for testscript variables
                                if 'testscript.' in dev_var_name:
                                    dev_var_name = dev_var_name.split('testscript.')[-1]
                                    try:
                                        loop_value = self.parent.parameters['save_variable_name'].setdefault('testscript', {}).get(dev_var_name, [])
                                    # if no key yet, just put empty list as iterable
                                    except (KeyError, AttributeError):
                                        loop_value = []
                                # testcase variables
                                else:
                                    try:
                                        loop_value = self.parameters['save_variable_name'].get(dev_var_name, [])
                                    # if no key yet, just put empty list as iterable
                                    except KeyError:
                                        loop_value = []
                            for dev in loop_value:
                                if dev not in device_list:
                                    device_list.append(dev)
                        # loop with dict for _keys/_values
                        elif (var_name == Dq(each_data).get_values('loop_variable_name', 0) +
                              '._keys') or (var_name
                                            == Dq(each_data).get_values('loop_variable_name', 0) +
                                            '._values'):
                            if Dq(each_data).get_values('value', 0):
                                for item in Dq(each_data).get_values('value', 0):
                                    for dev in item.keys():
                                        if dev not in device_list:
                                            device_list.append(dev)
            else:
                if device not in device_list:
                    device_list.append(device)

        log.debug('device_list: {}'.format(device_list))
        return device_list

    def _check_all_devices_connected(self, testbed, data, reconnect):
        """
        find search target depending on arg_name (health_uids/health_groups/health_sections)
        for `health_groups`, this function get `groups` from the triggers.

        Arguments:
            testbed (`obj`) : testbed object
            data   (`dict`) : data of section
            reconnect (`dict` or None) : parameters for reconnect
                                         ex.)
                                         {
                                             'max_time': 900, # maximum time to reconnect
                                             'interval': 60,  # sleep before retry
                                         }
        
        Returns:
            dev_list (`list`): device list which is connected
        """
        dev_list = []
        device_checked = []
        for each_data in self._get_actions(data):
            for dev in self._get_device_names(data, each_data):
                if dev not in device_checked:
                    device_checked.append(dev)
                    # check if device object, or not
                    if hasattr(dev, 'name'):
                        dev = dev.name
                    dev_obj = testbed.devices[dev]
                    # check if device exists in testbed and if connected
                    if dev in testbed.devices and dev_obj.connected:
                        if reconnect is None:
                            state = dev_obj.api.verify_device_connection_state()
                        else:
                            state = dev_obj.api.verify_device_connection_state(
                                reconnect=True,
                                reconnect_max_time=reconnect.get('max_time', 900),
                                reconnect_interval=reconnect.get('interval', 60))
                        if state and dev not in dev_list:
                            dev_list.append(dev)
        return dev_list

    def _find_search_target(self, section, arg_name, search_keyword,
                            search_keywords):
        """
        find search target depending on arg_name (health_uids/health_groups/health_sections)
        for `health_groups`, this function get `groups` from the triggers.

        Arguments:
            section (`obj`) : Aetest Subsection object.
            arg_name (`str`) : `health_sections`, `health_uids` or 
                               `health_groups`
            search_keyword (`str`): a keyword to search
            search_keywords (`list`): list of search keywords
        
        Returns:
            search_target (`str`) : found search target depending on arg_name
        """
        # replicate search_keywords for further loop
        search_keywords = copy.deepcopy(search_keywords)

        search_target = ''
        if arg_name == 'health_groups':
            search_target = getattr(section, 'groups', '')
            if not search_target:
                search_target = getattr(section.parent, 'groups', '')
            # add string in case section.parent.groups is None
            # for later regex search
            if search_target is None:
                search_target = ''
            if isinstance(search_target, list):
                for st_item in search_target:
                    search_target = st_item if re.search(
                        search_keyword, st_item) else ''
                    log.debug("health_groups/search_target: {uid}".format(
                        uid=search_target))
        elif arg_name == 'health_sections':
            search_target = section.uid
            log.debug("health_sections/search_target: {uid}".format(
                uid=search_target))
        elif arg_name == 'health_uids':
            for kw in search_keywords:
                # load `%VARIABLES{} and replace`
                _, kw = _load_saved_variable(self, section=section, val=kw)
                if re.search(kw, section.uid):
                    search_target = section.uid.split('.')[0]
                    log.debug(
                        "health_uids/search_target(section.uid): {uid}".format(
                            uid=section.uid))
                elif re.search(kw, section.parent.uid):
                    search_target = section.parent.uid.split('.')[0]
                    log.debug(
                        "health_uids/search_target(section.parent.uid): {uid}".
                        format(uid=section.parent.uid))
        return search_target

    def _pre_post_processors(self,
                             testbed,
                             processor,
                             section,
                             data,
                             name,
                             devices_connected,
                             processor_targets,
                             processor_type,
                             pre_processor_result=Passed):
        """
        execute pre/post processors and return if pre-processor runs and processor result

        Arguments:
            testbed (`obj`): testbed object
            processor (`obj`): Aetest Processor object
            section (`obj`): Aetest Section object
            data (`list`) : data of section
            name (`str`) : name of section in health yaml
            devices_connected (`list`) : list of connected devices
            processor_targets (`list`) : list of `processor_flag which ones 
                                         will be run as pre/post processors
            processor_type (`str`) : processor type `pre` or `post`
            pre_processor_result (`ob`) : result object. Default to `Passed`

        Returns:
            pre_processor_run (`bool`) : if pre processor runs or not
            pre_processor_result (`obj`) : return processor result (Result obj)
        """
        new_data_dict = {}
        selected_options = 0
        list_of_args = []
        # flag if health args are given to pyats command
        args_flag = False
        # flag if health args are defined under action in health yaml
        args_in_yaml_flag = False
        log.debug(
            'data:\n{d}'.format(d=json.dumps(data, indent=2, sort_keys=True)))
        orig_data = copy.deepcopy(data)

        # check if health arguments are given to pyats command
        for arg_name in ['health_sections', 'health_uids', 'health_groups']:
            if getattr(runtime.args, arg_name):
                args_flag = True
            for item in self._get_actions(data):
                if Dq(item).contains(
                        'health_sections|health_uids|health_groups',
                        regex=True):
                    args_in_yaml_flag = True

        for arg_name in ['health_sections', 'health_uids', 'health_groups']:
            log.debug('Checking {an}'.format(an=arg_name))
            selected = None
            selected_options = 0
            for item in self._get_actions(data):
                # from argument

                arg_search_keyword = getattr(runtime.args, arg_name)
                if arg_search_keyword:
                    args_flag = True
                    selected = self._select_health(
                        section, item, arg_search_keyword.split(' '), arg_name)
                    selected_options += 1
                    list_of_args.append(arg_name)
                if selected:
                    new_data_dict.setdefault(arg_name, {}).setdefault(
                        selected_options, selected)

                if not args_flag:
                    # from datafile
                    search_keywords = []
                    search_keywords = getattr(
                        runtime.args,
                        arg_name) or Dq(item).get_values(arg_name)
                    if not isinstance(search_keywords, list):
                        search_keywords = [search_keywords]
                    if search_keywords == []:
                        # if args are given to one of actions, other actions
                        # will run to all sections by default. To do so,
                        # adding `.*` as search_keywords
                        # ex.)
                        # - api:               # only section1
                        #     function: func1
                        #     health_sections: section1
                        # - api:               # all sections
                        #     function: func2
                        if (args_in_yaml_flag and arg_name == 'health_sections'
                            ) and (not Dq(item).get_values('health_sections')
                                   and not Dq(item).get_values('health_uids')):
                            search_keywords = ['.*']
                        else:
                            search_keywords = None

                    log.debug(
                        "arg_name, search_keywords: {sel_name}, {sel}".format(
                            sel_name=arg_name, sel=search_keywords))
                    if search_keywords:
                        selected_options += 1
                        list_of_args.append(arg_name)
                        selected = self._select_health(section, item,
                                                       search_keywords,
                                                       arg_name)
                    if selected:
                        new_data_dict.setdefault(arg_name, {}).setdefault(
                            selected_options, selected)

        if args_flag:
            # check for the case which multiple `arg_name`s given and check the same
            # among the `arg_name`s. if same between `arg_name`s, data will be overwittern
            # by one of new_data_dict value to execute selected ones
            new_data_flag = False
            if new_data_dict:
                value = ''
                log.debug(
                    'num of health args: {n}'.format(n=len(set(list_of_args))))
                log.debug('num of new_data_dict: {n}'.format(n=len(new_data_dict)))
                if len(set(list_of_args)) == len(new_data_dict):
                    for key, value_ in new_data_dict.items():
                        if value == value_:
                            new_data_flag = True
                        else:
                            new_data_flag = False
                            if not value:
                                value = value_
                                if len(new_data_dict) == 1:
                                    new_data_flag = True
        else:
            new_data_flag = len(set(list_of_args)) == len(new_data_dict)

        log.debug('new_data_flag: {f}'.format(f=new_data_flag))

        log.debug('new_data_dict: {ndd}'.format(
            ndd=json.dumps(new_data_dict, indent=2, sort_keys=True)))

        if new_data_flag:
            temp_data = []
            # override data because meeting criteria by `arg_name`s
            for key in new_data_dict:
                for idx in new_data_dict[key]:
                    temp_data.append(new_data_dict[key][idx].pop())
                data = temp_data
        else:
            if (not new_data_dict or len(set(list_of_args)) !=
                    len(new_data_dict)) and len(set(list_of_args)) != 0:
                data = []
        # processor start message
        log.debug('{type}-processor {name} started'.format(
            name=name, type=processor_type.capitalize()))
        pre_processor_run = True


        # check if `processor` tag matches processor_targets and
        # if device for action is connected
        # create temp_data with matched actions and override data by temp_data
        temp_data = []
        # list of checked devices. flag to ignore checked device
        device_checked = []
        # None if no device is defined in any actions
        all_devices_connected = None

        common_api = False

        for each_data in self._get_actions(data):
            for key in each_data:
                # get processor key from action. by default, `both`
                each_data_dq = Dq(each_data)
                processor_from_yaml = each_data_dq.contains(key).get_values('processor', 0)
                if not processor_from_yaml:
                    processor_from_yaml = 'both'

                log.debug('processor_targets: {pt}'.format(pt=processor_targets))
                log.debug('processor: {p}'.format(p=processor_from_yaml))

                # find `common_api` key and return True/False
                common_api = any(each_data_dq.get_values('common_api'))


                if processor_from_yaml in processor_targets:
                    # check if device for action is connected
                    all_devices_connected = None
                    for uut in self._get_device_names(orig_data, each_data):
                        if uut not in device_checked:
                            device_checked.append(uut)
                            if isinstance(uut, str):
                                if (testbed.devices[uut].name
                                        in devices_connected) or (
                                            testbed.devices[uut].alias
                                            in devices_connected):
                                    all_devices_connected = True
                                else:
                                    all_devices_connected = False
                                    log.info(
                                        'Device {d} is not connected.'.format(
                                            d=testbed.devices[uut].name))
                                    break
                            else:
                                if (uut.name in devices_connected) or (
                                        uut.alias in devices_connected):
                                    all_devices_connected = True
                                else:
                                    all_devices_connected = False
                                    log.info(
                                        'Device {d} is not connected.'.format(
                                            d=testbed.devices[uut].name))
                                    break
                    if (all_devices_connected == True
                            or all_devices_connected is None):
                        temp_data.append(each_data)

        # until here, data contains only actions
        # for cases like `parallel`, `loop`, need to put the headers
        # from original data `orig_data`
        if 'actions' in orig_data and data:
            data = copy.deepcopy(orig_data)
            if temp_data:
                data['actions'] = temp_data
                data = [{'loop': data}]
            else:
                data = []
        elif isinstance(orig_data, list):
            if len(orig_data) > 0 and 'parallel' in orig_data[0] and data:
                data = copy.deepcopy(orig_data)[0]
                if temp_data:
                    data['parallel'] = temp_data
                    data = [data]
                else:
                    data = []
            elif len(orig_data) > 0 and 'run_condition' in orig_data[0] and data:
                data = copy.deepcopy(orig_data)[0]
                data = [data]
            else:
                data = temp_data
        else:
            data = temp_data
        # remove section if no data
        if not data:
            processor.reporter.remove_section(id_list=processor.uid.list)

        # if any device is not connected, processor will be skipped
        # if common_api is True, will execute
        if devices_connected or common_api:
            # instantiate Steps() to reset step number
            steps = Steps()
            # execute dispatcher in Blitz
            result = self.dispatcher(steps, testbed, section, data, name)
            try:
                log.debug('Blitz section return:\n{result}'.format(
                    result=json.dumps(result, indent=2, sort_keys=True)))
            except TypeError:
                log.debug('Blitz section return:\n{result}'.format(
                    result=format_output(result)))
            # check section result
            log.debug('section result: {section_result}'.format(
                section_result=section.result.name))
            log.debug('steps result: {steps_result}'.format(
                steps_result=steps.result.name))
            if processor_type == 'pre' and steps.result != Passed and steps.result != Passx:
                log.info(
                    "Pre-processor pyATS Health {name} was failed, but continue section and Post-processor"
                    .format(name=name))
                # save pre-processor result
                pre_processor_result = steps.result
                return pre_processor_run, pre_processor_result
            elif processor_type == 'post':
                # refrect processor results to section
                processor.result += steps.result
                section.result = section.result + processor.result + self.pre_processor_result

                return pre_processor_run, pre_processor_result
        else:
            if processor_type == 'pre':
                pre_processor_run = False
                # processor is skipped. but call passed to move forward     for this case
                log.info(
                    "Pre-processor pyATS Health '{name}' is skipped because devices are not connected."
                    .format(name=name))
                return pre_processor_run, pre_processor_result
            elif processor_type == 'post':
                # for the case only pre-processors runs
                if section.result == pre_processor_result:
                    log.info(
                        'Only Pre-processor runs. Section result and '
                        'Pre-processor result are different.Reflecting '
                        'Post-processor result to Section.'
                    )
                    # reflect processor results to section
                    section.result = section.result + processor.result + self.pre_processor_result
                log.info(
                    "Post-processor pyATS Health '{name}' was skipped because devices are not connected."
                    .format(name=name))
                return pre_processor_run, pre_processor_result

        return pre_processor_run, pre_processor_result

    def health_dispatcher(self,
                          steps,
                          section,
                          data,
                          testbed,
                          processor,
                          reconnect,
                          name='',
                          **kwargs):
        """
        excute health yaml based on Blitz logic. This will be calling Blitz's
        `dispacher` to execute all the actions in health yaml
        
        `data` contains all the items under a section in health yaml
        
        example of `data`:
        [
          {
            'parallel': [
              {
                'api': {
                  'device': 'uut',
                  'function': 'get_platform_cpu_load',
                  'arguments': {
                    'command': 'show processes cpu',
                    'processes': ['BGP I/O']
                  },
                  'save': [
                    {
                      'variable_name': 'cpu'
                    }
                  ]
                }
              },
              {
                'api': {
                  'device': 'uut',
                  (snip)
        
        `data` is List, so store the `data` as dict to `data_dict` for Dq

        Arguments:
            steps (`obj`) : Aetest Steps object
            section (`obj`) : Aetest Section object
            data (`list`) : data of section
            testbed (`obj`) : testbed object
            processor (`obj`) : Aetest processor object
            name (`str`) : name of section in health yaml
                           Default to ``
            reconnect (`dict` or None) : parameters for reconnect
                                         ex.)
                                         {
                                             'max_time': 900, # maximum time to reconnect
                                             'interval': 60,  # sleep before retry
                                         }
        Returns:
            None
        """

        if 'genie' not in testbed.__module__:
            # convert testbed from pyATS to Genie
            testbed = Converter.convert_tb(runtime.testbed)

        if 'genie' not in testbed.__module__:
            # convert testbed from pyATS to Genie
            testbed = Converter.convert_tb(runtime.testbed)

        # ---------------------
        # pre-context processor
        # ---------------------

        # get connected devices list
        devices_connected = self._check_all_devices_connected(
            testbed, data, reconnect)

        # execute pre-processor and received result in self.pre_processor_result
        self.pre_processor_run, self.pre_processor_result = self._pre_post_processors(
            testbed,
            processor,
            section,
            data,
            name,
            devices_connected,
            processor_targets=['pre', 'both'],
            processor_type='pre')

        try:
            yield
        except Exception as e:
            # make section Errored when exception happens
            section.result = Errored.clone('Caught exception in %s' % str(section),
                               data = {'traceback': e})

        # ----------------------
        # post-context processor
        # ----------------------

        post_if_pre_execute_flag = True
        # check `post_if_pre_execute` and if pre-processor is executed
        for each_data in self._get_actions(data):
            if Dq(each_data).get_values(
                    'processor',
                    0) == 'post_if_pre_execute' and not self.pre_processor_run:
                post_if_pre_execute_flag = False

        if not post_if_pre_execute_flag:
            log.info(
                "Post-processor pyATS Health '{name}' was skipped because required Pre-processor was not executed."
                .format(name=name))

        else:
            if 'genie' not in testbed.__module__:
                # convert testbed from pyATS to Genie
                # need to convert to bring latest status from runtime again
                # for the case devices are connected after pre-processor
                testbed = Converter.convert_tb(runtime.testbed)

            # get connected devices list
            devices_connected = self._check_all_devices_connected(
                testbed, data, reconnect)

            # execute post-processor
            self._pre_post_processors(
                testbed,
                processor,
                section,
                data,
                name,
                devices_connected,
                processor_targets=['post', 'post_if_pre_execute', 'both'],
                processor_type='post',
                pre_processor_result=self.pre_processor_result)
