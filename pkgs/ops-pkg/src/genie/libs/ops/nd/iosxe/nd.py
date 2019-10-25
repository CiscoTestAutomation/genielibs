# Genie package
from genie.ops.base import Base

# genie.libs
from genie.libs.parser.iosxe.show_ipv6 import ShowIpv6Neighbors
from genie.libs.parser.iosxe.show_interface import ShowIpv6Interface


class Nd(Base):
    '''Nd Ops Object'''

    def learn(self, vrf='', interface=''):
        '''Learn Nd object'''

        # new Nd structure
        # Place holder to make it more readable
        #  interface
        #     interface
        #     router_advertisement
        #         interval
        #         lifetime
        #         suppress
        #     neighbors
        #         neighbor
        #             ip
        #             link_layer_address
        #             neighbor_state
        #             age
        #             origin                N/A
        #             is_router             N/A

        src_nd = '[interface][(?P<interface>.*)]'
        dest_nd = 'info' + src_nd
        self.add_leaf(cmd=ShowIpv6Neighbors,
                      src=src_nd + '[interface]',
                      dest=dest_nd + '[interface]',
                      vrf=vrf, interface=interface)
        self.make()

        src_rd = '[(?P<interface>.*)][ipv6][nd]'
        dest_rd = dest_nd +'[router_advertisement]'
        req_dict = {'router_advertisements_interval':'interval', 
                    'router_advertisements_live':'lifetime',
                    'suppress':'suppress'}

        for src, dest in req_dict.items():
            self.add_leaf(cmd=ShowIpv6Interface,
                          src=src_rd + '[{}]'.format(src),
                          dest=dest_rd + '[{}]'.format(dest),
                          interface=interface)

        src_nd_neighbor = src_nd +'[neighbors][(?P<neighbor>.*)]'
        dest_nd_neighbor = 'info' + src_nd_neighbor
        req_key =['ip','link_layer_address','neighbor_state','age']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6Neighbors,
                          src=src_nd_neighbor + '[{}]'.format(key),
                          dest=dest_nd_neighbor + '[{}]'.format(key),
                          vrf=vrf, interface=interface)
        
        self.make(final_call=True)
