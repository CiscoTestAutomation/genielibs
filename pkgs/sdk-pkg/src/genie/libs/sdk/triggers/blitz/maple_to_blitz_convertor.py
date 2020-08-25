import os
import re
import sys
import yaml
import json
import random
import string
import ruamel.yaml
from ats.easypy import runtime

# Collect uids since maple does not support groups all the triggers needs trigger uids.
uids = []

def get_value(key, obj):
    #log.debug('Performing get_value for key: %s, obj: %s type: %s' % (key, obj, type(obj).__name__))

    #Skip 'testbed' for Testbed object, return the object itself
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

def _testbed_info_gen(key_orig, testbed):

    key = key_orig.replace('topology.links','testbed.links')
    tree_keys = key.split('.')
    testbed_info = testbed
    for tree_key in tree_keys:
        testbed_info = get_value(tree_key, testbed_info)

    return testbed_info

def _data_ref_check(data):

    testbed = runtime.testbed

    if data is not None:

        #log.debug('[do_reference_cleanup] after do_device_cleanup\n %s\n' % data)
        referenece_names = re.findall(r'%\{[\w._\-\/]+\}', data)
        #log.debug('[do_reference_cleanup] findall: %s' % referenece_names)
        for name in referenece_names:
            key_orig = name.replace('%{','').replace('}','')

            #Replace topology.links with testbed.links
            testbed_info = _testbed_info_gen(key_orig, testbed)

            if testbed_info is not None:
                data = data.replace(name,str(testbed_info))
            else:
                if os.environ.get(key_orig) is not None:
                    data = data.replace(name,os.environ.get(key_orig))
    return data

def _data_ref_dev_check(data):

    testbed = runtime.testbed
 
    if data is not None:
        device_names = re.findall(r'device\{[\w._\/]+\}', str(data))
        #log.debug('[do_device_cleanup] findall: %s' % device_names)

        for name in device_names:
            key_orig = name.replace('device{','').replace('}','')
            #Replace topology.links with testbed.links
            testbed_info = _testbed_info_gen(key_orig, testbed)
            if testbed_info is not None:
                #log.debug('[do_device_cleanup] replacing %s with %s' % (name,testbed_info))
                data = data.replace(name,str(testbed_info))

    return data

def converter(maple_file):

    blitz_datafile_dict = {}

    if 'MAPLE_PATH' not in os.environ:
        raise Exception('Make sure to set MAPLE_PATH before running your '
                        'mpale script in the converter')

    if os.environ['MAPLE_PATH'] not in sys.path:
        sys.path.append(os.environ['MAPLE_PATH'])

    with open(maple_file, 'r') as tempfile:
        tempfile_text = tempfile.read()
        tempfile_text = _data_ref_dev_check(tempfile_text)
        tempfile_text = _data_ref_check(tempfile_text)
        maple_file_dict = ruamel.yaml.safe_load(tempfile_text)

    for blitz_test_name in maple_file_dict['tests'].keys():
        # multiple tests might exists within a maple testcase, and they all need to be extracted one by one
        uids.append(blitz_test_name)
        blitz_datafile_dict = _convertor(maple_file_dict['tests'][blitz_test_name],
                                         blitz_test_name, blitz_datafile_dict)

    blitz_file_name = 'blitz_' + maple_file
    with open(blitz_file_name, 'w') as blitz_file:
        blitz_file.write(ruamel.yaml.round_trip_dump(blitz_datafile_dict))

    return '/{}'.format(blitz_file_name)

def get_uids():
    return uids

def _convertor(maple_test, blitz_test_name, blitz_datafile_dict):

    log_processor = maple_test.pop('log', None)

    section_continue = maple_test.pop('testcase_control', None)
    continue_ = maple_test.pop('teststep_control', None)
    source_dict = {}
    section_list = []

    # Extracting log collection data and translating it into processor
    if log_processor:
        source_dict = _log_extract(source_dict, log_processor)

    # Each test would be map to one test in blitz and they all need source and class
    source_dict.update({'source':
                       {'pkg': 'genie.libs.sdk',
                        'class': 'triggers.blitz.blitz.Blitz'},
                        'test_sections' : section_list})

    blitz_datafile_dict.update({blitz_test_name: source_dict})

    # Maple steps are technically sections in blitz. 
    # In blitz section are build on various actions,
    # Major actions in maple are confirm, apply and unapply,
    # which translates to various actions in blitz.
    if 'test-steps' not in maple_test:

        if  'confirm' in maple_test.keys() or\
            'apply' in maple_test.keys() or\
            'unapply' in maple_test.keys() :

            maple_test = {'test-steps': {'step-1':maple_test}}
        else:
            {'test-steps': maple_test}

    for section, action in maple_test['test-steps'].items():
        action_list = []
        if section_continue and section_continue == 'abort-on-failure' and not action_list:
            action_list.append({'continue': False})

        section_dict = {section: action_list}
        section_list.append(section_dict)
        action_list = _action_level_distributer(action, action_list, continue_)

    return blitz_datafile_dict

