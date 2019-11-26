# Python
from ipaddress import ip_interface 

# super class
from genie.libs.ops.routing.routing import Routing as SuperRouting

# genie.libs
from genie.libs.parser.iosxr.show_routing import ShowRouteIpDistributor,\
                                      ShowRouteIpv6Distributor

class Routing(SuperRouting):
    '''Routing Ops Object'''

    def learn(self, vrf=None, address_family=None, route=None, protocol=None, interface=None):
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

        kwargs = {k: v for k, v in locals().items() if v}
        [kwargs.pop(x, None) for x in ['address_family', 'self']]
        
        if route:
            address_family = 'ipv4' if ip_interface(route).ip.version == 4 else 'ipv6'
            src_routing_route = '[entry][(?P<entry>.*)]'
            dest_routing_route = 'info[vrf][{vrf}][address_family][{address_family}]' \
                '[routes][(?P<entry>.*)]'.format(
                    vrf=vrf if vrf else 'default',
                    address_family=address_family if address_family else 'ipv4')
            src_routing_intf = src_routing_route + '[paths][(?P<paths>.*)]'
            dest_routing_intf = dest_routing_route + '[next_hop]'
        else:
            src_routing_route = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)]' \
                '[routes][(?P<route>.*)]'
            dest_routing_route = 'info' + src_routing_route
            src_routing_intf = src_routing_route +'[next_hop][outgoing_interface][{interface}]'. \
                format(interface='(?P<intf>.*)' if not interface else interface)
            dest_routing_intf = 'info' + src_routing_intf
            src_routing_hop = src_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
            dest_routing_hop = 'info' + src_routing_hop
        
        if not address_family or address_family == 'ipv4':
            if interface and kwargs.get('interface', None):
                kwargs.pop('interface')
            if route:
                req_key = ['ip', 'metric']
                kwargs.update({'cmd': ShowRouteIpDistributor})
                for key in req_key:
                    kwargs.update({'src': src_routing_route + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_route + '[{}]'.format(key)})
                    self.add_leaf(**kwargs)
                req_key = ['metric', 'nexthop', 'interface']
                for key in req_key:
                    des_key = key
                    if des_key == 'interface':
                        des_key = 'outgoing_interface'
                    if des_key == 'nexthop':
                        des_key = 'next_hop'
                    kwargs.update({'src': src_routing_intf + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_intf + '[{}]'.format(des_key)})
                    self.add_leaf(**kwargs)
            else:
                req_key = ['route', 'active', 'route_preference', 'metric','source_protocol','source_protocol_codes']
                kwargs.update({'cmd': ShowRouteIpDistributor})
                for key in req_key:
                    kwargs.update({'src': src_routing_route + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_route + '[{}]'.format(key)})
                    self.add_leaf(**kwargs)

                kwargs.update({'src': src_routing_intf + '[outgoing_interface]'})
                kwargs.update({'dest': dest_routing_intf + '[outgoing_interface]'})
                self.add_leaf(**kwargs)

                req_key = ['index', 'next_hop','outgoing_interface', 'updated']
                for key in req_key:
                    kwargs.update({'src': src_routing_hop + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_hop + '[{}]'.format(key)})
                    self.add_leaf(**kwargs)
        
        ##############################################
        ####            Ipv6                ##########
        if not address_family or address_family == 'ipv6':
            if route:
                if interface and kwargs.get('interface', None):
                    kwargs.pop('interface')
                req_key = ['ip', 'metric']
                kwargs.update({'cmd': ShowRouteIpv6Distributor})
                for key in req_key:
                    kwargs.update({'src': src_routing_route + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_route + '[{}]'.format(key)})
                    self.add_leaf(**kwargs)
                req_key = ['metric', 'fwd_intf']
                for key in req_key:
                    des_key = key
                    if des_key == 'fwd_intf':
                        des_key = 'outgoing_interface'
                    kwargs.update({'src': src_routing_intf + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_intf + '[{}]'.format(des_key)})
                    self.add_leaf(**kwargs)
            else:
                kwargs.update({'cmd': ShowRouteIpv6Distributor})
                req_key = ['route', 'active', 'route_preference', 'metric', 'source_protocol', 'source_protocol_codes']
                for key in req_key:
                    kwargs.update({'src': src_routing_route + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_route + '[{}]'.format(key)})
                    self.add_leaf(**kwargs)
                
                kwargs.update({'src': src_routing_intf + '[outgoing_interface]'})
                kwargs.update({'dest': dest_routing_intf + '[outgoing_interface]'})
                self.add_leaf(**kwargs)

                req_key = ['index', 'next_hop', 'updated', 'outgoing_interface']
                for key in req_key:
                    kwargs.update({'src': src_routing_hop + '[{}]'.format(key)})
                    kwargs.update({'dest': dest_routing_hop + '[{}]'.format(key)})
                    self.add_leaf(**kwargs)
                            
        self.make(final_call=True)