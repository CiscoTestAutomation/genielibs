''' 
Vrf Genie Ops Object for NXOS - CLI.
'''

# Genie
from genie.libs.ops.vrf.vrf import Vrf as SuperVrf
from genie.ops.base import Context

# nxos show_vrf
from genie.libs.parser.nxos.show_vrf import ShowVrfDetail


class Vrf(SuperVrf):
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
        keys = ['[table_id]']

        # route_distinguisher
        self.add_leaf(cmd=ShowVrfDetail,
                      src='[(?P<vrf>.*)][route_distinguisher]',
                      dest='info[vrfs][(?P<vrf>.*)][route_distinguisher]',
                      vrf=vrf)


        for key in keys:
            self.add_leaf(cmd=ShowVrfDetail,
                          src='[(?P<vrf>.*)][address_family][(?P<af>.*)]' + '{key}'.format(key=key),
                          dest='info[vrfs][(?P<vrf>.*)][address_family][(?P<af>.*)]' + '{key}'.format(key=key),
                          vrf=vrf)

        self.add_leaf(cmd=ShowVrfDetail,
                      src=src,
                      dest=dest,
                      action=self.keys,
                      vrf=vrf)

        self.make(final_call=True)
