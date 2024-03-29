'''
Show Terminal Genie Ops Object for IOSXE - CLI.
'''

# super class
from genie.libs.ops.terminal.terminal import Terminal as SuperTerminal

class Terminal(SuperTerminal):
    '''Show Terminal Genie Ops Object'''

    def learn(self):
        '''Learn Interface Ops'''
        ########################################################################
        #                               info
        ########################################################################
        # Global source
        src = ''
        dest = 'info'

        terminal_map = {
            'line': 'line',
            'location': 'location',
            "type": 'type',
            "length": 'length',
            "width": 'width',
            "baud_rate": "baud_rate",
            "parity": 'parity',
            "stopbits": 'stopbits',
            "databits": 'databits',
            "input_transport": 'input_transport',
            "output_transport": 'output_transport'
        }


        for src_key, dest_key in terminal_map.items():
            self.add_leaf(cmd=f'show terminal',
                          src=src + f'[{src_key}]',
                          dest=dest + f'[{dest_key}]')

        self.make(final_call=True)