def _action_level_distributer(action_dict, section_list, continue_):

    loop = False
    val_to_search_apply = None
    # Check whether a maple action is confirm or apply/unapply
    for action, data in action_dict.items():

        if action == 'flowcontrol':
            section_list = _control_extract(data, section_list)

        if action == 'loop':
            section_list = _loop_extract(data, section_list)
            loop = True 

        if action == 'apply' or action == 'unapply':
            section_list, val_to_search_apply = _action_level_apply_unapply(data,
                                                                            section_list,
                                                                            continue_,
                                                                            action,
                                                                            loop)
        if action == 'confirm':
            section_list = _action_level_confirm(data, section_list, continue_, loop, val_to_search_apply)

    return section_list

def _log_extract(source_dict, log_processor):

    # Extract the log collection input and mapping it into a preprocessor
    valid_section_results = log_processor['states'].split(',')
    devices = log_processor['devices'].strip(' ').split(',')
    log_commands = log_processor['commands'].split('\n')

    for cmd in log_commands:
        
        i = log_commands.index(cmd)
        if  cmd:     
            log_commands[i] = {'cmd': cmd}
        else:
            log_commands.pop(i)
    if 'server' in log_processor:
        server_info_list = log_processor['server'].split(',')

    source_dict.update({'processors': {'post':{'post_execute_command':
                          {'method':'genie.libs.sdk.libs.abstracted_libs.post_execute_command',
                           'parameters':{'zipped_folder': False, 'save_to_file':'per_command',
                           'valid_section_results': valid_section_results,
                           'server_to_store':{
                               "server_in_testbed": server_info_list[0],
                               'protocol': server_info_list[1],
                               'remote_path':server_info_list[2]
                           }}}}}})

    for device in devices:
        device = device.strip(' ')
        source_dict['processors']['post']['post_execute_command']['parameters'].update({'devices':{device:{}}})
        source_dict['processors']['post']['post_execute_command']['parameters']['devices'][device].update({'cmds':log_commands})

    return source_dict

def _control_extract(data, section_list):

    dict_vals = {}

    data_json = json.loads(data) 
    if  'XX(' in data_json['condition'] and\
        ')XX' in data_json['condition']:

        data_json['condition'] = _XX_pattern_matching(data_json['condition'], 'replace')
    
    if data_json['action'] == 'skip':
        data_json['action'] = 'skipped'
    elif data_json['action'] == 'block':
        data_json['action'] = 'blocked'
    elif data_json['action'] == 'error':
        data_json['action'] = 'errored'
    elif data_json['action'] == 'abort':
        data_json['action'] = 'aborted'
    elif data_json['action'] == 'fail':
        data_json['action'] = 'failed'
    elif data_json['action'] == 'pass':
        data_json['action'] = 'passed'

    dict_vals.update({'section_control':{'if': data_json['condition'],
                      'function': data_json['action']}})
    section_list.append(dict_vals)

    return section_list

def _loop_extract(data, section_list):

    # Extracting the loop from maple code and changing the section layout
    # To have loop on top of all the other actions
    dict_vals = {}
    p = re.compile(r'{(?P<loop_plugin>[\S\s]+)}')
    m = p.match(data)
    section = '{' + m.group(1) + '}'
    dict_vals.update({'loop':{'maple': True, 'section': section}})
    section_list.append(dict_vals)

    return section_list

