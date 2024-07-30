'''
Interface Genie Ops Object for Sonic.
'''

# super class
from genie.libs.ops.interface.interface import Interface as SuperInterface


class Interface(SuperInterface):
    '''Interface Genie Ops Object'''

    def learn(self, custom=None, interface=None, vrf=None, address_family=None):
        '''Learn Interface Ops'''
        ########################################################################
        #                               info
        ########################################################################
        # Global source

        src = '[(?P<interface>.*)]'
        dest = 'info[interface][(?P<interface>.*)]'
        wired_key_map = {
            'identifier': 'description',
            'oper_status': 'oper_status',
        }

        # show interfaces transceiver eeprom
        for src_key, dest_key in wired_key_map.items():
            self.add_leaf(cmd=f'show interfaces transceiver eeprom',
                          src=src + f'[{src_key}]',
                          dest=dest + f'[{dest_key}]',)

        # type
        self.add_leaf(cmd='show interfaces transceiver eeprom',
                      src=src + '[application_advertisment][cable_type]',
                      dest=dest + '[type]')

        self.make(final_call=True)
