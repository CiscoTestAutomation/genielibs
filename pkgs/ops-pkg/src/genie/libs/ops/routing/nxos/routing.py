# super class
from genie.libs.ops.routing.routing import Routing as SuperRouting

# genie.libs
from genie.libs.parser.nxos.show_routing import ShowIpRoute,\
                                     ShowIpv6Route

class Routing(SuperRouting):
    '''Routing Ops Object'''

    def learn(self, address_family=None, route=None, protocol=None, interface=None, vrf=None):
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

        kwargs = {k: v for k, v in locals().items() if v}
        [kwargs.pop(x, None) for x in ['address_family', 'self']]
        
        if not address_family or address_family == 'ipv4':
            ##############################################
            ####            Ipv4                ##########
            
            src_routing_route = '[vrf][{vrf}][address_family][(?P<af>.*)]' \
                                    '[routes][(?P<route>.*)]'.format(
                                        vrf=vrf if vrf else '(?P<vrf>.*)',
                                    )

            dest_routing_route = 'info' + src_routing_route
            
            req_key = ['route', 'active', 'source_protocol','metric','route_preference']
            
            kwargs.update({'cmd': ShowIpRoute})
            kwargs.update({'vrf': 'all' if not vrf else vrf})
            
            for key in req_key:
                kwargs.update({'src': src_routing_route + '[{}]'.format(key)})
                kwargs.update({'dest': dest_routing_route + '[{}]'.format(key)})
                self.add_leaf(**kwargs)

            src_routing_intf = src_routing_route +'[next_hop][outgoing_interface][(?P<intf>.*)]'
            dest_routing_intf = 'info' + src_routing_intf

            kwargs.update({'src': src_routing_intf + '[outgoing_interface]'})
            kwargs.update({'dest': dest_routing_intf + '[outgoing_interface]'})

            self.add_leaf(**kwargs)

            src_routing_hop = src_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
            dest_routing_hop = 'info' + src_routing_hop

            req_key = ['index', 'next_hop','updated','outgoing_interface']
            for key in req_key:
                kwargs.update({'src': src_routing_hop + '[{}]'.format(key)})
                kwargs.update({'dest': dest_routing_hop + '[{}]'.format(key)})
                self.add_leaf(**kwargs)
        
        if not address_family or address_family == 'ipv6':
            ##############################################
            ####            Ipv6                ##########
            kwargs.update({'cmd': ShowIpv6Route})
            src_routing_route_v6 = '[vrf][{vrf}][address_family][(?P<af>.*)]' \
                                    '[routes][(?P<route>.*)]'.format(
                                        vrf=vrf if vrf else '(?P<vrf>.*)',
                                    )
            dest_routing_route_v6 = 'info' + src_routing_route_v6

            req_key = ['route', 'active', 'route_preference', 'metric', 'source_protocol']
            for key in req_key:
                kwargs.update({'src': src_routing_route_v6 + '[{}]'.format(key)})
                kwargs.update({'dest': dest_routing_route_v6 + '[{}]'.format(key)})
                self.add_leaf(**kwargs)

            src_routing_intf_v6 = src_routing_route_v6 +'[next_hop][outgoing_interface][(?P<intf>.*)]'
            dest_routing_intf_v6 = 'info' + src_routing_intf_v6

            kwargs.update({'src': src_routing_intf_v6 + '[outgoing_interface]'})
            kwargs.update({'dest': dest_routing_intf_v6 + '[outgoing_interface]'})
            self.add_leaf(**kwargs)

            src_routing_hop_v6 = src_routing_route_v6 +'[next_hop][next_hop_list][(?P<index>.*)]'
            dest_routing_hop_v6 = 'info' + src_routing_hop_v6

            req_key = ['index', 'next_hop', 'updated','outgoing_interface']
            for key in req_key:
                kwargs.update({'src': src_routing_hop_v6 + '[{}]'.format(key)})
                kwargs.update({'dest': dest_routing_hop_v6 + '[{}]'.format(key)})
                self.add_leaf(**kwargs)

        self.make(final_call=True)