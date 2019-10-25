# Genie package
from genie.libs.ops.static_routing.static_routing import StaticRouting as SuperStaticRouting
from genie.ops.base import Base
# genie.libs
from genie.libs.parser.iosxr.show_static_routing import ShowStaticTopologyDetail

class StaticRouting(SuperStaticRouting):
    '''StaticRouting Ops Object'''

    def learn(self):
        '''Learn StaticRouting object'''

        # vrf
        #   af
        #     route
        #       next_hop
        #          outgoing_interface
        #               next_hop_vrf N/A
        #               tag N/A
        #               track N/A
        #          next_hop_list
        #               next_hop_vrf N/A
        #               outgoing_interface N/A
        #               tag N/A
        #               track N/A

        # new StaticRouting structure
        # Place holder to make it more readable

        src_static_routing_route = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)]' \
                                  '[routes][(?P<route>.*)]'
        dest_static_routing_route = 'info' + src_static_routing_route

        self.add_leaf(cmd=ShowStaticTopologyDetail,
                      src=src_static_routing_route + '[route]',
                      dest=dest_static_routing_route + '[route]'
                      )

        src_static_routing_intf = src_static_routing_route +'[next_hop][outgoing_interface][(?P<intf>.*)]'
        dest_static_routing_intf = 'info' + src_static_routing_intf


        req_key =['outgoing_interface','active','preference']
        for key in req_key:
            self.add_leaf(cmd=ShowStaticTopologyDetail,
                          src=src_static_routing_intf + '[{}]'.format(key),
                          dest=dest_static_routing_intf + '[{}]'.format(key))


        src_static_routing_hop = src_static_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
        dest_static_routing_hop = 'info' + src_static_routing_hop

        req_key = ['index', 'active', 'next_hop','preference']
        for key in req_key:
            self.add_leaf(cmd=ShowStaticTopologyDetail,
                          src=src_static_routing_hop + '[{}]'.format(key),
                          dest=dest_static_routing_hop + '[{}]'.format(key))

        self.make(final_call=True)

class StaticRoute(Base):
    # Keeping it for backward compatibility
    pass
