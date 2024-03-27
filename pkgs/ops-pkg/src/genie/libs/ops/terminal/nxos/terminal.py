'''
Show Terminal Genie Ops Object for NXOS - CLI.
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
            "type": "type",
            "length": "length",
            "width": "width"
        }

        self.add_leaf(cmd='show terminal',
                      src=src + '[tty]',
                      dest=dest + '[line]')

        for src_key, dest_key in terminal_map.items():
            self.add_leaf(cmd='show terminal',
                          src=src + f'[{src_key}]',
                          dest=dest + f'[{dest_key}]')

        self.make(final_call=True)