def _action_level_apply_unapply(data, section_list, continue_, section, loop=None):

    for dev in data['devices'].keys():

        # For IXIA legacy option connection was automatic but for plugins its manual
        # Then we need to connect it in plugins and since we translate legacy mode to
        # Plugins I need to add a connect on top of each IXIA legacy command
        if data['devices'][dev]['type'] == 'tgen-config':

            connect = '#@# cmds=connect: #@#                  \n'
            commands_actually = data['devices'][dev]['commands']
            data['devices'][dev]['commands'] = connect + commands_actually

        # Apply/unapply Commands are either raw commands 
        # (e.g show version, show clock, show interface)
        # OR they are CommandPlugins that are technically 
        # python codes developed by maple users to perform various commands
        # They need to be handled in the same order as they are inputted
        dmerest = True if data['devices'][dev]['type'] == 'dmerest' else False

        command_type_list =_command_handler(data['devices'][dev]['commands'], dmerest=dmerest, configure=True)

        letters = string.ascii_lowercase
        val_to_search_apply = ''.join(random.choice(letters) for i in range(10))

        for command in command_type_list:
            dict_vals, action = _command_translator(data['devices'][dev]['type'],\
                                                    command, data['devices'][dev],\
                                                    dev, section_list, section)
            # This is hacky :-(
            # There is sometimes a need to match/umatch the output of a apply/configure action
            # Since match/unmatch would always be done in confirm section, we need to store that value
            # and send to confirm section so in case there is no commands, code performs match/unmatch
            if action == 'configure':
                dict_vals[action].update({'save': [{'variable_name': val_to_search_apply, 'append': True}]})

            if not continue_ or continue_ != 'continue-on-failure':
                dict_vals[action].update({'continue': False})

            if loop:
                if 'actions' not in section_list[0]['loop']: 
                    section_list[0]['loop'].update({'actions':[dict_vals]})
                else:
                    section_list[0]['loop']['actions'].append(dict_vals)
            else:
                section_list.append(dict_vals)

    return section_list, val_to_search_apply

def _action_level_confirm(data, section_list, continue_, loop=None, val_to_search_apply=None):

    # check device name, for patterns like device{testbed.devices.<name>}
    search = False

    for dev in data['devices'].keys():
        for rule_id, rule_data in data['devices'][dev].items():

            # action confirms does have one more level called rule.
            # rules contains commands, and match/unmatch section, and the existance is and or or
            # which means there could be all of the together but there might be only match some times

            # There might be confirm actions with not commands
            # Uses for cmds=eval which in turn === action compare in blitz
            # OR uses for match/unmatch an apply action
            # val_to_search_apply has use for that
            if 'commands' not in rule_data:
                dict_vals = {}
                dict_vals = _match_unmatch(dict_vals, 'compare', 'confirm', rule_data['type'],\
                                           rule_id, device=dev, match=rule_data.get('match'), \
                                           unmatch=rule_data.get('unmatch'), val_to_search_apply=val_to_search_apply)
                section_list.append(dict_vals)
                continue

            # command_handler extract each command from the list of inputted
            # commands and returns them in a list. 3 types of commands exist in a confirm action
            # Normal as ('show_version', 'show interface'), 
            # Plugin commands that are python function as ('commandplugins' and 'matcherplugins'),
            # pattern matching commands that as (#cmds=patterns:::)
            command_type_list = _command_handler(rule_data['commands'])
            # function to translate cmds patterns to blitz equivalent
            # then it is arithmatic match
            val_to_search = rule_id + '_match_unmatch'
            
            for command in command_type_list:
                
                # command_translator gets each command, and based on their type (normal command or plugins)
                # returns the type of action(s) that would be executed in blitz 
                # and the dictionary representation of the action and its arguments
                dict_vals, action = _command_translator(rule_data['type'],
                                                        command, data['devices'][dev], dev, section_list, 'confirm', rule_id)

                if rule_data.get('match') or rule_data.get('unmatch'):

                    search = True
                    if loop:
                        dict_vals[action].update({'save': [{'variable_name': val_to_search}]})
                    else:
                        dict_vals[action].update({'save': [{'variable_name': val_to_search, 'append': True}]})

                if not continue_ or continue_ != 'continue-on-failure':
                    try:
                        dict_vals[action].update({'continue': False})
                    except KeyError:

                        # for cmds=patterns the output would be a dictionary of
                        # multiple blitz actions that is saved into a list
                        # It is necessary to update all those actions one by one
                        if "specifically_patterns" in dict_vals:
                            dict_vals.update({action:{'continue': False}})
                if loop:

                    if 'actions' not in section_list[0]['loop']: 
                        section_list[0]['loop'].update({'actions':[dict_vals]})
                    else:
                        section_list[0]['loop']['actions'].append(dict_vals)
                else:
                    if "specifically_patterns" in dict_vals:
                        cont_ = dict_vals.pop(action, None)
                        for item in dict_vals['specifically_patterns']:
                            if cont_:
                                item[action].update({'continue': False})
                            section_list.append(item)
                    else:
                        section_list.append(dict_vals)

            # in case match/unmatch exist, a map should be constructed
            # between match/unmatch to include/exclude
            # and the blitz action dictionary will be updated
            # match/unmatch might not always map to include exclude,
            # they can be mapped to an equivalent action in blitz
            if search:
                dict_vals = _match_unmatch(dict_vals, 'maple_search', 'confirm', rule_data['type'],
                                           rule_id, device=dev, match=rule_data.get('match'),
                                           unmatch=rule_data.get('unmatch'), val_to_search=val_to_search)

    return section_list

