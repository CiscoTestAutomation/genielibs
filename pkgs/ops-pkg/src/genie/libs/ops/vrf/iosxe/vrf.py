''' 
Vrf Genie Ops Object for IOSXE - CLI.
'''

# Genie
from genie.libs.ops.vrf.vrf import Vrf as SuperVrf
from genie.ops.base import Context


class Vrf(SuperVrf):
    '''Vrf Genie Ops Object'''

    def learn(self, vrf=''):

        '''Learn Vrf Ops'''

        ########################################################################
        #                                 info
        ########################################################################
        src = '[(?P<vrf>.*)][address_family][(?P<af>.*)]'
        dest = 'info[vrfs][(?P<vrf>.*)][address_family][(?P<af>.*)]'
        keys = ['[route_targets]','[table_id]','[import_from_global][import_from_global_map]',
                '[export_to_global][export_to_global_map]',
                '[routing_table_limit][routing_table_limit_action]',
                '[routing_table_limit][routing_table_limit_number]',
                '[routing_table_limit][enable_simple_alert]']

        # route_distinguisher
        self.add_leaf(cmd='show vrf detail',
                      src='[(?P<vrf>.*)][route_distinguisher]',
                      dest='info[vrfs][(?P<vrf>.*)][route_distinguisher]',
                      vrf=vrf)

        # description
        self.add_leaf(cmd='show vrf detail',
                      src= '[(?P<vrf>.*)][description]',
                      dest= 'info[vrfs][(?P<vrf>.*)][description]',
                      vrf=vrf)

        for key in keys:
            self.add_leaf(cmd='show vrf detail',
                          src=src + '{key}'.format(key=key),
                          dest=dest + '{key}'.format(key=key), vrf=vrf)

        self.make(final_call=True)

