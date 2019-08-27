''' 
Rip Genie Ops Object for IOSXE - CLI.
'''

# Genie
from genie.ops.base import Base

# iosxe parsers
from genie.libs.parser.iosxe.show_rip import ShowIpRipDatabase,\
                                             ShowIpv6RipDatabase,\
                                             ShowIpv6Rip
from genie.libs.parser.iosxe.show_protocols import ShowIpProtocolsSectionRip as  ShowIpProtocols,\
                                             ShowIpv6ProtocolsSectionRip as ShowIpv6Protocols
# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class Rip(Base):
    '''Rip Genie Ops Object'''

    def keys(self, item):
        if isinstance(item, dict):
            return list(item.keys())
        return []

    def learn(self):
        '''Learn Rip object'''

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

            # Place holder to make it more readable
            ########################################################################
            #####################              Ipv4                #################
            # IPV4
            # vrf
            #   af
            #     instance
            #         originate_default_route    N/A
            #         default_metric
            #         distance
            #         triggered_update_threshold        N/A
            #         maximum_paths
            #         output_delay
            #         distribute_list   N/A
            #         redistribute
            #                redistribute
            #                     metric
            #                     route_policy
            #         timers
            #             update_interval
            #             invalid_interval
            #             holddown_interval
            #             flush_intervalit
            #         interfaces
            #             interface
            #                authentication     N/A
            #                bfd                N/A
            #                cost               N/A
            #                neighbors          N/A
            #                no_listen                    N/A
            #                originate_default_route      N/A
            #                passive
            #                split_horizon                N/A
            #                summary_address
            #                      metric                 N/A
            #                timers                       N/A 
            #                oper_status                  N/A
            #                next_full_update             N/A
            #                valid_address                N/A
            #                statistics                   N/A
            #         next_triggered_update               N/A
            #         num_of_routes                       N/A
            #         neighbors
            #             address
            #                  last_update
            #                  bad_packets_rcvd              N/A
            #                  bad_routes_rcvd               N/A
            #         routes
            #             prefix
            #                 index
            #                     next_hop
            #                     interface
            #                     redistributed
            #                     route_type
            #                     summary_type
            #                     metric
            #                     expire_time                N/A
            #                     deleted                    N/A
            #                     holddown                   N/A
            #                     need_triggered_update      N/A
            #                     inactive                   N/A
            #                     flush_expire_before_holddown             N/A
            #         statistics                     N/A
            #
            src_instance = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)][instance][(?P<instance>.*)]'
            dest_instance = 'info[vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)][instance][(?P<instance>.*)]'

            src_protocol = '[protocols][rip][vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)][instance][(?P<instance>.*)]'


            req_key = ['distance','maximum_paths','output_delay']
            for key in req_key:
                self.add_leaf(cmd=ShowIpProtocols,
                          src=src_protocol + '[{}]'.format(key),
                          dest=dest_instance + '[{}]'.format(key),
                          vrf=vrf_name)

            self.add_leaf(cmd=ShowIpProtocols,
                          src=src_protocol + '[default_redistribution_metric]',
                          dest=dest_instance + '[default_metric]',
                          vrf=vrf_name)

            src_redistribute = src_protocol + '[redistribute][(?P<redistribute>.*)]'
            dest_redistribute = dest_instance + '[redistribute][(?P<redistribute>.*)]'

            self.add_leaf(cmd=ShowIpProtocols,
                          src=src_redistribute,
                          dest=dest_redistribute,
                          vrf=vrf_name)

            req_key = ['metric', 'route_policy']
            for key in req_key:
                self.add_leaf(cmd=ShowIpProtocols,
                              src=src_redistribute + '[{}]'.format(key),
                              dest=dest_redistribute + '[{}]'.format(key),
                              vrf=vrf_name)

            src_interface = src_protocol + '[interfaces][(?P<interface>.*)]'
            dest_interface = dest_instance + '[interfaces][(?P<interface>.*)]'

            self.add_leaf(cmd=ShowIpProtocols,
                          src=src_interface + '[passive]',
                          dest=dest_interface + '[passive]',
                          vrf=vrf_name)

            self.add_leaf(cmd=ShowIpProtocols,
                          src=src_interface + '[summary_address][(?P<summary_address>).*]',
                          dest=dest_interface + '[summary_address][(?P<summary_address>).*]',
                          vrf=vrf_name)


            src_route = src_instance + '[routes][(?P<prefix>.*)][index][(?P<index>.*)]'
            dest_route = dest_instance + '[routes][(?P<prefix>.*)][index][(?P<index>.*)]'

            req_key = ['summary_type','redistributed','next_hop','metric','interface','route_type']
            for key in req_key:
                self.add_leaf(cmd='show ip rip database vrf {vrf}'.format(vrf=vrf),
                              src=src_route + '[{}]'.format(key),
                              dest=dest_route + '[{}]'.format(key),
                              vrf=vrf_name)
            ###################################################################################
            #####################               Ipv6                          #################
            # IPV6
            # vrf
            #   af
            #     instance
            #         originate_default_route
            #                enabled
            #                route_policy           N/A
            #         default_metric                N/A
            #         distance
            #         split_horizon
            #         poison_reverse
            #         triggered_update_threshold        N/A
            #         maximum_paths
            #         output_delay              N/A
            #         distribute_list           N/A
            #         redistribute
            #                redistribute
            #                     metric
            #                     route_policy
            #         timers
            #             update_interval
            #             invalid_interval
            #             holddown_interval
            #             flush_interval
            #         interfaces
            #             interface
            #                authentication     N/A
            #                bfd                N/A
            #                cost               N/A
            #                neighbors          N/A
            #                no_listen                    N/A
            #                originate_default_route      N/A
            #                passive                      N/A
            #                split_horizon
            #                summary_address              N/A
            #                timers
            #                     update_interval
            #                     invalid_interval
            #                     holddown_interval
            #                     flush_interval
            #                oper_status                  N/A
            #                next_full_update             N/A
            #                valid_address                N/A
            #                statistics                   N/A
            #         next_triggered_update               N/A
            #         num_of_routes                       N/A
            #         neighbors
            #             address
            #                  last_update
            #                  bad_packets_rcvd              N/A
            #                  bad_routes_rcvd               N/A
            #         routes
            #             prefix
            #                 index
            #                     next_hop
            #                     interface
            #                     redistributed              N/A
            #                     route_type
            #                     summary_type               N/A
            #                     metric
            #                     expire_time                N/A
            #                     deleted                    N/A
            #                     holddown                   N/A
            #                     need_triggered_update      N/A
            #                     inactive                   N/A
            #                     flush_expire_before_holddown             N/A
            #         statistics                     N/A


            self.add_leaf(cmd=ShowIpv6Protocols,
                          src=src_instance ,
                          dest=dest_instance,
                          vrf=vrf_name)
            self.make()

            src_ipv6_redistribute = src_instance +'[redistribute][(?P<redistribute>.*)]'
            dest_ipv6_redistribute = dest_instance +'[redistribute][(?P<redistribute>.*)]'

            req_key = ['metric','route_policy']
            for key in req_key:
                self.add_leaf(cmd=ShowIpv6Protocols,
                              src=src_ipv6_redistribute + '[{}]'.format(key),
                              dest=dest_ipv6_redistribute + '[{}]'.format(key),
                              vrf=vrf_name)

            if hasattr(self, 'info'):
                for instance, value in self.info['vrf'][vrf]['address_family']['ipv6']['instance'].items():

                    src_ipv6 = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)]'

                    dest_ipv6 = 'info[vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)][instance]'\
                               '[{}]'.format(instance)

                    src_ipv6_timers = src_ipv6 + '[timers]'
                    dest_ipv6_timers = dest_ipv6 + '[timers]'

                    req_key = ['update_interval','invalid_interval','holddown_interval','flush_interval']
                    for key in req_key:
                        self.add_leaf(cmd='show ipv6 rip vrf {vrf}'.format(vrf=vrf),
                                      src=src_ipv6_timers + '[{}]'.format(key),
                                      dest=dest_ipv6_timers + '[{}]'.format(key),
                                      vrf=vrf_name)

                    req_key = ['split_horizon','poison_reverse','maximum_paths','distance']
                    for key in req_key:
                        self.add_leaf(cmd='show ipv6 rip vrf {vrf}'.format(vrf=vrf),
                                      src=src_ipv6 + '[{}]'.format(key),
                                      dest=dest_ipv6 + '[{}]'.format(key),
                                      vrf=vrf_name)

                    src_interface = src_ipv6 + '[interfaces][(?P<interface>.*)]'
                    dest_interface = dest_ipv6 + '[interfaces][(?P<interface>.*)]'

                    self.add_leaf(cmd='show ipv6 rip vrf {vrf}'.format(vrf=vrf),
                                  src=src_interface,
                                  dest=dest_interface,
                                  vrf=vrf_name)

                    self.add_leaf(cmd='show ipv6 rip vrf {vrf}'.format(vrf=vrf),
                                  src=src_ipv6 + '[originate_default_route]',
                                  dest=dest_ipv6 + '[originate_default_route]',
                                  vrf=vrf_name)

                    src_ipv6_route = src_ipv6 + '[routes][(?P<prefix>.*)][index][(?P<index>.*)]'
                    dest_ipv6_route = dest_ipv6 + '[routes][(?P<prefix>.*)][index][(?P<index>.*)]'

                    req_key = ['expire_time','next_hop','metric','interface','route_type']
                    for key in req_key:
                        self.add_leaf(cmd='show ipv6 rip vrf {vrf} database'.format(vrf=vrf),
                                      src=src_ipv6_route + '[{}]'.format(key),
                                      dest=dest_ipv6_route + '[{}]'.format(key),
                                      vrf=vrf_name)

        del self.list_of_vrfs
        self.make(final_call=True)
