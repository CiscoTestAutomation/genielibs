''' 
Vrf Genie Ops Object for IOSXR - CLI.
'''

# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# iosxe show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail


class Vrf(Base):
    '''Vrf Genie Ops Object'''

    def learn(self):

        '''Learn Vrf Ops'''

        ########################################################################
        #                                 info
        ########################################################################

        # route_distinguisher
        self.add_leaf(cmd=ShowVrfAllDetail,
                      src='[(?P<vrf>.*)][route_distinguisher]',
                      dest='info[vrfs][(?P<vrf>.*)][route_distinguisher]')

        # address_family          
        src = '[(?P<vrf>.*)][address_family][(?P<af>.*)][route_target]'
        dest = 'info[vrfs][(?P<vrf>.*)][address_family][(?P<af>.*)][route_targets]'

        self.add_leaf(cmd=ShowVrfAllDetail,
                          src=src,
                          dest=dest)

        self.make(final_call=True)