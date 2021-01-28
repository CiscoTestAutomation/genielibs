import re
import os
import sys
import json
import logging
import requests
import xmltodict
import ruamel.yaml

from ats.easypy import runtime

#genie
from genie.utils import Dq
from genie.testbed import load

TIMS_URL = 'http://tims.cisco.com/xml/{}/entity-list.svc'
log = logging.getLogger(__name__)


###################################################
#                                                 #
#                Pre-Job checks                   #
#                                                 #
###################################################

def verify_maple_env():

    '''
    Function description: Verifies whether the maple environment is exported into path
    '''

    if 'MAPLE_PATH' not in os.environ:
        raise Exception('Make sure to set MAPLE_PATH before running your '
                        'mpale script in the converter')

    if os.environ['MAPLE_PATH'] not in sys.path:
        sys.path.append(os.environ['MAPLE_PATH'])

def replace_maple_markups(maple_string, testbed):
    '''Replace maple markups pre running the test '''

    maple_string = _maple_markup_devices(maple_string, testbed)
    maple_string = _maple_markup_variables(maple_string, testbed)
    return maple_string

def _maple_markup_devices(maple_data, testbed):

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
            testbed_info = _testbed_info_gen(key_orig, testbed)

            if testbed_info is not None:
                maple_data = maple_data.replace(name,str(testbed_info))

    return maple_data

def _maple_markup_variables(maple_data, testbed):

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
            testbed_info = _testbed_info_gen(key_orig, testbed)
            # TODO comment this section

            if testbed_info is not None:
                maple_data = maple_data.replace(name,str(testbed_info))
            else:
                if os.environ.get(key_orig) is not None:
                    maple_data = maple_data.replace(name,os.environ.get(key_orig))

    return maple_data

def _testbed_info_gen(key_orig, testbed):

    # TODO - Comment this out debug the code

    '''
        This is a helper function for markup replace
        parse the testbed to the point of the exact path to the value

    '''
    key = key_orig.replace('topology.links','testbed.links')
    tree_keys = key.split('.')
    testbed_info = testbed
    for tree_key in tree_keys:
        testbed_info = _get_value_to_replace(tree_key, testbed_info)

    return testbed_info

def _get_value_to_replace(key, obj):

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

###################################################
#                                                 #
#                Pre-testcase checks              #
#                                                 #
###################################################

def pre_testcase_checks(maple_testcase_data,
                        testcase_control,
                        teststep_control,
                        tims_testplan_folder):

    '''
    info that will extracted pre running a maple testcase, such as log or tims logical id
    and added to the blitz testcase info, such as log processor and tims case_id
    '''
    blitz_pre_tc_data = {}
    # Log collection - Check if log collection is there
    # For blitz - it is a post-processor
    log_processor = maple_testcase_data.pop('log', None)

    # logical id that is used to store testcase result into TIMS
    tims_logical_id = maple_testcase_data.pop('logical_id', None)

    # setting continue value for each section in blitz
    # the value can be assigned from testsuite using testcase_control keyword
    if testcase_control:
        section_continue = testcase_control

    # if not specified there look for the equivalent in the testcase,
    # otherwise None
    else:
        section_continue = maple_testcase_data.pop('testcase_control', None)

    # setting  continue value for each action in blitz
    # since in maple this value is generated in the step level
    # The value should be passed out further to other function that creates
    # blitz actions to add the keyword to their dictionary
    # the value can be assigned from testsuite using teststep_control keyword
    if teststep_control:
        action_continue = teststep_control

    # if not specified there look for the equivalent in the testcase,
    # otherwise None
    else:
        action_continue = maple_testcase_data.pop('teststep_control', None)

    # Extracting log collection data and translating it into processor
    if log_processor:
        blitz_pre_tc_data.update(_log_converter(log_processor))

    if tims_logical_id and 'tims_rest' in runtime.args:

        try:
            case_id = _generate_tims_case_id(tims_logical_id,\
                                             tims_testplan_folder)
        except Exception as e:
            runtime.args.tims_rest = False
            log.error(str(e))
        else:
            blitz_pre_tc_data.update({'tims': {'case_id': case_id}})

    return { 'blitz_pre_tc_data': blitz_pre_tc_data,
             'section_cont': section_continue,
             'action_cont': action_continue }