def _command_translator( _type, command, device_section, device, section_list, section, rule_id=None):

    # maple actions are categorized on another level named type
    # types could be matcher, cli, dmerest, yangrest, ixia etc.
    # type matcher either support pattern matching --> ('cmds=patterns:::')
    # OR it support MatcherPlugins
    # matcher is always in the confirm section
    if _type == 'matcher':
        if section != 'confirm':
            raise Exception('Type matcher only works in confrim maple section')
        
        if 'plugin' in command:
            if 'cmds=' in command['plugin']:
                # in matcher cmds=patterns is always the action equivalent in blitz
                # action = 'execute'
                return _cmds_translate(command['plugin'].strip(' '), _type, device=device, section=section, plugin_type='matcher', rule_id=rule_id), 'execute'

            else:
                # All the plugins always actions ample
                # action = 'maple'
                return _plugin_command_translate(command, _type, device=device, plugin_type='matcher', rule_id=rule_id), 'maple'
    
    elif _type == 'dmerest':

        if not isinstance(command, dict):
            return _legacy_dme_translator(command, section, _type, device), 'maple'

        # action = 'maple'
        return _plugin_command_translate(command, _type, device=device, plugin_type='dmerest', rule_id=rule_id), 'maple'

    elif _type == 'smartman':
        return _smartman_to_plugin_translator(command, _type, device=device, section=section, plugin_type='command', rule_id=rule_id), 'maple'

    # Cli implementation and yangrest, tgen-config, nxapi etc.
    else:
        if isinstance(command, dict):

            # These cmds= are in the group of maple commands, such as waitfor, runraw etc.
            # All these would be translated from command to plugin as a result action maple
            # action = 'maple'
            if 'cmds=' in command['plugin']:
                return _cmds_translate(command['plugin'].strip(' '), _type, device=device, section=section, plugin_type='command', rule_id=rule_id), 'maple'

            else:
                # Command plugins translation
                return _plugin_command_translate(command, _type, device=device, section=section, plugin_type='command', rule_id=rule_id), 'maple'
        else:
            # Normal commands translation
            # action execute or configure
            action = 'execute' if section == 'confirm' else 'configure'
            return _hardcoded_command_translate(section_list, command, device, action), action

def _legacy_dme_translator(command, section_type, console_type, device, rule_id=None):

    # post and put DME calls are in apply
    # delete DME call comes in unapply 
    # get DME call comes in confirm section

    command_list = command.split(',,')
    method = command_list[0]
    command_list[0] = '{{"method":"{}"}},\n'.format(command_list[0].upper())
    command_list[1] = '{{"url":"{}"}},\n'.format(command_list[1])

    if section_type == 'apply' or section_type == 'unapply':
        
        # Then the payload is manually inputed and needs to be converted into Json
        # and saved into a file
        if len(command_list) == 4:

            object_name = command_list[2]
            values = command_list[3]
            values = values.replace('||','=')
            values=values.split('~~')
            _dict = {k:v for k,v in (x.split('=') for x in values)}
            payload = {object_name: {
                    "attributes": _dict
                }
            }
            letters = string.ascii_lowercase
            payload_name = ''.join(random.choice(letters) for i in range(6)) + '.json'
            payload_file = open(payload_name, 'a') 
            payload_file.write(json.dumps(payload))
            payload_file.close()
            command_list = command_list[0:2]
            command_list.append(payload_name)

        if method == 'put' or method == 'post':
            command_list[2] = '{{"payload":"{}"}},\n'.format(command_list[2])

        if len(command_list) == 3 and method == 'delete':
            command_list[2] = '{{"ignore_error":"{}"}},\n'.format(command_list[2])
    else:
        if len(command_list) == 3:
            command_list[2] = '{{"schema":"{}"}},\n'.format(command_list[2])

    return  cmds_to_plugin_converter('processdme', command_list, console_type, device=device, section=section_type, plugin_type='command', rule_id=rule_id)

def _plugin_command_translate(command, console_type, device=None, section=None, plugin_type=None, rule_id=None):

    # Plugins are translated into a blitz action called maple
    # specfically designed to handle maple plugins
    # the input of the maple are the json data representating
    # the maple section from the device to match/unmatch
    dict_vals = {}
    section_dict = {}

    command['plugin'] = _XX_pattern_matching(command['plugin'].strip(), 'replace')
    if rule_id:
        section_dict.update({rule_id: {'type': console_type, 'commands': command['plugin'].strip(' ')}})
    else:
        section_dict.update({'type': console_type, 'commands': command['plugin'].strip(' ')})
        if console_type == 'tgen-config':
            section_dict.update({'type': 'cli' ,'chassis': 'IXIA'})

    section_dict_in_str = json.dumps(section_dict)
    dict_vals.update({'maple':{'section':section_dict_in_str, 'device': device} })
    if plugin_type == 'command':

        dict_vals['maple'].update({'maple_section_type': section})

    return dict_vals

