import re
import logging

# pyATS
from pyats.easypy import runtime
from pyats.results import Passed, Passx
from pyats.aetest.steps import Steps

# Genie
from genie.utils import Dq
from genie.conf.utils.converter import Converter
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.parser.utils.common import format_output

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

        for search_keyword in search_keywords:
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
                    dq_item = Dq(data).contains(search_keyword,
                                                regex=True,
                                                level=1).reconstruct()
                if dq_item and dq_item not in new_data:
                    new_data.append(dq_item)
        return new_data

    def _check_all_devices_connected(self, testbed, data):
        """
        Check if all the targeted devices are connected.
        each device will be checked. if one of devices is not connected,
        return False

        Arguments:
            testbed (`obj`) : testbed object
            data   (`dict`) : data of section
        
        Returns:
            dev_list (`list`): device list which is connected

        """
        dev_list = []
        for each_data in data:
            for dev in Dq(each_data).get_values('device'):
                # check if device object, or not
                if hasattr(dev, 'name'):
                    dev = dev.name
                # check if device exists in testbed and if connected
                if dev in testbed.devices and testbed.devices[
                        dev].is_connected():
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
        args_flag = False

        # check if health arguments are given to pyats command
        for arg_name in ['health_sections', 'health_uids', 'health_groups']:
            if getattr(runtime.args, arg_name):
                args_flag = True

        for arg_name in ['health_sections', 'health_uids', 'health_groups']:

            log.debug('Checking {an}'.format(an=arg_name))
            selected = None
            selected_options = 0
            for item in data:
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
                            value = new_data_dict[key]
                            if len(new_data_dict) == 1:
                                new_data_flag = True

        log.debug('new_data_flag: {f}'.format(f=new_data_flag))
        log.debug('new_data_dict: {ndd}'.format(ndd=new_data_dict))
        if new_data_flag:
            data2 = []
            # override data because meeting criteria by `arg_name`s
            for key in new_data_dict:
                for idx in new_data_dict[key]:
                    data2.append(new_data_dict[key][idx].pop())
                data = data2
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
        # create data2 with matched actions and override data by data2
        data2 = []
        for each_data in data:
            for key in each_data.keys():
                if each_data[key].get('processor', 'both') in processor_targets:
                    # check if device for action is connected
                    uut = Dq(each_data).get_values('device', 0)
                    if uut:
                        if isinstance(uut, str):
                            if (testbed.devices[uut].name in devices_connected) or (testbed.devices[uut].alias in devices_connected):
                                data2.append(each_data)
                        else:
                            if (uut.name in devices_connected) or (uut.alias in devices_connected):
                                data2.append(each_data)
                    # for action which doesn't have device
                    else:
                        data2.append(each_data)
        data = data2
        # remove section if no data
        if not data:
            processor.reporter.remove_section(id_list=processor.uid.list)
        elif not new_data_flag:
            # remove report based on conditions
            # - no found data based on search
            # - number of given arguments and found data are not equal
            # - number of given arguments is not 0
            if (not new_data_dict 
                    or len(set(list_of_args)) != len(new_data_dict)) and len(
                        set(list_of_args)) != 0:
                processor.reporter.remove_section(id_list=processor.uid.list)


        # if any device is not connected, processor will be skipped
        if devices_connected:
            # instantiate Steps() to reset step number
            steps = Steps()
            result = self.dispatcher(steps, testbed, section, data, name)
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
                # refrect result to section
                getattr(
                    section,
                    str(steps.result + steps.result +
                        self.pre_processor_result))()
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
                        'Only Pre-processor runs. Section result and Pre-processor result are different.Reflecting Post-processor result to Section.'
                    )
                    getattr(section,
                            str(section.result + pre_processor_result))()
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
        Returns:
            None
        """
        if 'genie' not in testbed.__module__:
            # convert testbed from pyATS to Genie
            testbed = Converter.convert_tb(runtime.testbed)

        # ---------------------
        # pre-context processor
        # ---------------------

        # get connected devices list
        devices_connected = self._check_all_devices_connected(
            testbed, data)

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
            # for case section gets Exception
            section.errored(e)

        # ----------------------
        # post-context processor
        # ----------------------

        post_if_pre_execute_flag = True
        # check `post_if_pre_execute` and if pre-processor is executed
        for each_data in data:
            if Dq(each_data).get_values('processor', 0) == 'post_if_pre_execute' and not self.pre_processor_run:
                post_if_pre_execute_flag = False

        if not post_if_pre_execute_flag:
            log.info("Post-processor pyATS Health '{name}' was skipped because required Pre-processor was not executed.".format(name=name))

        else:
            if 'genie' not in testbed.__module__:
                # convert testbed from pyATS to Genie
                # need to convert to bring latest status from runtime again 
                # for the case devices are connected after pre-processor
                testbed = Converter.convert_tb(runtime.testbed)

            # get connected devices list
            devices_connected = self._check_all_devices_connected(
                testbed, data)

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