def _log_converter(log_processor):

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

def _generate_tims_case_id(logical_id, tims_testplan_folder):
    '''
    A tims case_id would link the uploaded results to the previously uploaded
    testcases that are already residing in TIMS. This function generates the
    case_id based on testcase logical_id
    '''

    if not tims_testplan_folder:
        raise Exception("Tims testplan folder in not provided.")
    folder_xml_data = requests.get(TIMS_URL.\
                                   format(tims_testplan_folder))

    folder_json_data = xmltodict.parse(folder_xml_data.text)
    data_dq = Dq(folder_json_data)
    dict_of_test_cases = data_dq.contains('Case').\
                         contains('@docID|LogicalID', regex=True).reconstruct()

    list_of_test_cases = dict_of_test_cases['Tims']['Case']
    for case in list_of_test_cases:
        if logical_id in case['LogicalID']:
            return case['@docID']

###################################################
#                                                 #
#                Pre-Section checks               #
#                                                 #
###################################################

def pre_section_checks(maple_action, data, blitz_action_list, loop):

    # Function to add the condition as a blitz action
    # reminder: section_control action is the equivalent of
    # flowcontrol in blitz
    if maple_action == 'flowcontrol':
        blitz_action_list.append(_flow_control_converter(data))

    # Function adjust the the layout of the dictionary of a blitz section
    # So blitz would have a loop keyword on top
    if maple_action == 'loop':
        blitz_action_list.append(_loop_converter(data))
        loop = True

    return blitz_action_list, loop

def _flow_control_converter(data):

    dict_vals = {}

    # %VARIABLES{}
    data_json = json.loads(data)
    if  'XX(' in data_json['condition'] and\
        ')XX' in data_json['condition']:
        data_json['condition'] = _XX_pattern_matching(data_json['condition'], 'replace')

    # Make it simpler with adding ed to the end.
    if data_json['action'] == 'skip':
        data_json['action'] = 'skipped'
    else:
        data_json['action'] = data_json['action'] + 'ed'

    dict_vals.update({'section_control':{
                            'if': data_json['condition'],
                            'function': data_json['action']}})
    return dict_vals

def _loop_converter(maple_data):

    # Extracting the loop from maple code and changing the section layout
    # To have loop on top of all the other actions
    dict_vals = {}

    p = re.compile(r'{(?P<loop_plugin>[\S\s]+)}')
    m = p.match(maple_data)
    section = '{' + m.group(1) + '}'
    dict_vals.update({'loop':{'maple': True, 'section': section}})

    return dict_vals

###################################################
#                                                 #
#        Helper functions for converters          #
#                                                 #
###################################################

def plugin_to_blitz_action_converter(command, maple_action_type,
                                     device=None, maple_action=None,
                                     plugin_type=None, rule_id=None):

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
    command['plugin'] = _XX_pattern_matching(command['plugin'].strip(), 'replace')
    # Creating the string representation of the of the command dictionary
    # adding type and rule_id to it for future use within blitz code

    if rule_id:
        maple_plugin_input.update({rule_id:
                                     {'type': maple_action_type,
                                      'commands': command['plugin'].strip(' ')}})
    else:
        maple_plugin_input.update({'type': maple_action_type,
                                   'commands': command['plugin'].strip(' ')})

        if maple_action_type == 'tgen-config':
            maple_plugin_input.update({'type': 'cli' ,'chassis': 'IXIA'})

    # The maple_plugin_input needs to be cast to string
    # as blitz maple action input
    maple_plugin_input_in_str = json.dumps(maple_plugin_input)
    blitz_action_dict.update({'maple':
                                {'maple_plugin_input':maple_plugin_input_in_str,
                                 'device': device} })

    if plugin_type == 'command':

        blitz_action_dict['maple'].update({'maple_action': maple_action})

    return blitz_action_dict

def show_command_to_blitz_action_converter(command, device, blitz_action):
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
    command = _XX_pattern_matching(command, 'replace')

    # if maple_action apply/unapply blitz_action configure
    # if confirm blitz_action execute
    blitz_action_dict.update({blitz_action: {'device': device, 'command': command}})

    return blitz_action_dict

