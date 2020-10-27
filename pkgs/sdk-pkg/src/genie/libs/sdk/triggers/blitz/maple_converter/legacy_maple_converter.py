import re
import json


'''
The name internal converter is chosen for this class
as this class is the base class to convert legacy maple commands
into maple_plugins commands so, technically internal conversion
between command --> Internal_Converter
'''


class Internal_Converter(object):
    
    def legacy_cmds_to_maple_plugin_converter(self,legacy_cmd_type, legacy_args ):

        '''
        Example of the legacy command to plugin conversion:

            syntax-legacy:
                #@# cmds=runonmodule:<module number>,<command>,<timeout> #@#
                         <legacy_cmd_type>:[<arg1>,<arg2>,<arg3>]
                                            legacy)_args

            syntax-plugin:

                #@# command:{
                "method":"runonmodule", 
                "options":[
                    {"module": <module number>},
                    {"command": <command>},
                    {"timeout": <timeout>}
                ]}
                #@#

        This function recieve the legacy maple cmds and the necessary arguments from the legacy commands
        And convert it into maple plugins command for further use in blitz

        args:
            legacy_cmd_type: represnet a plugin method name. This name would be mainly extracted from legacy cmds command
                             with exception of legacy dme and legacy smartman
        
            legacy_args: is a list of all the arguments that would be the input to that plugin, again these values would be 
                         extracted from the legacy command

        '''

        plugin_template = '''
                #@# command:{
                    "method":,
                    "options":[
                    ]}
                #@#
        '''

        # changing the empty method in plugin_template with method: <legacy_cmd_type>
        string_to_replace = '"method":' 
        method_line = '             {}'.format(string_to_replace)  
        string_that_replace = method_line + '"{}"'.format(legacy_cmd_type)
        plugin_template = plugin_template.replace(method_line,string_that_replace)

        # changing the empty options in plugin_template with <legacy_cmd_args>
        string_to_replace = '"options":[\n'
        option_line = '             {}'.format(string_to_replace)
        string_that_replace = option_line

        for arg in legacy_args:
            temp = '                    '+arg
            string_that_replace = string_that_replace + temp

        if legacy_args:
            plugin_template = plugin_template.replace(option_line,string_that_replace)
            plugin_template = re.sub(r',\n\s*]', r'\n       ]', plugin_template)
        else:
            plugin_template = plugin_template.replace(option_line, '').replace(']','')
            plugin_template = re.sub(r',\n\s*}', r'\n       }', plugin_template)

        # command_separator does receives various form of maple commands, and returns them sorted within a list
        # mape plugins in this function would change into dictionary
        # Maple plugins now needs to be adjusted into dictionary just like other maple plugins
        command_type_list = Internal_Converter._command_separator(plugin_template)

        return command_type_list[0]

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def _XR_pattern_matching(val):

        # XR used to replace values in cmds=patterns::: only! 
        pattern_XR = re.compile(r'XR\(([\S\s]+?)\)XR')
        matches_XR = re.findall(pattern_XR, str(val))
        if matches_XR:
            val = re.sub(r'\bXR\b', 'XX', str(val))
            return Internal_Converter._XX_pattern_matching(val, 'replace')

        return val
