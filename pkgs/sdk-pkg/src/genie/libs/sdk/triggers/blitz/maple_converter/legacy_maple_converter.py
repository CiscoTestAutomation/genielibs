import re
import json

from .utils import _command_separator

'''
The name internal converter is chosen for this class
as this class is the base class to convert legacy maple commands
into maple_plugins commands so, technically internal conversion
between command --> Internal_Converter
'''


class InternalConverter(object):
    
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
        command_type_list = _command_separator(plugin_template)

        return command_type_list[0]