def _hardcoded_command_translate(section_list, command, device, blitz_action):

    # handle the normal commands with replacement ability
    command = command.strip(' ')
    dict_vals = {}
    command = _XX_pattern_matching(command, 'replace')
    dict_vals.update({blitz_action: {'device': device, 'command': command,
                                     'save': [{'variable_name': ''}]}})

    return dict_vals

def _match_unmatch(dict_vals, action, section, console_type, rule_id, device=None, match=None, unmatch=None, val_to_search=None, val_to_search_apply=None):

    if not match and not unmatch:
        return dict_vals
    
    _include_list = _command_handler(match) if match else []
    _exclude_list = _command_handler(unmatch) if unmatch else []

    dict_vals = _find_type_of_match_unmatch_in_blitz('include', dict_vals, action,
                                                     section, console_type, rule_id, device, 
                                                     _include_list, val_to_search, val_to_search_apply)
    dict_vals = _find_type_of_match_unmatch_in_blitz('exclude', dict_vals, action,
                                                     section, console_type, rule_id, device,\
                                                     _exclude_list, val_to_search, val_to_search_apply)

    return dict_vals

def _find_type_of_match_unmatch_in_blitz(style, dict_vals, action, section, console_type, rule_id, device=None,\
                                         _match_unmatch_list=None, val_to_search=None, val_to_search_apply=None):

    storage_list = []
    if not _match_unmatch_list:
        return dict_vals

    # val_to_search is to search the output of a confirm section 
    # (bunch of show commands output that are appended)
    # val_to_search has priority over val_to_search_apply
    # val_to_search_apply for checking the include/exclude
    # for apply section
    # This only applies when confirm section doesnt exist

    if val_to_search:
        dict_vals.update({'maple_search':{'search_string': "%VARIABLES{}".format('{'+val_to_search+'}'), 'device': device}})
    elif val_to_search_apply:
        dict_vals.update({'maple_search':{'search_string': "%VARIABLES{}".format('{'+val_to_search_apply+'}'), 'device': device}})

    for item in _match_unmatch_list:
        if isinstance(item, dict):
            # if in cmds=eval::: then it is an arithmatic/logical operation
            # mapped to action compare in blitz

            if 'cmds=' in item['plugin']:
                # if it is a pattern matching scenario
                plugin_dict = _cmds_translate(item['plugin'], console_type, device=device, section=section, rule_id=rule_id)
                dict_vals.update(plugin_dict)
            else:
                # if it is a plugin it would ba confirm plugins which will be a maple action
                plugin_dict = _plugin_command_translate(item, console_type , device=device, plugin_type='confirm', rule_id=rule_id)

                if dict_vals and val_to_search:
                    # if previously an action execute exist on this match/unmatch
                    # The output of that action execute needs to be stored for the
                    # maple action further use
                    plugin_dict['maple'].update({'output': "%VARIABLES{}".format('{'+val_to_search+'}')})

                dict_vals.update(plugin_dict)
        else:
            item = _XX_pattern_matching(item, 'replace')
            storage_list.append(item)
            dict_vals['maple_search'].update({style: storage_list})

    if 'maple_search' in dict_vals:
        if 'include' not in dict_vals['maple_search'] and 'exclude' not in dict_vals['maple_search']:
            dict_vals.pop('maple_search')

    return dict_vals

def _command_handler(commands, dmerest=False, configure=False):

    # handles whether a command is normal, plugin or pattern matching,
    # it just extract the commands, and returns them in a readable format
    # and keeps the order

    append_it = ''
    ret_list = []
    pattern_plugin = re.compile(r'#@#(?P<plugin>[^#@#]+)#@#')
 
    all_match_plugins = re.finditer(pattern_plugin, commands)
    hardcoded_commands = commands
    function_commands = []
    order_list = []
    # check if there is any cmds= or plugin and extract it from original input
    for each_match in all_match_plugins:

        # add the place of the original command in the input for order uses
        order_list.append([each_match.start(), each_match.end()])
        matched_string = each_match.group(0)

        hardcoded_commands = hardcoded_commands.replace(matched_string , '')
        group = each_match.groupdict()

        # check the place of the original command in the input and store it the dict
        group.update({'length': [each_match.start(), each_match.end()]})
        function_commands.append(group)

    # sort out the hardcoded commands
    for command in hardcoded_commands.split('\n'):
        command = command.strip(' ')
        if not command:
           continue

        c = re.search(re.escape(command), commands)
        order_list.append([c.start(), c.end()])

    order_list.sort(key = lambda x : x[0])

    
    # Now all the commands whether hardcoded,
    # or plugins, or cmds is sorted by type
    # walk through the the ordered_list to get
    # the converted version of the input and 
    # add it into return val
    for _list in order_list:

        for command in function_commands:
            if 'length' in command and command['length'] == _list:
                del command['length']

                if append_it:
                    ret_list.append(append_it)
                    append_it = ''
                ret_list.append(command)
                break
        else:
            if configure and not dmerest:
                append_it += commands[_list[0]: _list[1]] + '\n'
            else: 
                ret_list.append(commands[_list[0]: _list[1]])
        
    if append_it:
        ret_list.append(append_it)

    return ret_list

