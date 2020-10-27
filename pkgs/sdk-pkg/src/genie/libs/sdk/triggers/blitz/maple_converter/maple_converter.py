import os
import re
import sys
import yaml
import json
import random
import string
import ruamel.yaml

from ats.easypy import runtime

from genie.testbed import load
from genie.libs.sdk.triggers.blitz.maple_converter.cmds_converter import CMDS_Converter
from genie.libs.sdk.triggers.blitz.maple_converter.legacy_maple_converter import Internal_Converter
from genie.libs.sdk.triggers.blitz.maple_converter.legacy_dme_converter import Legacy_DME_Converter
from genie.libs.sdk.triggers.blitz.maple_converter.legacy_smartman_converter import Legacy_Smartman_Converter

class Converter(object):
    def __init__(self, maple_file, new_yaml=None, testbed=None, testcase_control=None, teststep_control=None):

        self.maple_file = maple_file
        self.new_yaml = new_yaml
        self.uids = []
        self.testbed = load(testbed) if testbed else runtime.testbed
        self.testcase_control = testcase_control
        self.teststep_control = teststep_control

    def convert(self):

        """
        Function description: Recieves the maple yamle file name and covert it into blitz yaml file

        args:

        returned_value: 
            A list containing all the blitz trigger uids neccesary to be used in the job file
        """

        blitz_dict = {}

        self.verify_maple_env()

        # File text into string
        with open(self.maple_file, 'r') as tempfile:
            maple_string = tempfile.read()

        # Replace all the maple markups
        maple_string = self._maple_markup_devices(maple_string)
        maple_string = self._maple_markup_variables(maple_string)
        # create a dictionary object of the yaml file
        maple_dict = ruamel.yaml.safe_load(maple_string)
        for testcase_name, testcase_data in maple_dict['tests'].items():
            # multiple tests might exists within a maple testcase, and they all need to be extracted one by one
            blitz_dict.update({testcase_name: self._testcase_convertor(testcase_data,testcase_name)})

            # Adding the testcasename to a list 
            # The list will be returned to job file so it would used as trigger uids
            self.uids.append(testcase_name)
        with open(self.blitz_file, 'w') as blitz_file_dumped:
            blitz_file_dumped.write(ruamel.yaml.round_trip_dump(blitz_dict))

        return self.uids

    def _testcase_convertor(self, maple_testcase_data, maple_testcase_name):

        """Example of a maple testcase:
        tests: 
            confirm_and_search:                 <-- testcase_name
                test-steps:                     <-- Everything from here on is testcase_data
                    step-1:                     <-- section name
                        confirm:
                            devices:
                                N93_3:
                                    rule-1:
                                        type: cli
                                        commands: |
                                            show vdc
        ___________________________________________________

        Function_description: Get each testcase within the maple yaml file and perform blitz conversion on it
        args:
            maple_testcase_data: The yaml data of one maple testcase
                                 datatype: dict

            maple_testcase_name: The name of one maple testcase
                                datatype: string

        returned_value: 
            type(dict): containing the testcase maple that is converted to blitz
        """

        # Will generate the actual Testcase yaml
        blitz_testcase_data = {}
        # List of all the sections within a testcase
        blitz_sections_list = []

        # Log collection - Check if log collection is there
        # For blitz - it is a post-processor
        log_processor = maple_testcase_data.pop('log', None)

        # logical id that is used to store testcase result into TIMS
        tims_logical_id = maple_testcase_data.pop('logical_id', None)

        # setting continue value for each section in blitz
        # the value can be assigned from testsuite using testcase_control keyword
        if self.testcase_control:
            section_continue = self.testcase_control

        # if not specified there look for the equivalent in the testcase,
        # otherwise None
        else:
            section_continue = maple_testcase_data.pop('testcase_control', None)
        
        # setting  continue value for each action in blitz
        # since in maple this value is generated in the step level
        # The value should be passed out further to other function that creates
        # blitz actions to add the keyword to their dictionary 
        # the value can be assigned from testsuite using teststep_control keyword
        if self.teststep_control:
            action_continue = self.teststep_control

        # if not specified there look for the equivalent in the testcase,
        # otherwise None
        else:
            action_continue = maple_testcase_data.pop('teststep_control', None)

        # Extracting log collection data and translating it into processor
        if log_processor:
            blitz_testcase_data.update(self._log_converter(log_processor))

        # Each test would be map to one test in blitz and they all need source and class
        blitz_testcase_data.update({'source':
                           {'pkg': 'genie.libs.sdk',
                            'class': 'triggers.blitz.blitz.Blitz'},
                            'test_sections' : blitz_sections_list})

        if tims_logical_id:
            blitz_testcase_data.update({'tims': {'logical_id': tims_logical_id}})

        # Maple steps are technically sections in blitz. 
        # In blitz section are build on various actions,
        # Major actions in maple are confirm, apply and unapply,
        # which translates to various actions in blitz.
        if 'test-steps' not in maple_testcase_data:
            if  'confirm' in maple_testcase_data.keys() or\
                'apply' in maple_testcase_data.keys() or\
                'unapply' in maple_testcase_data.keys() :

                maple_testcase_data = {'test-steps': {'step-1':maple_testcase_data}}
            else:
                maple_testcase_data = {'test-steps': maple_testcase_data}

        # A maple testcase can have multiple sections and each section can have
        # up to 3 different action apply, confirm unapply
        for section, action_dict in maple_testcase_data['test-steps'].items():

            '''reminder blitz-format:
                    test_sections:
                        - <section-name>:
                            - <action-name>:
                                <key>: <value>
                                <key>: <value>
            '''

            # defining the list of actions
            blitz_action_list = []

            # if section continue == abort-on-failure
            # this would add the continue: False to the list of blitz actions for this section
            if section_continue == 'abort-on-failure':
                blitz_action_list.append({'continue': False})

            # Adding all the blitz action
            blitz_action_list = self._action_dispatcher(action_dict, blitz_action_list, action_continue)
            blitz_sections_list.append({section: blitz_action_list})

        return blitz_testcase_data

    def _maple_markup_devices(self, maple_data):

        ''' Example of replacing device{<path_to_device>} with its actual device equivalent
            example of maple before replacement:

                test-steps:
                    step-1:
                        apply:
                            devices:
                                device{testbed.custom.devices.host1}: <-- maple markup
                                   type: cli
                                   commands: |
                                       conf t
            
            example of maple after replacement:

                test-steps:
                    step-1:
                        apply:
                            devices:
                                N93_3:                                <-- replaced value
                                   type: cli
                                   commands: |
                                       conf t
            __________________________________
            Function description: This function replaces maple markup for devices with actual device name from testbed

            args:
                maple_data: maple_data yaml file as an string
                            datatype: string

            returned_value: 
                type(string): the maple yaml file string with markup replaced
        '''

        if maple_data is not None:
            device_names = re.findall(r'device\{[\w._\/]+\}', str(maple_data))

            for name in device_names:
                key_orig = name.replace('device{','').replace('}','')
                # TODO comment this section
                testbed_info = self._testbed_info_gen(key_orig, self.testbed)
                if testbed_info is not None:
                    maple_data = maple_data.replace(name,str(testbed_info))

        return maple_data

    def _maple_markup_variables(self, maple_data):

        ''' replacing %{path_to_keyword_variable} with its actual  equivalent
            example of maple before replacement:

            type: cli
            commands: |
                conf t
                interface %{testbed.custom.name.host12ixia_port}
                switchport
                switchport mode trunk
                no shut
                conf t
                interface %{testbed.custom.name.host12vpc1_l1}
            
            example of maple after replacement:

            type: cli
            commands: |
                conf t
                interface Ethernet1/32
                switchport
                switchport mode trunk
                no shut
                conf t
                interface Ethernet1/20
            __________________________________
            Function description: This function replaces maple markup variables with equal value from testbed

            args:
                maple_data: maple_data yaml file as an string
                            datatype: string

            returned_value: 
                type(string): the maple yaml file string with markup replaced

        '''

        if maple_data is not None:

            referenece_names = re.findall(r'%\{[\w._\-\/]+\}', maple_data)
            for name in referenece_names:
                key_orig = name.replace('%{','').replace('}','')
                # TODO comment this section
                testbed_info = self._testbed_info_gen(key_orig, self.testbed)
                # TODO comment this section
                if testbed_info is not None:
                    maple_data = maple_data.replace(name,str(testbed_info))
                else:
                    if os.environ.get(key_orig) is not None:
                        maple_data = maple_data.replace(name,os.environ.get(key_orig))
        return maple_data

    def verify_maple_env(self):
        
        '''
        Function description: Verifies whether the maple environment is exported into path
        '''

        if 'MAPLE_PATH' not in os.environ:
            raise Exception('Make sure to set MAPLE_PATH before running your '
                            'mpale script in the converter')

        if os.environ['MAPLE_PATH'] not in sys.path:
            sys.path.append(os.environ['MAPLE_PATH'])
    
    @property
    def testbed_file(self):

        return  os.path.abspath(self.testbed.testbed_file)

    @property
    def testbed_file(self):
        return  os.path.abspath(self.testbed.testbed_file)

    @property
    def testbed_file(self):
        return  os.path.abspath(self.testbed.testbed_file)

    @property
    def blitz_file(self):

        maple_script_full_path = os.path.abspath(self.maple_file)
        maple_script_path_splited = os.path.split(maple_script_full_path)
        blitz_script_file_name = maple_script_path_splited[1]
        dir_name = maple_script_path_splited[0]
        
        if not self.new_yaml:
            blitz_file_name = 'blitz_{}'.format(blitz_script_file_name)
        else:
            blitz_file_name = self.new_yaml

        return '{}/{}'.format(dir_name, blitz_file_name)

    def _get_value_to_replace(self, key, obj):

        # TODO - Comment this out debug the code 
        '''
            Function description: This is a helper function for markup replace 
                                  parse the testbed and the key to get to the exact value to replace
        '''

        if type(obj).__name__ == 'Testbed' and key == 'testbed':
            return obj

        #Rename topology to devices
        if key == 'topology':
            key = 'devices'

        if hasattr(obj,key):
            return getattr(obj,key)
        elif type(obj).__name__ == 'AttrDict' or type(obj).__name__ == 'dict':
            return obj.get(key)
        elif type(obj).__name__ == 'set':
            for link in obj:
                if link.name == key:
                    return link


    def _testbed_info_gen(self, key_orig, testbed):

        # TODO - Comment this out debug the code 

        '''
            This is a helper function for markup replace 
            parse the testbed to the point of the exact path to the value
            
        '''
        key = key_orig.replace('topology.links','testbed.links')
        tree_keys = key.split('.')
        testbed_info = testbed
        for tree_key in tree_keys:
            testbed_info = self._get_value_to_replace(tree_key, testbed_info)

        return testbed_info

    def _action_dispatcher(self, action_dict, blitz_action_list, action_continue):

        ''' Info: Three types of maple_actions exist:

                1 - apply 
                2 - unapply
                3 - confirm
        
        ____________________
        Function description:
                This function simply dispatch maple_actions to the proper converter function
                that does the conversion of actions from maple to their blitz equivalent
        args:
            action_dict: maple actions in a dictionary
                        datatype: dict
            
            action_continue: the continue value for blitz action 
                             datatype: boolean

        returned_value: 
                type(list): A list of converted maple_actions to equivalent blitz actions for A section of A testcase
        '''

        # loop flag in case that the section has a loop 
        # using this loop later we add the actions 
        # underneath the loop keyword in blitz
        loop = False

        # This is the value to store output of an apply action and all of its commands
        # necessary in case a query is running on an apply action output
        val_to_search_apply = None

        # Check whether a maple action is confirm or apply/unapply
        for maple_action, data in action_dict.items():

            # Function to add the condition as a blitz action
            # reminder: section_control action is the equivalent of 
            # flowcontrol in blitz
            if maple_action == 'flowcontrol':
                blitz_action_list.append(self._flow_control_converter(data)) 

            # Function adjust the the layout of the dictionary of a blitz section
            # So blitz would have a loop keyword on top 
            if maple_action == 'loop':
                blitz_action_list.append(self._loop_converter(data))
                loop = True

            # dispatching apply/unapply actions to its converters
            if maple_action == 'apply' or maple_action == 'unapply':
                blitz_action_list, val_to_search_apply = self._apply_unapply_converter(data,
                                                                                blitz_action_list,
                                                                                action_continue,
                                                                                maple_action,
                                                                                loop)
            # dispatching confirm actions to its converters
            if maple_action == 'confirm':
                blitz_action_list = self._confirm_converter(data, blitz_action_list, action_continue, loop, val_to_search_apply)

        return blitz_action_list

    def _log_converter(self, log_processor):

        '''Convert Maple dict for log into processor

           tests:
               log_collection_test:
                 log:
                   states: passed, failed                               <-- Testcase results
                   devices: N93_3                                       <-- The device that the log collection is occuring on
                   server: scp_server,scp,/ws/mziabari-ott/,management  <-- the server that would users want to send their log to
                   commands: |                                          <-- Commands that logs are collected on 
                       show version
        =================================================================
            log_collection_test:
              processors:
                post:
                  post_execute_command:
                    method: genie.libs.sdk.libs.abstracted_libs.post_execute_command
                    parameters:
                      zipped_folder: false
                      save_to_file: per_command
                      valid_section_results:
                      - passed
                      - failed
                      server_to_store:
                        server_in_testbed: scp_server
                        protocol: scp
                        remote_path: /ws/mziabari-ott/development
                      devices:
                        N93_3:
                          cmds:
                          - cmd: show version
        _________________________________
        Function description: convert the log collection subsection of a maple testcase into a genie post_processor

        args:
            log_processor: A dictionary containing the log subsection of a maple testcase 
                          datatype: dict

        returned_value: 
                type(dict) containing the processor equivalent of log collection input in maple

        '''

        post_processor_dict = {}

        # Extract the log collection input and mapping it into a post_processor
        # Info: If testcase results are not in this list the post_processor would skip in genie
        valid_section_results = log_processor['states'].split(',') 

        devices = log_processor['devices'].strip(' ').split(',')
        log_commands = log_processor['commands'].split('\n')

        commands = []
        for cmd in log_commands:
            
            if  cmd:
                commands.append({'cmd': cmd})

        if 'server' in log_processor:
            server_info_list = log_processor['server'].split(',')

        post_processor_dict.update({'processors': {'post':{'post_execute_command':
                              {'method':'genie.libs.sdk.libs.abstracted_libs.post_execute_command',
                               'parameters':{'zipped_folder': False, 'save_to_file':'per_command',
                               'valid_section_results': valid_section_results,
                               'server_to_store':{
                                   "server_in_testbed": server_info_list[0],
                                   'protocol': server_info_list[1],
                                   'remote_path':server_info_list[2]
                               },
                               'devices': {}}}}}})

        for device in devices:
            device = device.strip(' ')
            post_processor_dict['processors']['post']['post_execute_command']['parameters']['devices'].update({device:{'cmds':commands}})

        return post_processor_dict

    def _flow_control_converter(self, data):

        dict_vals = {}

        # %VARIABLES{}
        data_json = json.loads(data) 
        if  'XX(' in data_json['condition'] and\
            ')XX' in data_json['condition']:

            data_json['condition'] = Internal_Converter._XX_pattern_matching(data_json['condition'], 'replace')

        # Make it simpler with adding ed to the end.
        if data_json['action'] == 'skip':
            data_json['action'] = 'skipped'
        else: 
            data_json['action'] = data_json['action'] + 'ed'

        dict_vals.update({'section_control':{'if': data_json['condition'],
                          'function': data_json['action']}})

        return dict_vals

    def _loop_converter(self, maple_data):

        # Extracting the loop from maple code and changing the section layout
        # To have loop on top of all the other actions
        dict_vals = {}
        p = re.compile(r'{(?P<loop_plugin>[\S\s]+)}')
        m = p.match(maple_data)
        section = '{' + m.group(1) + '}'

        dict_vals.update({'loop':{'maple': True, 'section': section}})

        return dict_vals

    def _apply_unapply_converter(self, apply_unapply_data, blitz_action_list, action_continue, maple_action, loop=None):

        ''' Example of the layout of apply action

        test-steps:
            step-1:
                apply: <--- maple_action
                    devices:
                        N93_3: <-- device to run the config on
                            type: cli <-- type of maple_action
                            commands: |  <---- commands that will be configured/applied to the device
                                conf t
                                feature bfd
        ____________________________________________
        Function description:

        args: 
            apply_unapply_data:
        '''

        for dev, data in apply_unapply_data['devices'].items():

            # For IXIA legacy option connection was automatic but for plugins its manual
            # Then we need to connect it in plugins and since we translate legacy mode to
            # Plugins I need to add a connect on top of each IXIA legacy command
            if data['type'] == 'tgen-config':

                connect = '#@# cmds=connect: #@#                  \n'
                commands_actually = data['commands']
                data['commands'] = connect + commands_actually

            # dmerest flag 
            dmerest = True if data['type'] == 'dmerest' else False

            # Different types of commands (cmds, plugins or show command)
            # might be the input of the apply action, these command needs
            # to separated 
            command_type_list =Internal_Converter._command_separator(data['commands'], dmerest=dmerest, configure=True)

            letters = string.ascii_lowercase
            val_to_search_apply = ''.join(random.choice(letters) for i in range(10))

            for command in command_type_list:
                blitz_action_dict, blitz_action = self._maple_command_to_blitz_action_converter(data['type'],\
                                                        command, dev, maple_action)
                # This is hacky :-(
                # There is sometimes a need to match/umatch the output of a apply/configure action
                # Since match/unmatch would always be done in confirm section, we need to store that value
                # and send to confirm section so in case there is no commands, code performs match/unmatch
                if blitz_action == 'configure':
                    blitz_action_dict[blitz_action].update({'save': [{'variable_name': val_to_search_apply, 'append': True}]})

                if not action_continue or action_continue != 'continue-on-failure':
                    blitz_action_dict[blitz_action].update({'continue': False})

                # if loop, since 
                # there would be technically one action in blitz
                # all the blitz actions should be moved underneath the loop keyword
                if loop:
                    if 'actions' not in blitz_action_list[0]['loop']: 
                        blitz_action_list[0]['loop'].update({'actions':[blitz_action_dict]})
                    else:
                        blitz_action_list[0]['loop']['actions'].append(blitz_action_dict)
                else:
                    blitz_action_list.append(blitz_action_dict)

        return blitz_action_list, val_to_search_apply

    def _confirm_converter(self, confirm_data, blitz_action_list, action_continue, loop=None, val_to_search_apply=None):

        ''' Example of the layout of confirm action

        step-2:
            confirm: <--- Maple action
                devices:
                    N93_3:
                        rule-1: <-- rule_id (To generate multiple confirm actions)
                            type: cli
                            commands: |
                                show vlan
                                show vrf 
                                show nxapi
                                #@# cmds=waitfor:::show module,,Up,,10 #@#
        '''

        # check device name, for patterns like device{testbed.devices.<name>}
        search = False

        for dev, data in confirm_data['devices'].items():
            for rule_id, rule_data in data.items():

                # action confirms does have one more level called rule.
                # rules contains commands, and match/unmatch section, and the existance is and or or
                # which means there could be all of the together but there might be only match some times

                # There might be confirm actions with not commands
                # Uses for cmds=eval which in turn === action compare in blitz
                # OR uses for match/unmatch an apply action
                # val_to_search_apply has use for that
                if 'commands' not in rule_data:
                    blitz_action_dict = {}
                    blitz_action_dict = self._match_unmatch_dispatcher(blitz_action_dict, 'compare', rule_data['type'],\
                                               rule_id, device=dev, match=rule_data.get('match'), \
                                               unmatch=rule_data.get('unmatch'), val_to_search_apply=val_to_search_apply)
                    blitz_action_list.append(blitz_action_dict)
                    continue

                # command_separator extract each command from the list of inputted
                # commands and returns them in a list. 3 types of commands exist in a confirm action
                # Normal as ('show_version', 'show interface'), 
                # Plugin commands that are python function as ('commandplugins' and 'matcherplugins'),
                # pattern matching commands that as (#cmds=patterns:::)
                command_type_list = Internal_Converter._command_separator(rule_data['commands'])
                # function to translate cmds patterns to blitz equivalent
                # then it is arithmatic match
                val_to_search = rule_id + '_match_unmatch'

                for command in command_type_list:

                    # command_translator gets each command, and based on their type (normal command or plugins)
                    # returns the type of action(s) that would be executed in blitz 
                    # and the dictionary representation of the action and its arguments
                    blitz_action_dict, action = self._maple_command_to_blitz_action_converter(rule_data['type'],
                                                            command, dev, 'confirm', rule_id)
                    if rule_data.get('match') or rule_data.get('unmatch'):

                        search = True
                        # TODO One loop limitation that cannot loop over a multiple command
                        # single confirm action (Yet never seen its example)
                        # if loop and because of the mentioned limitation, there is always one command to be queried
                        # Hence no need to append
                        save_list = [{'variable_name': val_to_search}]
                        if not loop:
                            save_list[0].update({'append': True})

                        try:
                            blitz_action_dict[action].update({'save': save_list})
                        except KeyError:
                            if "specifically_patterns" in blitz_action_dict:
                                pass

                    if not action_continue or action_continue != 'continue-on-failure':
                        try:
                            blitz_action_dict[action].update({'continue': False})
                        except KeyError:

                            # for cmds=patterns the output would be a dictionary of
                            # multiple blitz actions that is saved into a list
                            # It is necessary to update all those actions one by one
                            if "specifically_patterns" in blitz_action_dict:
                                blitz_action_dict.update({action:{'continue': False}})

                    if loop:
                        if 'actions' not in blitz_action_list[0]['loop']: 
                            blitz_action_list[0]['loop'].update({'actions':[blitz_action_dict]})
                        else:
                            blitz_action_list[0]['loop']['actions'].append(blitz_action_dict)
                    else:
                        if "specifically_patterns" in blitz_action_dict:
                            cont_ = blitz_action_dict.pop(action, None)
                            for item in blitz_action_dict['specifically_patterns']:
                                if cont_:
                                    item[action].update({'continue': False})
                                blitz_action_list.append(item)
                        else:
                            blitz_action_list.append(blitz_action_dict)

                # in case match/unmatch exist, a map should be constructed
                # between match/unmatch to include/exclude
                # and the blitz action dictionary will be updated
                # match/unmatch might not always map to include exclude
                # they can be mapped to an equivalent action in blitz
                if search:
                    if "specifically_patterns" in blitz_action_dict:
                        for action_dict in blitz_action_dict['specifically_patterns']:
                            action_dict = self._match_unmatch_dispatcher(action_dict, 'maple_search', rule_data['type'],
                                                       rule_id, device=dev, match=rule_data.get('match'),
                                                       unmatch=rule_data.get('unmatch'), val_to_search=val_to_search)
                    else:
                        blitz_action_dict = self._match_unmatch_dispatcher(blitz_action_dict, 'maple_search', rule_data['type'],
                           rule_id, device=dev, match=rule_data.get('match'),
                           unmatch=rule_data.get('unmatch'), val_to_search=val_to_search)

        return blitz_action_list

    def _maple_command_to_blitz_action_converter(self, maple_action_type, command, device, maple_action, rule_id=None):

        ''' Example of different commands in maple 
            confirm:
                devices: 
                    N93_3:
                        rule-1: <-- rule_id
                            type: dmerest|yangrest|cli|tgen-config|smartman <-- all type of maple_action_type 
                            commands: |
                                show module                                         <-- show commands
                                #@# cmds=waitfor:::show module,,Up,,10 #@#          <-- cmds commands

                                                                                    <-- plugin commands
                                #@# matcher:{                                       <-- plugin_type == matcher|confirm|commands
                                    "package":"maple.plugins.user.MatcherPlugins",  <-- package that plugin is residing in maple code
                                    "method":"populateObjects",                     <-- plugin method that will be called in maple code
                                    "command":"show version",                       <-- from here on out, the arguments to that maple plugin method
                                    "type":"cli"
                                    }    
                                #@#

                                get,, <url>                                         <-- legacy dme commands
            __________________________________
            function description:
                Get a SINGLE command within a maple action and translate them into an equivalent blitz action

            args:
                command: whether cmds commands, show command, legacy_dme command or plugin commands 
                         datatype: string if command == <show command> OR datatype: dict if cmds commands or plugin commands
                
                maple_action_type: type of maple_action whether it is (cli, dmerest, yangrest)
                                    datatype: string

                device: device that will actions executed on
                        datatype: string

                maple_action: confirm, apply, unapply
                              datatype: string

                rule_id: (optional) - the rule name for possible confirm action that will perform.
                         datatype: string

            returned_value: 
                type(dict): containing the blitz action equivalnet of each maple commands
                type(string): the blitz action name of the converted maple command
        '''

        # When stated as command, a plugin_type either can be of type matcher, or command
        plugin_type = 'command' if maple_action_type != 'matcher' else 'matcher' 

        # if type of maple_action is dmerest and if command is not a dictionary
        # which means that the command is not for a plugin but for a legacy dme
        # legacy dme ex: get,, http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json
        # the legacy dme needs to be translated into its plugins equivalent
        # so blitz would understand it
        if maple_action_type == 'dmerest' and not isinstance(command, dict):

            # dme legacy commands needs to be converted to maple plugins arguments first
            # a Legacy_DME_Converter object first created
            ldc = Legacy_DME_Converter(command, maple_action)

            # converting legacy_dme_to_maple_plugin
            # command -> plugins command -> dictionary
            command = ldc.legacy_dme_to_maple_plugin_converter()

        # if type of maple_action is smartman 
        # it means that the command should use a smartman cli
        # Blitz does not support smartman
        # Hence the smartman input should be converted into a smartman plugin
        # so blitz would understand it 
        elif maple_action_type == 'smartman':

            # smartman commands needs to be converted to maple plugins arguments first
            # a Legacy_Smartman_Converter object first created
            lsc =  Legacy_Smartman_Converter(command)

            # converting smartman_to_maple_plugin
            # command -> plugins command -> dictionary
            command = lsc.smartman_to_maple_plugin_converter()

        # If the command is a dictionary then it is either cmds command or plugins command
        if isinstance(command, dict):

            # These cmds= are in the group of maple commands, such as waitfor, runraw etc.
            # All these should be translated from cmds= to plugin and then translated into blitz_action
            # Exception is cmds=patterns that directly translates to a list of blitz_action
            if 'cmds=' in command['plugin']:

                # cmds= commands all need to be translated into a plugin first 
                # so blitz could understand it
                cmds_converter = CMDS_Converter(command['plugin'], maple_action_type)

                # converting cmds commands to maple 
                # command -> plugins command -> dictionary
                command =  cmds_converter.cmds_to_maple_plugin_converter()

                # There are two exceptions when translating cmds= commands to plugins cmds=patterns and cmds=eval
                # if the cmds=patterns (cmds= of type "patterns") then instead of translating it into a maple_plugins
                # we directly convert cmds=patterns into a dictionary containing a list of blitz actions
                # if maple action type is matcher and if cmds=pattrens
                if maple_action_type == 'matcher' and command.get('type') == 'patterns':
                    return cmds_converter.cmds_patterns_to_blitz_action_converter(command['data'], device), 'execute'
                
                if command.get('type') == 'groups':
                    return cmds_converter.cmds_groups_command_to_blitz_action_converter(command['data'], device), 'execute'

            # Whether if it is plugins commands the following function would convert it into a blitz action
            # if cmds= commands (with exception of two) they are already translated in maple plugins above
            # all of them now will be converted as maple plugin into an blitz action
            return self._plugin_to_blitz_action_converter(command, maple_action_type, device=device, maple_action=maple_action,
                                                          plugin_type=plugin_type, rule_id=rule_id), 'maple'

        # if command is not a dictionary then it is a show command 
        else:
            # Normal commands translation
            # if maple_action == apply, unapply | blitz_action action configure 
            # if maple_action == confirm | blitz action execute
            blitz_action = 'execute' if maple_action == 'confirm' else 'configure'

            # show commands translated into a blitz action
            return self._show_command_to_blitz_action_converter(command, device, blitz_action), blitz_action

    def _plugin_to_blitz_action_converter(self, command, maple_action_type,
                                          device=None, maple_action=None, plugin_type=None, rule_id=None):

        ''' 
            3 types of maple plugins exist: 
                1) confirm
                2) matcher
                3) command
            
            Example of converting maple plugins into equivalent blitz action
            apply:
                devices:
                    N93_3:
                        type: dmerest
                        commands: |
                            #@# command:{       <-- plugin_type  (command|matcher|confirm)
                                "method":"processdme",
                                "options":[
                                    {"method":"GET"},
                                    {"url":"http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json"}
                                ]} 
                            #@#
            ==================================================================================
            Blitz equivalent of the abovementioned command maple plugin
            - maple:
                # maple_plugin_input keyword below is section dict containing all the maple_action information and is input to blitz code  
                
                maple_plugin_input: '{"type": "dmerest", "commands":   < -- string representation of the dictionary representation of the maple_plugin with maple_action_type and rule_id for use in blitz
                            "command:{\n
                                \"method\":\"processdme\",\n
                                                \"options\":[\n
                                                            {\"method\":\"GET\"},\n
                                                            {\"url\":\"http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json\"}\n
                                                            ]}"}'
                
                device: N93_3
                maple_action: apply <-- necessary for blitz
                save:
                - variable_name: my_variable
                  append: true
                continue: false
            _______________________________________________
            Function description: This function convert a maple plugins into its blitz equivalent action

            args:
                command: maple plugins command as a dictionary
                    datatype: dictionary
                
                maple_action_type: type of maple action (dmerest, tgen-config, cli, etc)
                    datatype: string
                
                device: (Optional) unit under test
                    datatype: string
                
                maple_action: (Optional) (confirm apply/unapply)
                    datatype: string

                plugin_type: (matcher/confirm/command)
                    datatype: string
                
                rule_id: the rule_id that is used to separate confirm actions (Allowing to have multiple confirm actions)

            returned_value: 
                type(dict): containing the equivalent blitz action of the plugin command that is in the input
        '''
        # Plugins are translated into a blitz action called maple
        # specifically designed to handle maple plugins
        # the input of the maple are the json data representing
        # the maple section from the device to match/unmatch
        blitz_action_dict = {}

        # The #@# plugin command inputted from the user in the yaml file
        # would be stored as dictionary within this var
        maple_plugin_input = {}

        # Replacing all the XX(<var>)XX with its blitz equivalent %VARIABLES{<var>}
        command['plugin'] = Internal_Converter._XX_pattern_matching(command['plugin'].strip(), 'replace')

        # Creating the string representation of the of the command dictionary 
        # adding type and rule_id to it for future use within blitz code

        if rule_id:
            maple_plugin_input.update({rule_id: {'type': maple_action_type, 'commands': command['plugin'].strip(' ')}})
        else:
            maple_plugin_input.update({'type': maple_action_type, 'commands': command['plugin'].strip(' ')})
            if maple_action_type == 'tgen-config':
                maple_plugin_input.update({'type': 'cli' ,'chassis': 'IXIA'})

        # The maple_plugin_input needs to be cast to string 
        # as blitz maple action input 
        maple_plugin_input_in_str = json.dumps(maple_plugin_input)
        blitz_action_dict.update({'maple':{'maple_plugin_input':maple_plugin_input_in_str, 'device': device} })
        if plugin_type == 'command':

            blitz_action_dict['maple'].update({'maple_action': maple_action})

        return blitz_action_dict

    def _show_command_to_blitz_action_converter(self, command, device, blitz_action):

        ''' confirm maple action with regular show command convert to blitz action execute
            
            step-2:
                confirm:
                    devices:
                        N93_3:
                            rule-1:
                                type: cli
                                commands: |
                                    show vlan
        =============================================
            - execute:
                device: N93_3
                command: show vlan
        +++++++++++++++++++++++++++++++++++++++++++++
            apply maple action with regular show command convert to blitz action configure

            step-1:
                apply:
                    devices:
                        device{testbed.custom.devices.deviceA}:
                            type: cli
                            commands: |
                                conf t
                                feature bfd
            ======================================================
            - step-1:
              - configure:
                  device: device{testbed.custom.devices.deviceA}
                  command: "conf t\nfeature bfd\n"
                  save:
                  - variable_name: jemhwnbtyf
                    append: true
                  continue: false
            _______________________________________________
            returned_value: a dictionary containing the equivalent blitz action of the plugin command that is in the input
        '''

        # handle the normal commands with replacement ability
        # command such as : show module show version etc
        command = command.strip(' ')
        blitz_action_dict = {}
        command = Internal_Converter._XX_pattern_matching(command, 'replace')
        
        # if maple_action apply/unapply blitz_action configure
        # if confirm blitz_action execute
        blitz_action_dict.update({blitz_action: {'device': device, 'command': command,
                                         'save': [{'variable_name': ''}]}})

        return blitz_action_dict

    def _match_unmatch_dispatcher(self, blitz_action_dict, maple_action, maple_action_type,
                                  rule_id, device=None, match=None,
                                  unmatch=None, val_to_search=None, val_to_search_apply=None):

        """

        function description:  This function simply dispatch match/unmatch cases to the converter function

        args: 
            blitz_action_dict: match/unmatch will add an action to the previous blitz_action_dict which has already a maple/execute/configure action in it
            maple_action: confirm/apply/unapply
            maple_action_type: (dmerest/cli/tgen-config etc.)
            rule_id: confirm action rule_id
            device: device name
            match: all the values that should be found the actions output
            unmatch: all the values that shouldn't be found the actions output
            val_to_search: variable to store the output of a confirm action and pass it to be searched for match/unmatchs
            val_to_search_apply: variable to store the output of an apply action and pass it to be searched for match/unmatchs

        returned_value: dictionary value containing the equivalent action of match/unmatch in blitz
        """

        if not match and not unmatch:
            return blitz_action_dict

        _include_list = Internal_Converter._command_separator(match) if match else []
        _exclude_list = Internal_Converter._command_separator(unmatch) if unmatch else []

        blitz_action_dict = self.match_unmatch_converter('include', blitz_action_dict, 
                                                  maple_action_type, rule_id, device, 
                                                  _include_list, val_to_search, val_to_search_apply)
        blitz_action_dict = self.match_unmatch_converter('exclude', blitz_action_dict,
                                                  maple_action_type, rule_id, device,\
                                                  _exclude_list, val_to_search, val_to_search_apply)

        return blitz_action_dict

    def match_unmatch_converter(self, style, blitz_action_dict, maple_action_type, rule_id, device=None,\
                                _match_unmatch_list=None, val_to_search=None, val_to_search_apply=None):

        '''
            Explanation: 
                1) if the match/unmatch values are simple values or regex then the blitz_action_dict contains already converted 
                   maple actions. The output of those blitz actions are saved into val_to_search variable, and in this function
                   a maple_search would be created that would query that val_to_search variable.
                
                2)If the match/unmatch is confirm plugins, the input would convert into a blitz maple action to call the plugins 
                  from the blitz code

                3)If the input is a cmds=eval then an arithmetic/logical statement is in the input. Blitz action compare is 
                  the equivalent of this cmds= command 

            EX-1)
            confirm:
                devices:
                    N93_3:
                        rule-1:
                            type: cli
                            commands: |
                                show vdc
                                show vrf
                            match: |
                                .*
                                UP
            ==============================
            - execute:
                device: N93_3
                command: show vdc
                save:
                - variable_name: rule-1_match_unmatch
                  append: true
              execute:
                device: N93_3
                command: show vrf
                save: 
                 - variable_name: rule-1_match_unmatch
                   append: true 
              maple_search:
                search_string: '%VARIABLES{rule-1_match_unmatch}'
                device: N93_3
                include:
                - .*
                - UP

            EX-2)
            step-2:
                confirm:
                    devices:
                        N93_3:
                            rule-1:
                                type: cli
                                commands: |
                                    show module
                                match: |
                                    #@# confirm:{
                                        "package":"maple.plugins.user.ConfirmPlugins",
                                        "method":"checkIfPresent",
                                        "options":[
                                            {"count":"1"},
                                            {"check1": "XX(dummy_key_name)XX"}
                                        ]}
                                    #@#
            ====================================================
            - step-2:
              - execute:
                  command: show module
                  continue: false
                  device: N93_3
                  save:
                  - append: true
                    variable_name: rule-1_match_unmatch
                maple:
                  device: N93_3
                  output: '%VARIABLES{rule-1_match_unmatch}'
                  section: '{"rule-1": {"type": "cli", "commands": "confirm:{\n    \"package\":\"maple.plugins.user.ConfirmPlugins\",\n    \"method\":\"checkIfPresent\",\n    \"options\":[\n        {\"count\":\"1\"},\n        {\"check1\":
                    \"%VARIABLES{dummy_key_name}\"}\n    ]}"}}'

            EX-3)
            step-2-get:
                confirm:
                    devices:
                        N93_3:
                            rule-1:
                                type: dmerest
                                commands: |
                                    #@# command:{
                                        "method":"processdme",
                                        "options":[
                                            {"method":"GET"},
                                            {"url":"http://acjain-laas:8001/api/node/mo/sys/ldp.json"}
                                        ]} 
                                    #@#
                                match: |
                                    #@# cmds=eval:::'XX(adminSt)XX' == 'enabled' #@# 
                ======================================================
            - step-2-get:
              - continue: false
              - maple:
                  section: '{"rule-1": {"type": "dmerest", "commands": "command:{\n    \"method\":\"processdme\",\n    \"options\":[\n        {\"method\":\"GET\"},\n        {\"url\":\"http://acjain-laas:8001/api/node/mo/sys/ldp.json\"}\n    ]}"}}'
                  device: N93_3
                  save:
                  - variable_name: rule-1_match_unmatch
                    append: true
                  continue: false
                compare:
                  items:
                  - "'%VARIABLES{adminSt}' == 'enabled'"
        ____________________
        args:
            blitz_action_dict: match/unmatch will add an action to the previous blitz_action_dict which has already a maple/execute/configure action in it
            maple_action: confirm/apply/unapply
            maple_action_type: (dmerest/cli/tgen-config etc.)
            rule_id: confirm action rule_id
            device: device name
            _match_unmatch_list: list containing the values that would be used for checking their inclusion/exclusion
            val_to_search: variable to store the output of a confirm action and pass it to be searched for match/unmatchs
            val_to_search_apply: variable to store the output of an apply action and pass it to be searched for match/unmatchs

        returned_value: dictionary value containing the equivalent action of match/unmatch in blitz
        ''' 

        storage_list = []
        if not _match_unmatch_list:
            return blitz_action_dict

        # TODO : Fix the - not showing in yaml file (the fix should be done somewhere here)
        # val_to_search is to search the output of a confirm section 
        # (bunch of show commands output that are appended together are stored in val_to_search)
        # val_to_search has priority over val_to_search_apply
        # that means if val_to_search is there val_to_search_apply will be ignored
        # val_to_search_apply for checking the include/exclude for outputs of the apply section (could be equivalent of multiple actions in blitz)
        # This only applies when confirm section doesn't exist
        if val_to_search:
            blitz_action_dict.update({'maple_search':{'search_string': "%VARIABLES{}".format('{'+val_to_search+'}'), 'device': device}})
        elif val_to_search_apply:
            blitz_action_dict.update({'maple_search':{'search_string': "%VARIABLES{}".format('{'+val_to_search_apply+'}'), 'device': device}})

        for item in _match_unmatch_list:
            if isinstance(item, dict):


                # if in cmds=eval::: then it is an arithmatic/logical operation
                # mapped to action compare in blitz
                if 'cmds=' in item['plugin']:

                    cmds_converter = CMDS_Converter(item['plugin'], maple_action_type)
                    # converting cmds commands to maple
                    # command -> plugins command -> dictionary
                    command =  cmds_converter.cmds_to_maple_plugin_converter()

                    # if cmds= then it is surely cmds=eval and it is a compare scenario
                    if command.get('type') == 'eval':
                        plugin_dict = cmds_converter.cmds_eval_to_blitz_action_converter(command['data'])

                    elif command.get('type') == 'groups':
                        plugin_dict = cmds_converter.cmds_groups_match_to_blitz_action(command['data'])

                    blitz_action_dict.update(plugin_dict)
                else:
                    # if it is a plugin it would ba confirm plugin_type which will be a maple action
                    plugin_dict = self._plugin_to_blitz_action_converter(item, maple_action_type , device=device, plugin_type='confirm', rule_id=rule_id)

                    if blitz_action_dict and val_to_search:
                        # if previously an action execute exist on this match/unmatch
                        # The output of that action execute needs to be stored for the
                        # maple action further use
                        plugin_dict['maple'].update({'output': "%VARIABLES{}".format('{'+val_to_search+'}')})

                    blitz_action_dict.update(plugin_dict)
            else:
                # This variable will put all the item whether int/boolean/str
                # in the double quote, which is necessary to not face any issue 
                # in Blitz
                double_quote = ruamel.yaml.scalarstring.DoubleQuotedScalarString
                storage_list.append(double_quote(item))
                blitz_action_dict['maple_search'].update({style: storage_list})

        # if include/exclude added to maple_search there is no point of having the maple_search in the output
        if 'maple_search' in blitz_action_dict:
            if 'include' not in blitz_action_dict['maple_search'] and 'exclude' not in blitz_action_dict['maple_search']:
                blitz_action_dict.pop('maple_search')

        return blitz_action_dict


# IF YOU WANT TO ONLY CONVERT TWO SCRIPTS
# SIMPLY CALL THE CONVERTOR FUNCTION WITH 
# THE NAME OF YOUR TESTSCRIPT AS AN ARGS

# converter = Converter('groups.yaml')
# # converter = Converter('anycast_testcase.yaml')

# trigger_uids = converter.convert()
