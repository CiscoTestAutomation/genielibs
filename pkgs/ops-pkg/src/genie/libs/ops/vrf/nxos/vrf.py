''' 
Vrf Genie Ops Object for NXOS - CLI.
'''

# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# nxos show_vrf
from genie.libs.parser.nxos.show_vrf import ShowVrfDetail


class Vrf(Base):
    '''Vrf Genie Ops Object'''

    def keys(self, item):
        '''return only the key from the item'''
        ret_dict = {}
        for key in item:
            ret_dict[key] = {}
        return ret_dict

    def learn(self, vrf=''):

        '''Learn Vrf Ops'''

        src = '[(?P<vrf>.*)][address_family]'
        dest = 'info[vrfs][(?P<vrf>.*)][address_family]'

        self.add_leaf(cmd=ShowVrfDetail,
                      src='[(?P<vrf>.*)][route_distinguisher]',
                      dest='info[vrfs][(?P<vrf>.*)][route_distinguisher]',
                      vrf=vrf)
        self.add_leaf(cmd=ShowVrfDetail,
                      src=src,
                      dest=dest,
                      action=self.keys,
                      vrf=vrf)

        self.make(final_call=True)