def _cmds_translate(cmd, console_type, device=None, section=None, plugin_type=None, rule_id=None):

    # translates cmds=patterns::: and cmds=eval::: secnarios
    pattern = re.compile(r'cmds=(?P<type>[\w\s]+):{1,3}(?P<data>[\S\s]+)?')
    m = pattern.match(cmd.strip(' '))
    group = m.groupdict()
    if group['type'].strip(' ') == 'patterns':
        return _cmds_patterns_translate(group['data'], device)

    elif group['type'].strip(' ') == 'eval':
        return _cmds_eval_translate(group['data'])

    else:
        if console_type == 'tgen-config':

            # translate legacy mode ixia commands to new plugin inputs,
            return _cmds_ixia_translates(group['type'].strip(' '), group['data'],\
                                        console_type, device=device, section=section,\
                                        plugin_type=plugin_type, rule_id=rule_id)

        # translate legacy mode maple commands to new plugin inputs,
        return _cmds_yaml_translates(group['type'].strip(' '), group['data'],\
                                    console_type, device=device, section=section,\
                                    plugin_type=plugin_type, rule_id=rule_id)

def _cmds_ixia_translates(_type, data, console_type, device=None, section=None, plugin_type=None, rule_id=None):


    # translate legacy mode ixia commands to new plugin inputs,
    args_list= []
    args_ = data

    args_list.append('{{"command":"{}"}},\n'.format(_type))
    args_list.append('{"use_https": "False"},\n')

    if _type == 'trafficstats':
        args_list[0] = '{{"command":"{}"}},\n'.format('gettrafficstats')
        args_list.append('{{"sleep":"{}"}},\n'.format(args_))
    if _type == 'loadconfig':
        args_list.append('{{"config_files":["{}"]}},\n'.format(args_))

    return cmds_to_plugin_converter('ixia', args_list, console_type, device=device, 
                                    section=section, plugin_type=plugin_type, rule_id=rule_id)

def _cmds_yaml_translates(_type, data, console_type, device=None, section=None, plugin_type=None, rule_id=None):

    # gets the cmds=<command> and call the proper function
    args_list= []
    args_ = data

    if _type == 'switchto' or _type == 'suspendvdc':
        argument = '{{"value":"{}"}},\n'.format(args_)
        args_list.append(argument)
    elif _type == 'novpc' or _type == 'sso' or _type == 'sleep' :
        if args_:
            argument = '{{"duration":"{}"}},\n'.format(args_)
            args_list.append(argument)
    elif _type == 'killprocess':
        args_list = _cmds_killprocess_translate(args_)
    elif _type == 'dialog':
        args_list = _cmds_dialog_translate(args_)
    elif _type == 'runonmodule':
        args_list = _cmds_runonmodule_translate(args_)
    elif _type == 'runraw':
        args_list = _cmds_runraw_translate(args_)
    elif _type == 'waitfor':
        args_list = _cmds_waitfor_translate(args_)
    elif _type == 'issu':
        args_list = _cmds_issu_translate(args_)
    elif 'reload' in _type:
        args_list = _cmds_reload_translate(_type, args_)
        _type = 'reload'
    elif 'copy' in _type:
        args_list = _cmds_copy_translate(args_)

    return cmds_to_plugin_converter(_type, args_list, console_type, device=device, 
                                    section=section, plugin_type=plugin_type, rule_id=rule_id)

def _cmds_dialog_translate(data, device=None):

    #cmds=dialog
    data_list = data.split('~')

    data_list[0] = '{{"cmd":"{}"}},\n'.format(data_list[0])
    data_list[1] = '{{"dialog-list":{}}},\n'.format(data_list[1])
    data_list[2] = '{{"sleep":"{}"}},\n'.format(data_list[2])
    if len(data_list) == 4:
        data_list[3] = '{{"timeout":"{}"}},\n'.format(data_list[3])

    return data_list

