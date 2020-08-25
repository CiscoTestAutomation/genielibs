import json
import random
import string
from genie.libs.sdk.triggers.blitz.maple_converter.legacy_maple_converter import Internal_Converter

class Legacy_Smartman_Converter(Internal_Converter):
    
    def __init__(self, command):
        super().__init__()

        self.command = command

    def smartman_to_maple_plugin_converter(self):

        '''
            converting the smartman legacy commands to a smartman maple plugin
        '''

        args_list = []
        args_list.append('{{"command":"{}"}},\n'.format(self.command.replace('\n', '\\n')))
        return self.legacy_cmds_to_maple_plugin_converter('smartman', args_list)