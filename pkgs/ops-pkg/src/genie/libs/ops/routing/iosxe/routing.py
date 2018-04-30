# Genie package
from genie.ops.base import Base

# genie.libs
from genie.libs.parser.iosxe.show_routing import ShowIpRoute,\
                                      ShowIpv6RouteUpdated
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

class Routing(Base):
    '''Routing Ops Object'''

    def learn(self):
        '''Learn Routing object'''

        # get vrf list        
        self.add_leaf(cmd=ShowVrfDetail,
                      src='',
                      dest='list_of_vrfs',
                      action=lambda x: list(x.keys()))

        self.make()

        # loop for vrfs
        for vrf in self.list_of_vrfs + ['default']:

            # skip the vrf when it is mgmt-vrf
            if vrf == 'Mgmt-vrf':
                continue

            # create kwargs
            vrf_name = '' if vrf == 'default' else vrf

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
                self.add_leaf(cmd=ShowIpRoute,
                              src=src_routing_route + '[{}]'.format(key),
                              dest=dest_routing_route + '[{}]'.format(key),
                              vrf=vrf_name)

            src_routing_intf = src_routing_route +'[next_hop][outgoing_interface][(?P<intf>.*)]'
            dest_routing_intf = 'info' + src_routing_intf

            self.add_leaf(cmd=ShowIpRoute,
                          src=src_routing_intf + '[outgoing_interface]',
                          dest=dest_routing_intf + '[outgoing_interface]',
                          vrf=vrf_name)


            src_routing_hop = src_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
            dest_routing_hop = 'info' + src_routing_hop

            req_key = ['index', 'next_hop','outgoing_interface', 'updated']
            for key in req_key:
                self.add_leaf(cmd=ShowIpRoute,
                              src=src_routing_hop + '[{}]'.format(key),
                              dest=dest_routing_hop + '[{}]'.format(key),
                              vrf=vrf_name)


            ##############################################
            ####            Ipv6                ##########

            self.add_leaf(cmd=ShowIpv6RouteUpdated,
                          src='[ipv6_unicast_routing_enabled]',
                          dest='info[ipv6_unicast_routing_enabled]',
                          vrf=vrf_name)

            req_key = ['route', 'active', 'route_preference', 'metric', 'source_protocol', 'source_protocol_codes']
            for key in req_key:
                self.add_leaf(cmd=ShowIpv6RouteUpdated,
                              src=src_routing_route + '[{}]'.format(key),
                              dest=dest_routing_route + '[{}]'.format(key),
                              vrf=vrf_name)


            self.add_leaf(cmd=ShowIpv6RouteUpdated,
                          src=src_routing_intf + '[outgoing_interface]',
                          dest=dest_routing_intf + '[outgoing_interface]',
                          vrf=vrf_name)


            req_key = ['index', 'next_hop', 'updated', 'outgoing_interface']
            for key in req_key:
                self.add_leaf(cmd=ShowIpv6RouteUpdated,
                              src=src_routing_hop + '[{}]'.format(key),
                              dest=dest_routing_hop + '[{}]'.format(key),
                              vrf=vrf_name)
                
        # delete the list_of_vrfs in the info table
        del self.list_of_vrfs
        self.make()