def _cmds_killprocess_translate(args_):

    #cmds=killprocess
    args_splited = args_.split(',')

    if len(args_splited) > 1:
        args_splited[0] = '{{"media":"{}"}},\n'.format(args_splited[0])
        args_splited[1] = '{{"debug_plugin":"{}"}},\n'.format(args_splited[1])
        args_splited[2] = '{{"process_name":"{}"}},\n'.format(args_splited[2])
    else:
        args_splited[0] = '{{"process_name":"{}"}},\n'.format(args_splited[0])

    return args_splited

def _cmds_copy_translate(args_):

    #cmds=copy

    args_splited = args_.split(',')
    temp_list = []
    args_splited[0] = '{{"server":"{}"}},\n'.format(args_splited[0])
    args_splited[1] = '{{"source":"{}"}},\n'.format(args_splited[1])
    args_splited[2] = '{{"vrf":"{}"}},\n'.format(args_splited[2])
    args_splited[3] = '{{"username":"{}"}},\n'.format(args_splited[3])
    args_splited[4] = '{{"password":"{}"}},\n'.format(args_splited[4])
    args_splited[5] = '{{"media":"{}"}},\n'.format(args_splited[5])
    args_splited[6] = '{{"source_file":"{}"}},\n'.format(args_splited[6])
    if len(args_splited) > 7:
        temp_list = args_splited[7:]

        if len(temp_list) == 2:
            args_splited[7] = '{{"dest_file":"{}"}},\n'.format(args_splited[7])
            args_splited[8] = '{{"compact_copy":"{}"}},\n'.format(args_splited[8])
        else:
            args_splited[7] = '{{"dest_file":"{}"}},\n'.format(args_splited[7])

    return args_splited

def _cmds_reload_translate(_type, args_):

    #cmds=reload
    #cmds=reload_vdc
    #cmds=reload_module

    args_splited = args_.split(',')
    if _type == 'reload':
        args_splited[0] = '{{"sleep":"{}"}},\n'.format(args_splited[0])

        if len(args_splited) == 2:
            args_splited[1] = '{{"no_copy_rs":"{}"}},\n'.format(args_splited[1]) 
        
        if len(args_splited) == 3:
            args_splited[1] = '{{"no_copy_rs":"{}"}},\n'.format(args_splited[1]) 
            args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])
        
        if len(args_splited) == 3:
            args_splited[1] = '{{"no_copy_rs":"{}"}},\n'.format(args_splited[1]) 
            args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])
            args_splited[3] = '{{"is_ascii":"{}"}},\n'.format(args_splited[3])

    elif _type == 'reload_vdc' or _type == 'reload_module':
        args_splited[0] = '{{"value":"{}"}},\n'.format(args_splited[0])

    args_splited.insert(0, '{{"command":"{}"}},\n'.format(_type))

    return args_splited

def _cmds_issu_translate(args_):

    #cmds=issu

    args_splited = args_.split(',')
    ret_list  = []
    ret_list.append('{{"media":"{}"}},\n'.format(args_splited[0]))

    if len(args_splited) == 4:
        ret_list.append('{{"kickstart":"{}"}},\n'.format(args_splited[1]))
        ret_list.append('{{"system":"{}"}},\n'.format(args_splited[2]))
        ret_list.append('{{"sleep":"{}"}},\n'.format(args_splited[3]))
    else:
        ret_list.append('{{"nxos":"{}"}},\n'.format(args_splited[1]))
        ret_list.append('{{"sleep":"{}"}},\n'.format(args_splited[2]))
    
    return ret_list

def _cmds_waitfor_translate(args_):

    #cmds=waitfor

    args_splited = args_.split(',,')

    args_splited[0] = '{{"command":"{}"}},\n'.format(args_splited[0].replace('\n', '\\n'))
    args_splited[1] = '{{"match":"{}"}},\n'.format(args_splited[1])
    args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])

    return args_splited

def _cmds_runraw_translate(args_):

    #cmds=runraw

    args_splited = args_.split(',,')

    args_splited[0] = '{{"command":"{}"}},\n'.format(args_splited[0].replace('\n', '\\n'))
    
    args_splited[1] = '{{"patterns":["{}"]}},\n'.format(args_splited[1])
    if len(args_splited) > 2: 
        args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])

    return args_splited

def _cmds_runonmodule_translate(args_):

    #cmds=runonmodule

    args_splited = args_.split(',')

    args_splited[0] = '{{"module":"{}"}},\n'.format(args_splited[0])
    args_splited[1] = '{{"command":"{}"}},\n'.format(args_splited[1].replace('\n', '\\n'))
    if len(args_splited) == 3:
        args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])

    return args_splited

