import re
import copy
import json
import logging

# pyATS
from pyats import aetest
from pyats.easypy import runtime
from pyats.results import Passed, Passx, Errored, Skipped
from pyats.aetest.steps import Steps
from pyats.async_ import pcall

# Genie
from genie.utils import Dq
from genie.conf.utils.converter import Converter
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.parser.utils.common import format_output
from genie.libs.sdk.triggers.blitz.markup import (_load_saved_variable,
                                                  save_variable)

log = logging.getLogger(__name__)

SECTION_CLASS_MAPPING = {
    'CommonSetup': aetest.commons.CommonSetup,
    'CommonCleanup': aetest.commons.CommonCleanup,
    'SetupSection': aetest.sections.SetupSection,
    'CleanupSection': aetest.sections.CleanupSection,
    'TestSection': aetest.sections.TestSection,
    'TestCase': aetest.testcase.Testcase
}


class Health(Blitz):
    def _find_item_by_search_keyword(self, section, data, arg_name,
                                     search_keyword):
        """
        This function will be called when `health_tc_sections`, `health_tc_uids` or
        `health_tc_groups` is given to pyats run command.
        Search `search_keyword` in item based on givin arg_name such as
        `health_tc_sections`, `health_tc_uids` and `health_tc_groups` in search_keyword

        Arguments:
            section (`obj`) : Aetest Subsection object.
            data (`dict`) : data of section
            arg_name (`str`) : one the way to narrow down such as
                                    `health_tc_sections`, `health_tc_uids` or
                                    `health_tc_groups`
            search_keyword (`str`) : keyword to search which supports regex

        Returns:
            data (`dict`) : item if search_keyword can be found in item
                            Otherwise, return empty dict
        """
        # arg health_tc_sections given
        if arg_name in ['health_tc_sections', 'health_sections']:
            if re.search(search_keyword, section.uid):
                return data
        # arg health_tc_uids given
        elif arg_name in ['health_tc_uids', 'health_uids']:
            if re.search(search_keyword, section.uid) or re.search(
                    search_keyword, section.parent.uid):
                return data
        # arg health_tc_groups given
        elif arg_name in ['health_tc_groups', 'health_groups']:
            # groups location is different depending on
            # where the section is in commonSetup/Cleanup or Testcase
            # check `section.groups` first, if not, check `section.parent.groups`
            if isinstance(section, aetest.testcase.Testcase):
                try:
                    for grp in section.groups:
                        if re.search(search_keyword, grp):
                            return data
                except AttributeError:
                    # import remote_pdb; remote_pdb.set_trace()
                    for grp in section.parent.groups:
                        if re.search(search_keyword, grp):
                            return data
        return {}

    def _select_health(self, section, data, search_keywords, arg_name):
        """
        check if pyATS Health Check processor meets criteria
        via `health_tc_sections`, `health_tc_uids` and `health_tc_groups`

        Arguments:
            section (`obj`) : Aetest Subsection object.
            data (`dict`) : data of section
            search_keywords (`list`) :  list of search keywords
            arg_name (`str`) : `health_tc_sections`, `health_tc_uids` or
                               `health_tc_groups`

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
            _, search_keyword = _load_saved_variable(self,
                                                     section=section,
                                                     val=search_keyword)

            if 'type:' in search_keyword:
                search_class = search_keyword.replace('type:', '')
                if isinstance(section,
                              SECTION_CLASS_MAPPING.get(search_class)):
                    new_data.append(data)

            else:
                # get search_target such as section.uid, section.groups from section
                search_target = self._find_search_target(
                    section, arg_name, search_keyword, search_keywords)
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

    def _get_actions(self, data, processor_targets=None):
        """
        get action items only from any Blitz sections such as parallel and loop

        Arguments:
            data   (`dict`) : data of section
            processor_targets (`list`) : list of `processor_flag which ones
                                         will be run as pre/post processors
                                         Defaults to ['pre', 'post', 'both']

        Returns:
            (`dict`): only actions from data
        """
        def _check_processor(actions, processor_targets):
            """
            check `processor` in pyats health yaml should be executed or not

              test_sections:
              - get_testcase_name:
                - api:
                    common_api: true
                    function: get_testcase_name
                    health_sections:
                    - ^(?!common_).*
                    health_uids:
                    - ^(?!common_).*
                    hide_processor: true
                    processor: pre # <- check this
                    save:
                    - variable_name: testcase_name

            Arguments:
                actions (`dict`): action data
                processor_targets (`list`) : list of `processor` which ones
                                             will be run as pre/post processors

            Returns:
                (`list`): list of action data which is supposed to be executed
            """
            return_actions = []
            # example of actions
            # actions = [{
            #     'api': {
            #         'common_api': True,
            #         'function': 'get_testcase_name',
            #         'health_sections': ['^(?!common_).*'],
            #         'health_uids': ['^(?!common_).*'],
            #         'hide_processor': True,
            #         'processor': 'pre',
            #         'save': [{
            #             'variable_name': 'testcase_name'
            #         }]
            #     }
            # }]
            for each_action in actions:
                processor = Dq(each_action).get_values('processor', 0)
                if not processor:
                    processor = 'both'
                if processor in processor_targets:
                    return_actions.append(each_action)
            return return_actions

        if processor_targets is None:
            processor_targets = ['pre', 'post', 'both', 'post_if_pre_execute']
        if data:
            # parsing YAML if data is list or dict
            # Dq doesn't support list at first level, so having this check
            if isinstance(data, list):
                # parallel
                if 'parallel' in data[0]:
                    return _check_processor(data[0]['parallel'],
                                            processor_targets)
                # run_condition
                elif 'run_condition' in data[0]:
                    return _check_processor(
                        data[0]['run_condition']['actions'], processor_targets)
                # normal action
                else:
                    return _check_processor(data, processor_targets)
            elif isinstance(data, dict):
                # loop
                if Dq(data).contains('actions'):
                    return _check_processor(
                        Dq(data).get_values('actions'), processor_targets)

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
        # before running health check, analyze actions and check/resolve
        # device name from %VARIABLES and loop_variable_name for device connectivity check
        for device in Dq(each_data).get_values('device'):
            m = re.search('%VARIABLES{(?P<var_name>.*)}',
                          device.name if hasattr(device, 'name') else device)
            if m:
                var_name = m.groupdict()['var_name']
                if isinstance(
                        data, dict
                ) and 'loop_variable_name' in data and 'value' in data:
                    # loop with list
                    if var_name == data['loop_variable_name']:
                        for dev in data['value']:
                            if dev not in device_list:
                                device_list.append(dev)
                    elif var_name in [
                            data['loop_variable_name'] + '._keys',
                            data['loop_variable_name'] + '._values',
                    ]:
                        if data['value']:
                            for item in data['value']:
                                for dev in item.keys():
                                    if dev not in device_list:
                                        device_list.append(dev)
                elif Dq(each_data).contains('loop_variable_name') and Dq(
                        each_data).contains('value'):
                    # loop with list
                    if var_name == Dq(each_data).get_values(
                            'loop_variable_name', 0):
                        loop_value = Dq(each_data).get_values('value', 0)
                        m = re.search('%VARIABLES{(?P<dev_var_name>.*)}',
                                      loop_value)
                        if m:
                            dev_var_name = m.groupdict()['dev_var_name']
                            # for testscript variables
                            if dev_var_name.startswith('testscript.'):
                                dev_var_name = dev_var_name[len('testscript.'
                                                                ):]
                                try:
                                    loop_value = self.parent.parameters[
                                        'save_variable_name'].setdefault(
                                            'testscript',
                                            {}).get(dev_var_name, [])
                                # if no key yet, just put empty list as iterable
                                except (KeyError, AttributeError):
                                    loop_value = []
                            # testcase variables
                            else:
                                try:
                                    loop_value = self.parameters[
                                        'save_variable_name'].get(
                                            dev_var_name, [])
                                # if no key yet, just put empty list as iterable
                                except KeyError:
                                    loop_value = []
                        for dev in loop_value:
                            if dev not in device_list:
                                device_list.append(dev)
                    elif var_name in [
                            Dq(each_data).get_values('loop_variable_name', 0) +
                            '._keys',
                            Dq(each_data).get_values('loop_variable_name', 0) +
                            '._values',
                    ]:
                        loop_value = Dq(each_data).get_values('value', 0)
                        m = re.search('%VARIABLES{(?P<dev_var_name>.*)}',
                                      loop_value)
                        if m:
                            dev_var_name = m.groupdict()['dev_var_name']
                            markup_variable_value = self.parent.parameters[
                                'save_variable_name'].setdefault(
                                    'testscript', {})
                            # for testscript variables
                            if dev_var_name.startswith('testscript.'):
                                dev_var_name = dev_var_name[len('testscript.'
                                                                ):]
                                if isinstance(
                                        markup_variable_value.setdefault(
                                            dev_var_name, None), dict):
                                    try:
                                        if '_keys' in var_name:
                                            loop_value = markup_variable_value.get(
                                                dev_var_name, []).keys()
                                        else:
                                            loop_value = markup_variable_value.get(
                                                dev_var_name, []).values()
                                    except (KeyError, AttributeError):
                                        loop_value = []
                                elif isinstance(
                                        markup_variable_value.setdefault(
                                            dev_var_name, None), list):
                                    loop_value = markup_variable_value[
                                        dev_var_name]
                                else:
                                    # return empty in case none of above matched
                                    loop_value = []
                            elif isinstance(
                                    markup_variable_value[dev_var_name], dict):
                                try:
                                    if '_keys' in var_name:
                                        loop_value = markup_variable_value.get(
                                            dev_var_name, []).keys()
                                    elif '_values' in var_name:
                                        loop_value = markup_variable_value.get(
                                            dev_var_name, []).values()
                                # if no key yet, just put empty list as iterable
                                except KeyError:
                                    loop_value = []
                            elif isinstance(
                                    markup_variable_value[dev_var_name], list):
                                loop_value = markup_variable_value[
                                    dev_var_name]
                            else:
                                # return empty in case none of above matched
                                loop_value = []
                        for dev in loop_value:
                            if dev not in device_list:
                                device_list.append(dev)
            elif device not in device_list:
                device_list.append(device)

        log.debug('device_list: {}'.format(device_list))
        return device_list

    def _check_all_devices_connected(self, testbed, data, reconnect):
        """
        find search target depending on arg_name (health_tc_uids/health_tc_groups/health_tc_sections)
        for `health_tc_groups`, this function get `groups` from the triggers.

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
        def _connectivity_check(device, testbed, reconnect):
            """
            check device connectivity and retry if needed

            Arguments:
                device (`obj`): device object
                testbed (`obj`) : testbed object
                reconnect (`dict` or None) : parameters for reconnect
                                             ex.)
                                             {
                                                 'max_time': 900, # maximum time to reconnect
                                                 'interval': 60,  # sleep before retry
                                             }

            Returns:
                (`string`): device name if connected. return empty string if not connected
            """
            # check if device object, or not
            if hasattr(device, 'name'):
                device = device.name
            dev_obj = testbed.devices[device]
            # check if device exists in testbed and if device is connected
            if dev_obj.name in testbed.devices and dev_obj.connected:
                if reconnect is None:
                    state = dev_obj.api.verify_device_connection()
                else:
                    state = dev_obj.api.verify_device_connection(
                        reconnect=True,
                        reconnect_max_time=reconnect.get('max_time', 900),
                        reconnect_interval=reconnect.get('interval', 60))
                # verify_device_connection returns True(device connected)/False
                if state:
                    return dev_obj.name
            return ''

        dev_list = []
        device_check_list = []
        # build device_check_list for pcall
        for each_data in self._get_actions(data):
            for dev in self._get_device_names(data, each_data):
                if dev not in device_check_list:
                    device_check_list.append(dev)

        # check connectivity in parallel by pcall
        log.debug('device_check_list: {}'.format(device_check_list))
        if device_check_list:
            # check device connectivity via pcall
            dev_list = pcall(
                _connectivity_check,
                device=set(device_check_list),
                testbed=[testbed for i in range(len(set(device_check_list)))],
                reconnect=[
                    reconnect for i in range(len(set(device_check_list)))
                ])

        # return confirmed connected device list
        log.debug('connected device list: {}'.format(dev_list))
        return dev_list

    def _find_search_target(self, section, arg_name, search_keyword,
                            search_keywords):
        """
        find search target depending on arg_name (health_tc_uids/health_tc_groups/health_tc_sections)
        for `health_tc_groups`, this function get `groups` from the triggers.

        Arguments:
            section (`obj`) : Aetest Subsection object.
            arg_name (`str`) : `health_tc_sections`, `health_tc_uids` or 
                               `health_tc_groups`
            search_keyword (`str`): a keyword to search
            search_keywords (`list`): list of search keywords
        
        Returns:
            search_target (`str`) : found search target depending on arg_name
        """
        # replicate search_keywords for further loop
        search_keywords = copy.deepcopy(search_keywords)

        search_target = ''
        if arg_name in ['health_tc_groups', 'health_groups']:
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
                    log.debug("{ag}/search_target: {uid}".format(
                        ag=arg_name, uid=search_target))
        elif arg_name in ['health_tc_sections', 'health_sections']:
            search_target = section.uid
            log.debug("{ag}/search_target: {uid}".format(ag=arg_name,
                                                         uid=search_target))
        elif arg_name in ['health_tc_uids', 'health_uids']:
            for kw in search_keywords:
                # load `%VARIABLES{} and replace`
                _, kw = _load_saved_variable(self, section=section, val=kw)
                if re.search(kw, section.uid):
                    search_target = section.uid.split('.')[0]
                    log.debug("{ag}/search_target(section.uid): {uid}".format(
                        ag=arg_name, uid=section.uid))
                elif re.search(kw, section.parent.uid):
                    search_target = section.parent.uid.split('.')[0]
                    log.debug(
                        "{ag}/search_target(section.parent.uid): {uid}".format(
                            ag=arg_name, uid=section.parent.uid))
        return search_target

    def _pre_post_processors(self,
                             testbed,
                             processor,
                             section,
                             data,
                             name,
                             reconnect,
                             processor_targets,
                             processor_type,
                             pre_processor_result=Passed,
                             health_settings=None):
        """
        execute pre/post processors and return if pre-processor runs and processor result

        Arguments:
            testbed (`obj`): testbed object
            processor (`obj`): Aetest Processor object
            section (`obj`): Aetest Section object
            data (`list`) : data of section
            name (`str`) : name of section in health yaml
            reconnect (`dict` or None) : parameters for reconnect
            processor_targets (`list`) : list of `processor_flag which ones 
                                         will be run as pre/post processors
            processor_type (`str`) : processor type `pre` or `post`
            pre_processor_result (`ob`) : result object. Default to `Passed`

        Returns:
            pre_processor_run (`bool`) : if pre processor runs or not
            pre_processor_result (`obj`) : return processor result (Result obj)
        """
        devices_connected = []
        new_data_dict = {}
        selected_options = 0
        list_of_args = []
        # store reasons why processor is skipped
        reasons = []
        # flag if health args are given to pyats command
        args_flag = False
        # flag if health args are defined under action in health yaml
        args_in_yaml_flag = False
        log.debug(
            'data:\n{d}'.format(d=json.dumps(data, indent=2, sort_keys=True)))
        orig_data = copy.deepcopy(data)

        # check if health arguments are given to pyats command
        for arg_name in [
                'health_tc_sections', 'health_tc_uids', 'health_tc_groups',
                'health_sections', 'health_uids', 'health_groups'
        ]:
            if getattr(runtime.args, arg_name):
                args_flag = True
            for item in self._get_actions(data, processor_targets):
                if Dq(item).contains(
                        'health_tc_sections|health_tc_uids|health_tc_groups|health_sections|health_uids|health_groups',
                        regex=True):
                    args_in_yaml_flag = True

        for arg_name in [
                'health_tc_sections', 'health_tc_uids', 'health_tc_groups',
                'health_sections', 'health_uids', 'health_groups'
        ]:
            log.debug('Checking {an}'.format(an=arg_name))
            selected = None
            selected_options = 0
            for item in self._get_actions(data, processor_targets):
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
                        #     health_tc_sections: section1
                        # - api:               # all sections
                        #     function: func2
                        if (args_in_yaml_flag and arg_name
                                in ['health_tc_sections', 'health_sections']
                                and
                            ((not Dq(item).get_values('health_tc_sections')
                              or not Dq(item).get_values('health_sections'))
                             and (not Dq(item).get_values('health_tc_uids')
                                  or not Dq(item).get_values('health_uids')))):
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
                log.debug(
                    'num of new_data_dict: {n}'.format(n=len(new_data_dict)))
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
            for key, value__ in new_data_dict.items():
                for idx in value__:
                    # data from each health arg should be same
                    # so remove redundant data by overwriting
                    temp_data = [new_data_dict[key][idx].pop()]
                data = temp_data
        elif (not new_data_dict or len(set(list_of_args)) != len(new_data_dict)
              ) and len(set(list_of_args)) != 0:
            reasons.append(
                f"health arg {set(list_of_args)-set(new_data_dict.keys())} does not meet criteria"
            )
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

        if new_data_dict and new_data_flag:
            # get connected devices list
            devices_connected = self._check_all_devices_connected(
                testbed, data, reconnect)
            devices_connected = [dev for dev in devices_connected if dev != '']

        actions = self._get_actions(data, processor_targets)
        if not actions:
            # check processor in action and put in proc_in_action
            proc_in_action = []
            if isinstance(data, list):
                for each_data in data:
                    for each_proc in Dq(each_data).get_values('processor'):
                        proc_in_action.append(each_proc)
            else:
                for each_proc in Dq(data).get_values('processor'):
                    proc_in_action.append(each_proc)
            proc_in_action = set(proc_in_action)
            if proc_in_action:
                reasons.append(
                    f"processor {proc_in_action} does not meet criteria {processor_targets}"
                )
        for each_data in actions:
            for key in each_data:
                # get processor key from action. by default, `both`
                each_data_dq = Dq(each_data)
                processor_from_yaml = each_data_dq.contains(key).get_values(
                    'processor', 0)
                if not processor_from_yaml:
                    processor_from_yaml = 'both'

                log.debug(
                    'processor_targets: {pt}'.format(pt=processor_targets))
                log.debug('processor: {p}'.format(p=processor_from_yaml))

                # find `common_api` key and return True/False
                common_api = any(each_data_dq.get_values('common_api'))

                if processor_from_yaml in processor_targets:
                    # check if device for action is connected
                    all_devices_connected = None
                    devices_not_connected = []
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
                                    devices_not_connected.append(uut)
                            elif (uut.name in devices_connected) or (
                                    uut.alias in devices_connected):
                                all_devices_connected = True
                            else:
                                all_devices_connected = False
                                devices_not_connected.append(uut)

                    if devices_not_connected:
                        log.warning("devices are not connected: {}".format(
                            devices_not_connected))

                    force_all_connected = health_settings.get(
                        'force_all_connected', True)
                    if device_checked and not force_all_connected and devices_connected:
                        log.warning(
                            "force_all_connected is False. Executing even though some of devices might not be connected."
                        )
                    # data will be created if all devices are connected or
                    # if force_all_connected == False and one of devices is connected
                    if (all_devices_connected == True or all_devices_connected
                            is None) or (force_all_connected == False
                                         and devices_connected):
                        temp_data.append(each_data)
                    else:
                        log.warning('health check is blocked due to force_all_connected is True.')

        # until here, data contains only actions
        # for cases like `parallel`, `loop`, need to put the headers
        # from original data `orig_data`
        if 'actions' in orig_data and data and temp_data:
            data = copy.deepcopy(orig_data)
            if temp_data:
                data['actions'] = temp_data
                data = [{'loop': data}]
            else:
                data = []
        elif isinstance(orig_data, list):
            if len(orig_data
                   ) > 0 and 'parallel' in orig_data[0] and data and temp_data:
                data = copy.deepcopy(orig_data)[0]
                if temp_data:
                    data['parallel'] = temp_data
                    data = [data]
                else:
                    data = []
            elif len(orig_data) > 0 and 'run_condition' in orig_data[
                    0] and data and temp_data:
                data = copy.deepcopy(orig_data)[0]
                data = [data]
            else:
                data = temp_data
        else:
            data = temp_data
        # remove section if no data
        removed_section = False
        # set reason in case device is not connected
        if (not devices_connected and not common_api) and not reasons:
            reasons.append('Device is not connected')
        if not data or reasons:
            processor.result = Skipped
            processor.reporter.remove_section(id_list=processor.uid.list)
            removed_section = True

        # if any device is not connected, processor will be skipped
        # if common_api is True, will execute
        if devices_connected or common_api:
            # instantiate Steps() to reset step number
            steps = Steps()
            # execute dispatcher in Blitz
            result = self.dispatcher(steps, testbed, section, data, name)

            if isinstance(data, list):
                hide_processor = any(
                    Dq(data[0]).get_values('hide_processor', 0) == True
                    for each_data in data)

            else:
                hide_processor = Dq(data[0]).get_values('hide_processor', 0)

            if hide_processor and not removed_section:
                removed_section = self._remove_section(processor)
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

            # if section is skipped by run_condition, remove section
            if (isinstance(result, dict) and 'run_condition_skipped' in result
                    and not removed_section
                    and result['run_condition_skipped'] == True):
                processor.result = Skipped
                removed_section = self._remove_section(processor)
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

                # return processor.result to raise the result
                # at end of context post processor
                return pre_processor_run, processor.result

        elif processor_type == 'pre':
            pre_processor_run = False
            # processor is skipped
            log.info(
                f"Pre-processor pyATS Health '{name}' is skipped due to: {reasons}"
            )
            if pre_processor_result == Passed:
                # processor.skipped()
                pre_processor_result = Skipped
            return pre_processor_run, pre_processor_result
        elif processor_type == 'post':
            # for the case only pre-processors runs
            if section.result == pre_processor_result:
                log.info('Only Pre-processor runs. Section result and '
                         'Pre-processor result are different.Reflecting '
                         'Post-processor result to Section.')
                # reflect processor results to section
                section.result = section.result + processor.result + self.pre_processor_result
            # processor is skipped
            log.info(
                f"Post-processor pyATS Health '{name}' was skipped due to: {reasons}"
            )
            if pre_processor_result == Passed:
                # processor.skipped()
                pre_processor_result = Skipped

            # return processor.result to raise the result
            # at end of context post processor
            return pre_processor_run, processor.result

        return pre_processor_run, pre_processor_result

    def _remove_section(self, processor):
        processor.reporter.remove_section(id_list=processor.uid.list)
        log.debug('removed section: {}'.format(processor.uid.list))

        return True

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

        if 'health_settings' in kwargs:
            health_settings = kwargs['health_settings']
        else:
            health_settings = {}

        # save `health_settings` as testscript variable
        save_variable(self, section, 'testscript.health_settings',
                      health_settings)
        # handling for `health_settings.devices`. TODO; AttrDict support
        if 'devices' in health_settings:
            save_variable(self, section, 'testscript.health_settings.devices',
                          health_settings['devices'])

        # ---------------------
        # pre-context processor
        # ---------------------

        # set result Passed at beginning of section in pre processor
        # because section sometimes doesn't have any item like commonCleanup
        # if the section doesn't have any, section.result is None and rolled-up
        # only with pyATS Health Check result. But section should have Passed 
        # at first place
        if section.__result__ is None:
            section.result = Passed

        # execute pre-processor and received result in self.pre_processor_result
        self.pre_processor_run, self.pre_processor_result = self._pre_post_processors(
            testbed,
            processor,
            section,
            data,
            name,
            reconnect,
            processor_targets=['pre', 'both'],
            processor_type='pre',
            health_settings=health_settings)

        try:
            yield
        except Exception as e:
            # make section Errored when exception happens
            section.result = Errored.clone('Caught exception in %s' %
                                           str(section),
                                           data={'traceback': e})

        # ----------------------
        # post-context processor
        # ----------------------
        post_if_pre_execute_flag = not any(
            Dq(each_data).get_values('processor', 0) == 'post_if_pre_execute'
            and not self.pre_processor_run
            for each_data in self._get_actions(data))

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

            # execute post-processor
            _, post_processor_result = self._pre_post_processors(
                testbed,
                processor,
                section,
                data,
                name,
                reconnect,
                processor_targets=['post', 'post_if_pre_execute', 'both'],
                processor_type='post',
                pre_processor_result=self.pre_processor_result,
                health_settings=health_settings)

            # raise result
            getattr(processor, post_processor_result.name)()
