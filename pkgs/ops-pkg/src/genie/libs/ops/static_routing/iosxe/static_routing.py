# Genie package
from genie.libs.ops.static_routing.static_routing import StaticRouting as SuperStaticRouting
from genie.ops.base import Base
# genie.libs
from genie.libs.parser.iosxe.show_static_routing import ShowIpStaticRoute,\
                                             ShowIpv6StaticDetail
# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

class StaticRouting(SuperStaticRouting):
    '''StaticRouting Ops Object'''

    def keys(self, item):
        if isinstance(item, dict):
            return list(item.keys())
        return []

    def learn(self):
        '''Learn StaticRouting object'''

        # get vrf list
        self.add_leaf(cmd=ShowVrfDetail,
                      src='',
                      dest='list_of_vrfs',
                      action=self.keys)
        # when show vrf details return nothing
        # initial vrf list
        try:
            self.make()
        except Exception:
            self.list_of_vrfs = []

        # incase attribtues are specified that show vrf won't be executed
        if not hasattr(self, 'list_of_vrfs'):
            self.list_of_vrfs = []

        # loop for vrfs
        for vrf in self.list_of_vrfs + ['default']:

            # skip the vrf when it is mgmt-vrf
            if vrf == 'Mgmt-vrf':
                continue

            # create kwargs
            vrf_name = '' if vrf == 'default' else vrf

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
            #               tag N/A
            #               track N/A

            # new StaticRouting structure
            # Place holder to make it more readable

            ##############################################
            ####            Ipv4                ##########

            src_static_routing_route = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)]' \
                                      '[routes][(?P<route>.*)]'
            dest_static_routing_route = 'info' + src_static_routing_route

            self.add_leaf(cmd='show ip static route vrf {vrf}'.format(vrf=vrf),
                          src=src_static_routing_route + '[route]',
                          dest=dest_static_routing_route + '[route]',
                          vrf=vrf_name)

            src_static_routing_intf = src_static_routing_route +'[next_hop][outgoing_interface][(?P<intf>.*)]'
            dest_static_routing_intf = 'info' + src_static_routing_intf


            req_key =['outgoing_interface','active','preference']
            for key in req_key:
                self.add_leaf(cmd='show ip static route vrf {vrf}'.format(vrf=vrf),
                              src=src_static_routing_intf + '[{}]'.format(key),
                              dest=dest_static_routing_intf + '[{}]'.format(key),
                              vrf=vrf_name)


            src_static_routing_hop = src_static_routing_route +'[next_hop][next_hop_list][(?P<index>.*)]'
            dest_static_routing_hop = 'info' + src_static_routing_hop

            req_key = ['index', 'active', 'next_hop', 'outgoing_interface', 'preference']
            for key in req_key:
                self.add_leaf(cmd='show ip static route vrf {vrf}'.format(vrf=vrf),
                              src=src_static_routing_hop + '[{}]'.format(key),
                              dest=dest_static_routing_hop + '[{}]'.format(key),
                              vrf=vrf_name)


            ##############################################
            ####            Ipv6                ##########

            self.add_leaf(cmd='show ipv6 static vrf {vrf} detail'.format(vrf=vrf),
                          src=src_static_routing_route + '[route]',
                          dest=dest_static_routing_route + '[route]',
                          vrf = vrf_name)

            req_key = ['outgoing_interface', 'active', 'preference']
            for key in req_key:
                self.add_leaf(cmd='show ipv6 static vrf {vrf} detail'.format(vrf=vrf),
                              src=src_static_routing_intf + '[{}]'.format(key),
                              dest=dest_static_routing_intf + '[{}]'.format(key),
                              vrf=vrf_name)


            req_key = ['index', 'active', 'next_hop', 'outgoing_interface', 'preference']
            for key in req_key:
                self.add_leaf(cmd='show ipv6 static vrf {vrf} detail'.format(vrf=vrf),
                              src=src_static_routing_hop + '[{}]'.format(key),
                              dest=dest_static_routing_hop + '[{}]'.format(key),
                              vrf=vrf_name)

        del self.list_of_vrfs
        self.make(final_call=True)

class StaticRoute(Base):
    # Keeping it for backward compatibility
    pass