def _smartman_to_plugin_translator(command, console_type, device=None, section=None, plugin_type=None, rule_id=None):

    # converting smartman inputs into plugin inputs

    args_list = []
    args_list.append('{{"command":"{}"}},\n'.format(command.replace('\n', '\\n')))
    return cmds_to_plugin_converter('smartman', args_list, console_type, device=device, 
                                    section=section, plugin_type=plugin_type, rule_id=rule_id)


def cmds_to_plugin_converter(_type, args_list, console_type, device=None, section=None, plugin_type=None, rule_id=None):

    # This function convert legacy mode inputs of maple commands
    # Convert into new syntax of plugins
    # Then call plugins command converter to create an action maple

    plugin_template = '''
            #@# command:{
                "method":,
                "options":[
                ]}
            #@#
    '''

    string_to_replace = '"method":' 
    method_line = '                {}'.format(string_to_replace)
    string_that_replace = method_line + '"{}"'.format(_type)

    plugin_template = plugin_template.replace(method_line,string_that_replace)

    string_to_replace = '"options":[\n'
    option_line = '            {}'.format(string_to_replace)
    string_that_replace = option_line

    for arg in args_list:
        temp = '                    '+arg
        string_that_replace = string_that_replace + temp

    if args_list:
        plugin_template = plugin_template.replace(option_line,string_that_replace).replace(',\n                ]','\n                ]')
    else:
        plugin_template = plugin_template.replace(option_line, '').replace(']','').replace(',\n                    }','\n                    }')

    command_type_list =_command_handler(plugin_template)

    return _plugin_command_translate(command_type_list[0], console_type, device=device, section=section, plugin_type=plugin_type, rule_id=rule_id)

def _cmds_patterns_translate(cmd_pattern, device):

    # Converting the cmds=patterns into save with filter regex
    # on an action execute in blitz
    cmds_dict = {}
    ret_list = []
    for cmd in cmd_pattern.split('\n'):
        cmd = cmd.strip(' ')
        if not cmd:
            continue

        cmds_list = cmd.strip('[]').split(',,')
        if cmds_list[0] not in cmds_dict:
            cmds_dict.update({cmds_list[0]: [cmds_list[1]]})
        else:
            cmds_dict[cmds_list[0]].append(cmds_list[1])

    for key, value in cmds_dict.items():

        action_dict = {}
        action_dict.update({'execute':{'device': device, 'command': key}})
        value_list = []
        for val in value:
            val = _XX_pattern_matching(val, 'save') 
            val = _XR_pattern_matching(val)
            value_list.append({'filter': val, 'regex': True})
            action_dict['execute'].update({'save':value_list})

        # when checking the pattern matching
        # in matcher section
        # there might be a need for returning
        # multiple actions,
        # The goal here is to achieve that.
        ret_list.append(action_dict)
    return {'specifically_patterns': ret_list}

def _cmds_eval_translate(cmd_eval):

    #changing cmds=eval to compare action in blitz
    ret_dict = {}
    compare_item_list = []
    for cmd in cmd_eval.split('\n'):
        cmd = cmd.strip(' ')
        if not cmd:
            continue
        cmd = _XX_pattern_matching(cmd, 'replace')
        compare_item_list.append(cmd)
    ret_dict.update({'compare':{'items':compare_item_list}})

    return ret_dict

def _XR_pattern_matching(val):

    # XR used to replace values in cmds=patterns::: only! 
    pattern_XR = re.compile(r'XR\(([^XR]+)\)XR')
    matches_XR = re.findall(pattern_XR, val)
    if matches_XR:
        val = re.sub(r'\bXR\b', 'XX', val)
        return _XX_pattern_matching(val, 'replace')

    return val

def _XX_pattern_matching(val, XX_type):

    # XX is used to save/replace variables in command!
    pattern_XX = re.compile(r'XX\(([^X]+)\)XX')
    matches_XX = re.finditer(pattern_XX, val)

    for match in matches_XX:
        variable_name = match.group(1)
        if XX_type == 'save':
            save_var_name_regx = '?P<{}>'.format(variable_name)
            val = val.replace(match.group(0)+'(', '({}'.format(save_var_name_regx))
        elif XX_type == 'replace':
            save_var_name_regx = "%VARIABLES{}".format('{'+variable_name+'}')
            val = val.replace(match.group(0), '{}'.format(save_var_name_regx))

    return val

# IF YOU WANT TO ONLY CONVERT TWO SCRIPTS
# SIMPLY CALL THE CONVERTOR FUNCTION WITH 
# THE NAME OF YOUR TESTSCRIPT AS AN ARGS

# convertor('mpls-static-n9k-tests.yaml')
