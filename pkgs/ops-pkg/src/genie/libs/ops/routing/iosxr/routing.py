# Genie package
from genie.ops.base import Base

# genie.libs
from genie.libs.parser.iosxr.show_routing import ShowRouteIpv4,\
                                      ShowRouteIpv6

class Routing(Base):
    '''Routing Ops Object'''

    def learn(self):
        '''Learn Routing object'''

        # vrf
        #    af
        #     route
        #       route
        #       active
        #       source_protocol
        #       metric
        #       route_preference
        #       source_protocol_codes
        #       last_updated    N/A
        #       next_hop
        #           outgoing_interface
        #               outgoing_interface
        #          next_hop_list
        #               next_hop
        #               updated
        #               index
        #               outgoing_interface
        #          special_next_hop     N/A
        #               special_next_hop       N/A
        #
        # routing structure
        # Place holder to make it more readable

        ##############################################
        ####            Ipv4                ##########

        src_routing_route = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)]' \
                                  '[routes][(?P<route>.*)]'
        dest_routing_route = 'info' + src_routing_route

        req_key = ['route', 'active', 'route_preference', 'metric','source_protocol','source_protocol_codes']
        for key in req_key:
            self.add_leaf(cmd=ShowRouteIpv4,
                          src=src_routing_route + '[{}]'.format(key),
                          dest=dest_routing_route + '[{}]'.format(key)
                          )

        src_routing_intf = src_routing_route +'[next_hop][outgoing_interface][(?P<intf>.*)]'
        dest_routing_intf = 'info' + src_routing_intf

        self.add_leaf(cmd=ShowRouteIpv4,
                      src=src_routing_intf + '[outgoing_interface]',
                      dest=dest_routing_intf + '[outgoing_interface]')


        src_routing_hop = src_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
        dest_routing_hop = 'info' + src_routing_hop

        req_key = ['index', 'next_hop','outgoing_interface', 'updated']
        for key in req_key:
            self.add_leaf(cmd=ShowRouteIpv4,
                          src=src_routing_hop + '[{}]'.format(key),
                          dest=dest_routing_hop + '[{}]'.format(key))


        ##############################################
        ####            Ipv6                ##########

        self.add_leaf(cmd=ShowRouteIpv6,
                      src='[ipv6_unicast_routing_enabled]',
                      dest='info[ipv6_unicast_routing_enabled]'
                      )

        req_key = ['route', 'active', 'route_preference', 'metric', 'source_protocol', 'source_protocol_codes']
        for key in req_key:
            self.add_leaf(cmd=ShowRouteIpv6,
                          src=src_routing_route + '[{}]'.format(key),
                          dest=dest_routing_route + '[{}]'.format(key)
                          )


        self.add_leaf(cmd=ShowRouteIpv6,
                      src=src_routing_intf + '[outgoing_interface]',
                      dest=dest_routing_intf + '[outgoing_interface]')


        req_key = ['index', 'next_hop', 'updated', 'outgoing_interface']
        for key in req_key:
            self.add_leaf(cmd=ShowRouteIpv6,
                          src=src_routing_hop + '[{}]'.format(key),
                          dest=dest_routing_hop + '[{}]'.format(key))
        self.make(final_call=True)