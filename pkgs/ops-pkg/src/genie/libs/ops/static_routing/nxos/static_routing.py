# Genie package
from genie.ops.base import Base
from genie.libs.ops.static_routing.static_routing import StaticRouting as SuperStaticRouting
# genie.libs
from genie.libs.parser.nxos.show_static_routing import ShowIpStaticRoute,\
                                             ShowIpv6StaticRoute

class StaticRouting(SuperStaticRouting):
    '''StaticRouting Ops Object'''

    def learn(self):
        '''Learn StaticRouting object'''

        # new StaticRouting structure
        # Place holder to make it more readable

        ##############################################
        ####            Ipv4                ##########

        # vrf
        #   ipv4
        #     route
        #       next_hop
        #          outgoing_interface
        #               next_hop_vrf N/A
        #               tag N/A
        #               track N/A
        #               preference N/A
        #          next_hop_list
        #               next_hop_vrf N/A
        #               tag N/A
        #               track N/A
        #               preference N/A

        src_static_routing_route = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)]' \
                                  '[routes][(?P<route>.*)]'
        dest_static_routing_route = 'info' + src_static_routing_route

        self.add_leaf(cmd=ShowIpStaticRoute,
                      src=src_static_routing_route + '[route]',
                      dest=dest_static_routing_route + '[route]'
                      )

        src_static_routing_intf = src_static_routing_route +'[next_hop][outgoing_interface][(?P<intf>.*)]'
        dest_static_routing_intf = 'info' + src_static_routing_intf


        req_key =['outgoing_interface','active']
        for key in req_key:
            self.add_leaf(cmd=ShowIpStaticRoute,
                          src=src_static_routing_intf + '[{}]'.format(key),
                          dest=dest_static_routing_intf + '[{}]'.format(key))


        src_static_routing_hop = src_static_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
        dest_static_routing_hop = 'info' + src_static_routing_hop

        req_key = ['index', 'active', 'next_hop', 'outgoing_interface']
        for key in req_key:
            self.add_leaf(cmd=ShowIpStaticRoute,
                          src=src_static_routing_hop + '[{}]'.format(key),
                          dest=dest_static_routing_hop + '[{}]'.format(key))


        ##############################################
        ####            Ipv6                ##########
        # vrf
        #   ipv6
        #     route
        #       next_hop
        #          outgoing_interface
        #               tag N/A
        #               active N/A
        #               track N/A
        #          next_hop_list
        #               tag N/A
        #               track N/A
        #               active N/A

        self.add_leaf(cmd=ShowIpv6StaticRoute,
                      src=src_static_routing_route + '[route]',
                      dest=dest_static_routing_route + '[route]'
                      )

        req_key = ['outgoing_interface', 'next_hop_vrf' ,'preference']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6StaticRoute,
                          src=src_static_routing_intf + '[{}]'.format(key),
                          dest=dest_static_routing_intf + '[{}]'.format(key))


        req_key = ['index', 'next_hop', 'outgoing_interface', 'next_hop_vrf', 'preference']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6StaticRoute,
                          src=src_static_routing_hop + '[{}]'.format(key),
                          dest=dest_static_routing_hop + '[{}]'.format(key))
        self.make(final_call=True)

class StaticRoute(Base):
    # Keeping it for backward compatibility
    pass
