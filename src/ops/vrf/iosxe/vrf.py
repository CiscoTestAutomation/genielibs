''' 
Vrf Genie Ops Object for IOSXE - CLI.
'''

# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class Vrf(Base):
    '''Vrf Genie Ops Object'''

    def learn(self):

        '''Learn Vrf Ops'''

        ########################################################################
        #                                 info
        ########################################################################

        # route_distinguisher
        self.add_leaf(cmd=ShowVrfDetail,
                      src='[(?P<vrf>.*)][route_distinguisher]',
                      dest='info[vrfs][(?P<vrf>.*)][route_distinguisher]')

        # address_family          
        src = '[(?P<vrf>.*)][address_family][(?P<af>.*)]'
        dest = 'info[vrfs][(?P<vrf>.*)][address_family][(?P<af>.*)]'

        keys = ['[route_targets]', '[import_from_global][import_from_global_map]',
                '[export_to_global][export_to_global_map]',
                '[routing_table_limit][routing_table_limit_action]',
                '[routing_table_limit][routing_table_limit_number]',
                '[routing_table_limit][enable_simple_alert]']

        for key in keys:
            self.add_leaf(cmd=ShowVrfDetail,
                          src=src+'{key}'.format(key=key),
                          dest=dest+'{key}'.format(key=key))

        self.make()