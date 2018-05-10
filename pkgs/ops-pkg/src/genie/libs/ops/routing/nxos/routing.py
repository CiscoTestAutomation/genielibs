# Genie package
from genie.ops.base import Base

# genie.libs
from genie.libs.parser.nxos.show_routing import ShowIpRoute,\
                                     ShowIpv6Route

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
        #       source_protocol_codes  N/A
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

        req_key = ['route', 'active', 'source_protocol','metric','route_preference']
        for key in req_key:
            self.add_leaf(cmd=ShowIpRoute,
                          src=src_routing_route + '[{}]'.format(key),
                          dest=dest_routing_route + '[{}]'.format(key),
                          vrf='all')

        src_routing_intf = src_routing_route +'[next_hop][outgoing_interface][(?P<intf>.*)]'
        dest_routing_intf = 'info' + src_routing_intf

        self.add_leaf(cmd=ShowIpRoute,
                      src=src_routing_intf + '[outgoing_interface]',
                      dest=dest_routing_intf + '[outgoing_interface]',
                      vrf='all')

        src_routing_hop = src_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
        dest_routing_hop = 'info' + src_routing_hop

        req_key = ['index', 'next_hop','updated','outgoing_interface']
        for key in req_key:
            self.add_leaf(cmd=ShowIpRoute,
                          src=src_routing_hop + '[{}]'.format(key),
                          dest=dest_routing_hop + '[{}]'.format(key),
                          vrf='all')

        ##############################################
        ####            Ipv6                ##########

        req_key = ['route', 'active', 'route_preference', 'metric', 'source_protocol']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6Route,
                          src=src_routing_route + '[{}]'.format(key),
                          dest=dest_routing_route + '[{}]'.format(key),
                          vrf='all')

        self.add_leaf(cmd=ShowIpv6Route,
                      src=src_routing_intf + '[outgoing_interface]',
                      dest=dest_routing_intf + '[outgoing_interface]',
                      vrf='all')

        req_key = ['index', 'next_hop', 'updated','outgoing_interface']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6Route,
                          src=src_routing_hop + '[{}]'.format(key),
                          dest=dest_routing_hop + '[{}]'.format(key),
                          vrf='all')

        self.make()