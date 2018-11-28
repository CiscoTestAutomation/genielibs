# Genie package
from genie.ops.base import Base

# genie.libs
from genie.libs.parser.nxos.show_nd import ShowIpv6NeighborDetail,\
                                            ShowIpv6NdInterface,\
                                            ShowIpv6IcmpNeighborDetail,\
                                            ShowIpv6Routers

class Nd(Base):
    '''Nd Ops Object'''

    def learn(self):
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
        #             origin
        #             is_router
        #             neighbor_state
        #             age

        src_nd = '[interfaces][(?P<interface>.*)]'
        dest_nd = 'info' + src_nd
        self.add_leaf(cmd=ShowIpv6NeighborDetail,
                      src=src_nd + '[interface]',
                      dest=dest_nd + '[interface]',
                      vrf='all')

        src_nd_router_advertisment = '[vrf][(?P<vrf>.*)]'+ src_nd +'[router_advertisement]'
        dest_nd_router_advertisment = dest_nd +'[router_advertisement]'
        req_key = ['interval','lifetime','suppress']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6NdInterface,
                        src=src_nd_router_advertisment + '[{}]'.format(key),
                        dest=dest_nd_router_advertisment + '[{}]'.format(key),
                        vrf='all')

        src_nd_neighbor = src_nd +'[neighbors][(?P<neighbor>.*)]'
        dest_nd_neighbor = 'info' + src_nd_neighbor
        req_key =['ip','link_layer_address','origin','age']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6NeighborDetail,
                          src=src_nd_neighbor + '[{}]'.format(key),
                          dest=dest_nd_neighbor + '[{}]'.format(key),
                          vrf='all')

        self.add_leaf(cmd=ShowIpv6Routers,
                      src=src_nd_neighbor + '[is_router]',
                      dest=dest_nd_neighbor + '[is_router]',
                      vrf='all')

        self.add_leaf(cmd=ShowIpv6IcmpNeighborDetail,
                      src=src_nd_neighbor + '[neighbor_state]',
                      dest=dest_nd_neighbor + '[neighbor_state]',
                      vrf='all')
        self.make(final_call=True)