def _command_separator(commands, dmerest=False, configure=False):

    """
    Example of inputs in confirm section:
        commands: |
            show module                                         <-- Show command
            #@# cmds=waitfor:::show module,,Up,,10 #@#          <-- cmds= command
            #@# matcher:{
                "package":"maple.plugins.user.MatcherPlugins",  <-- plugin command
                "method":"populateObjects",
                "command":"show version",
                "type":"cli"
                }
            #@#

    Example of output:
    ['show module', {'plugin': ' cmds=waitfor:::show module,,Up,,10 '},
    {'plugin': ' matcher:{\n    "package":"maple.plugins.user.MatcherPlugins",\n    "method":"populateObjects",\n    "command":"show version",\n    "type":"cli"\n    }    \n'}]

    ===========================================================================
    Example of inputs in apply section:
    commands: |
        conf t
        feature bfd
        feature telnet
        #@# cmds=waitfor:::show vlan,,Up,,9 #@#
        #@# cmds=switchback: #@#

    Example of output:
    ['conf t\nfeature bfd\nfeature telnet\n', {'plugin': ' cmds=waitfor:::show vlan,,Up,,9 '}, {'plugin': ' cmds=switchback: '}]
    _______________________________________________________
    Function description:
        handles whether a command is show commands, plugins or cmds=,
        it just extract the commands, and returns them in a readable format
        and keeps the order within a list to be parsed later on

    args:
        commands: a group of commands as shown in the example of inputs
        dmerest: flag to see if the input has maple_action_type dmerest
        configure: flag to see if the maple action is configure

    returned_value: a list containing the commands with order.
                    cmds=, and plugins are transformed into a dictionary type
    """

    # This value is defined because config commands should be appended together
    # despite normal show commands that gets them broken down to a single command
    append_config_commands = ''

    ret_list = []
    pattern_plugin = re.compile(r'#@#(?P<plugin>[\S\s]+?)#@#')

    all_match_plugins = re.finditer(pattern_plugin, commands)
    show_commands = commands

        # check if there is any = or plugin and extract it from original input
    for each_match in all_match_plugins:

        matched_string = each_match.group(0)
        group = each_match.groupdict()

        # replace the plugins input with its dictonary equivalent
        # within the commands
        # the equivalent is created as the result of
        # after pattern matching
        group_in_str = json.dumps(group)
        show_commands = show_commands.replace(matched_string , group_in_str)

    # splitting the command by line
    for command in show_commands.split('\n'):
        # if after split and stripping spaces
        # the command is empty continue
        command = command.strip()
        if not command:
            continue

        try:
        # attempt to create the dict object of the command
        # if it happens, then we have a plugin

            command = json.loads(command)

            # if append_config commands exist and we are about to append a plugin
            # first we need to append all the previous append_config_commands
            if append_config_commands:
                ret_list.append(append_config_commands)
                append_config_commands = ''

            # append the plugin command to the reutrn list
            ret_list.append(command)

        except Exception:
        # if exception happen then we have a show command (show version, feature telnet etc.)

            # if maple_action is apply and the input is not
            # legacy dmerest then append every show command to one line
            if configure and not dmerest:
                append_config_commands += command + '\n'
            else:
                # append to the return list
                ret_list.append(command)

    if append_config_commands:
        ret_list.append(append_config_commands)

    return ret_list

def _XX_pattern_matching(val, XX_type):

        # XX is used to save/replace variables in command!
    pattern_XX = re.compile(r'XX\(([\S\s]+?)\)XX')
    matches_XX = re.finditer(pattern_XX, str(val))

    for match in matches_XX:
        variable_name = match.group(1)
        if XX_type == 'save':
            save_var_name_regx = '?P<{}>'.format(variable_name)
            val = val.replace(match.group(0)+'(', '({}'.format(save_var_name_regx))
        elif XX_type == 'replace':
            save_var_name_regx = "%VARIABLES{}".format('{'+variable_name+'}')
            val = val.replace(match.group(0), '{}'.format(save_var_name_regx))

    return val

def _XR_pattern_matching(val):

    # XR used to replace values in cmds=patterns::: only!
    pattern_XR = re.compile(r'XR\(([\S\s]+?)\)XR')
    matches_XR = re.findall(pattern_XR, str(val))
    if matches_XR:
        val = re.sub(r'\bXR\b', 'XX', str(val))
        return _XX_pattern_matching(val, 'replace')

    return val
