''' 
Prefix-list Genie Ops Object for NXOS - CLI.
'''

import re

# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# nxos show_prefix_list
from genie.libs.parser.nxos.show_prefix_list import ShowIpPrefixList, \
                                         ShowIpv6PrefixList


class PrefixList(Base):
    '''Prefix-list Genie Ops Object'''

    def learn(self):
        '''Learn Prefix-list Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        for cmd in [ShowIpPrefixList, ShowIpv6PrefixList]:

            # Global source
            src = '[prefix_set_name][(?P<name>.*)]'
            dest = 'info[prefix_set_name][(?P<name>.*)]'
            req_keys = ['[prefix_set_name]', '[protocol]',
                        '[prefixes][(?P<prefixes>.*)][prefix]',
                        '[prefixes][(?P<prefixes>.*)][masklength_range]',
                        '[prefixes][(?P<prefixes>.*)][action]']

            for key in req_keys:
                self.add_leaf(cmd=cmd,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key))


        # make to write in cache
        self.make(final_call=True)
