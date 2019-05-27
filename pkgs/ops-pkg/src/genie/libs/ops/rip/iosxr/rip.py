"""
Rip Genie Ops Object for IOSXR - CLI
"""
# Genie
from genie.ops.base import Base

# IOSXR Parsers
from genie.libs.parser.iosxr.show_rip import ShowRip, \
                                             ShowRipStatistics, \
                                             ShowRipDatabase, \
                                             ShowRipInterface
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail


class Rip(Base):
    """Rip Genie Ops Object"""

    def keys(self, item):
        if isinstance(item, dict):
            return list(item.keys())

    def check_metric(self, item):
        try:
            return int(item)
        except ValueError:
            pass

    def lower_case(self, item):
        return item.lower()

    def learn(self):
        """Learn Rip Object"""

        # get vrf list
        self.add_leaf(cmd=ShowVrfAllDetail,
                      src='',
                      dest='list_of_vrfs',
                      action=self.keys)

        # If show vrf returns nothing make initial vrf list
        try:
            self.make()
        except Exception:
            self.list_of_vrfs = []

        # incase attributes are specified that show vrf won't be executed
        if not hasattr(self, 'list_of_vrfs'):
            self.list_of_vrfs = []

        for vrf in self.list_of_vrfs + ['default']:
            vrf_name = '' if vrf == 'default' else vrf

            ###################################################################
            ###################################################################
            #   vrf
            #       af
            #           instance
            #               originate_default_route                         N/A
            #               default_metric
            #               split_horizon                                   N/A
            #               poison_reverse                                  N/A
            #               distance                                        N/A
            #               triggered_update_threshold                      N/A
            #               maximum_paths                                   
            #               output_delay                                    N/A
            #               distribute_list                                 N/A
            #               redistribute                                    N/A
            #               timers
            #                   update_interval
            #                   invalid_interval
            #                   holddown_interval
            #                   flush_interval
            #               interfaces
            #                    interface
            #                        authentication
            #                            auth_key_chain
            #                                key_chain
            #                            auth_key
            #                                key                            N/A
            #                                crypto_algorithm
            #                        bfd                                    N/A
            #                        cost
            #                        neighbors
            #                            address
            #                                address
            #                        no_listen                              N/A
            #                        originate_default_route                N/A
            #                        passive
            #                        split_horizon
            #                        poison_reverse
            #                        summary_address                        N/A
            #                        timers                                 N/A
            #                        oper_status
            #                        next_full_update                       N/A
            #                        valid_address                          N/A
            #                        statistics                             N/A
            #                next_triggered_update                          N/A
            #                num_of_routes                                  
            #                neighbors                                      N/A
            #                routes
            #                    route
            #                        index
            #                            next_hop
            #                            interface
            #                            redistributed
            #                            route_type
            #                            summary_type
            #                            metric
            #                            expire_time                        N/A
            #                            deleted                            N/A
            #                            holddown                           N/A
            #                            need_triggered_update              N/A
            #                            inactive
            #                            flush_expire_before_holddown       N/A
            #                statistics                                     N/A

            src_instance = '[vrf][(?P<vrf>.*)][address_family] \
                            [(?P<address_family>.*)][instance][(?P<instance>.*)]'
            dest_instance = 'info[vrf][(?P<vrf>.*)][address_family] \
                            [(?P<address_family>.*)][instance][(?P<instance>.*)]'
            self.add_leaf(cmd=ShowRip,
                          src=src_instance + '[default_metric]',
                          dest=dest_instance + '[default_metric]',
                          vrf=vrf_name,
                          action=self.check_metric)
            self.add_leaf(cmd=ShowRip,
                          src=src_instance + '[maximum_paths]',
                          dest=dest_instance + '[maximum_paths]',
                          vrf=vrf_name)
            
            self.make()
            if hasattr(self, 'info'):
                try:
                    if self.info['vrf'][vrf]['address_family']['ipv4']['instance']['rip']['default_metric'] is None:
                        self.info['vrf'][vrf]['address_family']['ipv4']['instance']['rip'].pop('default_metric', None)
                except KeyError:
                    pass

            src_instance_timers = src_instance + '[timers]'
            dest_instance_timers = dest_instance + '[timers]'
            req_key = ['[flush_interval]', '[holddown_interval]', '[invalid_interval]',
                       '[update_interval]']
            for key in req_key:
                self.add_leaf(cmd=ShowRip,
                            src=src_instance_timers + key,
                            dest=dest_instance_timers + key,
                            vrf=vrf_name)

            src_statistics = src_instance + '[statistics][routes_allocated]'
            dest_statistics = dest_instance + '[num_of_routes]'
            self.add_leaf(cmd=ShowRipStatistics,
                          src=src_statistics,
                          dest=dest_statistics,
                          vrf=vrf_name)

            src_database = src_instance + '[routes][(?P<route>.*)][index][(?P<index>.*)]'
            dest_database = dest_instance + '[routes][(?P<route>.*)][index][(?P<index>.*)]'
            req_key = ['[route_type]', '[metric]', '[interface]', '[next_hop]',
                       '[redistributed]', '[summary_type]', '[inactive]']
            for key in req_key:
                self.add_leaf(cmd=ShowRipDatabase,
                              src=src_database + key,
                              dest=dest_database + key,
                              vrf=vrf_name)

            src_interface = src_instance + '[interfaces][(?P<interface>.*)]'
            dest_interface = dest_instance + '[interfaces][(?P<interface>.*)]'
            req_key = ['[cost]', '[passive]', '[split_horizon]', '[poison_reverse]']
            for key in req_key:
                self.add_leaf(cmd=ShowRipInterface,
                              src=src_interface + key,
                              dest=dest_interface + key,
                              vrf=vrf_name)
            self.add_leaf(cmd=ShowRipInterface,
                          src=src_interface + '[oper_status]',
                          dest=dest_interface + '[oper_status]',
                          vrf=vrf_name,
                          action=self.lower_case)

            src_authentication = src_interface + '[authentication]'
            dest_authentication = dest_interface + '[authentication]'
            req_key = ['[auth_key_chain][key_chain]',
                       '[auth_key][crypto_algorithm]']
            for key in req_key:
                self.add_leaf(cmd=ShowRipInterface,
                              src=src_authentication + key,
                              dest=dest_authentication + key,
                              vrf=vrf_name)

            src_neighbors = src_interface + '[neighbors][(?P<neighbor>.*)][address]'
            dest_neighbors = dest_interface + '[neighbors][(?P<neighbor>.*)][address]'
            self.add_leaf(cmd=ShowRipInterface,
                          src=src_neighbors,
                          dest=dest_neighbors,
                          vrf=vrf_name)

        del self.list_of_vrfs
        self.make(final_call=True)
