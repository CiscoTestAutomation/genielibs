''' 
Vrf Genie Ops Object for IOSXR - CLI.
'''

# Genie
from genie.libs.ops.vrf.vrf import Vrf as SuperVrf
from genie.ops.base import Context

# iosxe show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail


class Vrf(SuperVrf):
    '''Vrf Genie Ops Object'''

    def learn(self, vrf=''):

        '''Learn Vrf Ops'''

        src = '[(?P<vrf>.*)][address_family][(?P<af>.*)][route_target]'
        dest = 'info[vrfs][(?P<vrf>.*)][address_family][(?P<af>.*)][route_targets]'

        # route_distinguisher
        self.add_leaf(cmd=ShowVrfAllDetail,
                      src='[(?P<vrf>.*)][route_distinguisher]',
                      dest='info[vrfs][(?P<vrf>.*)][route_distinguisher]',
                      vrf=vrf)

        # description
        self.add_leaf(cmd=ShowVrfAllDetail,
                      src= '[(?P<vrf>.*)][description]',
                      dest= 'info[vrfs][(?P<vrf>.*)][description]',
                      vrf=vrf)

        self.add_leaf(cmd=ShowVrfAllDetail,
                      src=src,
                      dest=dest,
                      vrf=vrf)

        self.make(final_call=True)