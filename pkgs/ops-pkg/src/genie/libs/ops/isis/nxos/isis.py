'''
ISIS Genie Ops Object for NXOS - CLI.
'''

# Python
import re

# Genie
from genie.libs.ops.isis.isis import Isis as SuperIsis
from genie.libs.sdk.apis.utils import time_to_int

# iosxe parsers
from genie.libs.parser.nxos.show_isis import (ShowIsis,
                                              ShowIsisHostname,
                                              ShowIsisAdjacency,
                                              ShowIsisInterface,
                                              ShowIsisSpfLogDetail,
                                              ShowIsisDatabaseDetail,
                                              ShowIsisHostnameDetail)

class Isis(SuperIsis):
    '''Isis Genie Ops Object'''

    def get_enable(self, item):
        return True

    def get_passive(self, item):
        return True

    def get_metric_type(self, item):
        if 'wide' in item and 'narrow' in item:
            return 'both'
        elif 'wide' in item:
            return 'wide-only'
        elif 'narrow' in item:
            return 'old-only'
        return 'unknown'

    def get_topo(self, item):
        ret_dict = {}
        for topo, data in item.items():
            sub = ret_dict.setdefault(str(topo), {})
            sub.update({'topology': str(topo)})
            for af, af_dict in data.get('address_family', {}).items():
                default = af_dict.get('distance', 0)
                sub.setdefault('preference', {}).setdefault('coarse', {}).\
                    setdefault('default', default)
        return ret_dict

    def get_level_key(self, item):
        return 'level_' + str(item)

    def get_level_value(self, item):
        return 'level-' + str(item)

    def get_interface_level_type(self, item):
        mapping = {'L1':'level-1-only',
                   'L2':'level-2-only',
                   'L1-2':'level-1-2'}
        return mapping.get(item, '')

    def get_interface_topo(self, item):
        ret_dict = {}
        for key, data in item.items():
            sub_dict = ret_dict.setdefault(key, {})
            sub_dict.update({'name': key})
            lvl_dict = data.get('level', {})
            for lvl, value_dict in lvl_dict.items():
                sub = sub_dict.setdefault('metric', {}).\
                    setdefault('level_{}'.format(lvl), {})
                metric = value_dict.get('metric')
                sub.update({'metric': int(metric)})
        return ret_dict

    def to_int(self, item):
        return int(item)

    def to_list(self, item):
        return [item]
    
    def get_hold_timer(self, item):
        return time_to_int(item)

    def get_adj_state(self, item):
        return item.capitalize()

    def get_mt_entries(self,item):
        ret_dict = {}
        for entry, data in item.items():
            mt_id = str(entry)
            attributes = str(data.get('att'))

            sub_dict = ret_dict.setdefault(str(entry), {})
            sub_dict.update({'attributes':attributes, 'mt_id':mt_id})
        return ret_dict

    def get_mt_is_neighbor(self,item):
        mt_id = item.get('topo_id')
        if mt_id:
            item.update({'mt_id': str(mt_id)})
            try:
                del item['topo_id']
            except Exception:
                pass
        return item

    def get_extended_ipv4_reachability(self, item):
        ret_dict = {}
        for prefix, data in item.items():
            ip_prefix = prefix.split('/')[0]
            prefix_len = prefix.split('/')[-1]
            up_down = data.get('up_down').lower() == 'u'
            metric = data.get('metric')

            sub_dict = ret_dict.setdefault(prefix, {})
            sub_dict.update({'metric':metric, 'up_down':up_down,
                             'ip_prefix':ip_prefix, 'prefix_len':prefix_len})
        return ret_dict

    def get_mt_ipv6_reachability(self, item):
        ret_dict = {}
        for prefix, data in item.items():
            ip_prefix = prefix.split('/')[0]
            prefix_len = prefix.split('/')[-1]
            mt_id = data.get('topo_id')
            up_down = data.get('up_down').lower() == 'u'
            metric = data.get('metric')

            sub_dict = ret_dict.setdefault(prefix, {})
            sub_dict.update({'mt_id': str(mt_id), 'up_down':up_down,
                             'ip_prefix':ip_prefix, 'prefix_len':prefix_len,
                             'metric':metric})
        return ret_dict


    def learn(self, vrf='all'):
        '''Learn Isis object'''

        # Global callable
        self.callables = {'lk': self.get_level_key,
                          'lv': self.get_level_value}

        # Place holder to make it more readable
        # instance
        #   instance_id
        #     process_id
        #     vrf
        #       vrf
        #         vrf
        #         enable
        #         system_id
        #         area_address
        #         nsel                                              N/A
        #         maximum_area_addresses                            N/A
        #         mpls                                              N/A
        #         lsp_mtu
        #         lsp_lifetime                                      N/A
        #         lsp_refresh                                       N/A
        #         graceful_restart
        #           enable
        #           restart_interval                                N/A
        #         nsr                                               N/A
        #           enable                                          N/A
        #         authentication                                    N/A
        #         metric_type
        #           value
        #           level_1                                         N/A
        #           level_2                                         N/A
        #         default_metric                                    N/A
        #         overload                                          N/A
        #         fast_reroute                                      N/A
        #         spf_control                                       N/A
        #         spf_log                                           N/A
        #         lsp_log                                           N/A
        #         hostname_db
        #           hostname
        #             system_id
        #               hostname
        #         topologies
        #           topology
        #             topology
        #             local_rib                                     N/A
        #             preference
        #               detail                                      N/A
        #               coarse
        #                   default
        #         local_rib                                         N/A
        #         system_counters                                   N/A
        #         interfaces
        #           if_name
        #             name
        #             level_type
        #             lsp_pacing_interval
        #             lsp_retransmit_interval                       N/A
        #             passive
        #             hello_padding                                 N/A
        #             interface_type                                N/A
        #             tag                                           N/A
        #             hello_authentication                          N/A
        #             hello_interval
        #               interval                                    N/A
        #               level_1
        #                 interval
        #               level_2
        #                 interval
        #             hello_multiplier
        #               multiplier                                  N/A
        #               level_1
        #                 multiplier
        #               level_2
        #                 multiplier
        #             priority
        #               priority                                    N/A
        #               level_1
        #                 priority
        #               level_2
        #                 priority
        #             adjacencies
        #               neighbor_sysid
        #                 neighbor_snpa
        #                   neighbor_snpa
        #                     level
        #                       level
        #                         neighbor_systype                  N/A
        #                         neighbor_extended_circuit_id      N/A
        #                         hold_timer
        #                         neighbor_priority                 N/A
        #                         lastuptime                        N/A
        #                         state
        #             event_counters                                N/A
        #             topologies:                            
        #               if_topology
        #                 name
        #                 metric
        #                   metric                                  N/A
        #                   level_1
        #                     metric
        #                   level_2
        #                     metric
        #                 adjacencies                               N/A
        #             packet_counters                               N/A
        #               level                                       N/A
        #                 level                                     N/A
        #                   iih                                     N/A
        #                     in                                    N/A
        #                     out                                   N/A
        #                   ish                                     N/A
        #                     in                                    N/A
        #                     out                                   N/A
        #                   esh                                     N/A
        #                     in                                    N/A
        #                     out                                   N/A
        #                   lsp                                     N/A
        #                     in                                    N/A
        #                     out                                   N/A
        #                   psnp                                    N/A
        #                     in                                    N/A
        #                     out                                   N/A
        #                   csnp                                    N/A
        #                     in                                    N/A
        #                     out                                   N/A
        #             address_family                                N/A

        kwargs = {}
        kwargs.update({'vrf': vrf})

        # process_id
        kwargs.update({'cmd': ShowIsis})
        kwargs.update({'src': '[instance][(?P<instance>.*)][isis_process]'})
        kwargs.update({'dest': 'info[instance][(?P<instance>.*)][process_id]'})
        self.add_leaf(**kwargs)

        src_isis = '[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)]'
        dest_isis = 'info[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)]'

        # enable
        kwargs.update({'src': src_isis + '[vrf]'})
        kwargs.update({'dest': dest_isis + '[enable]'})
        kwargs.update({'action': self.get_enable})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        isis_keys = ['area_address', 'system_id', 'vrf']
        for key in isis_keys:
            kwargs.update({'src': src_isis + '[{}]'.format(key)})
            kwargs.update({'dest': dest_isis + '[{}]'.format(key)})
            self.add_leaf(**kwargs)

        # lsp_mtu
        kwargs.update({'src': src_isis + '[maximum_lsp_mtu]'})
        kwargs.update({'dest': dest_isis + '[lsp_mtu]'})
        self.add_leaf(**kwargs)

        src_graceful_restart = src_isis + '[graceful_restart]'
        dest_graceful_restart = dest_isis + '[graceful_restart]'

        graceful_restart_keys = ['enable']
        for key in graceful_restart_keys:
            kwargs.update({'src': src_graceful_restart + '[{}]'.format(key)})
            kwargs.update({'dest': dest_graceful_restart + '[{}]'.format(key)})
            self.add_leaf(**kwargs)

        # metric_type
        kwargs.update({'src': src_isis + '[metric_type][advertise]'})
        kwargs.update({'dest': dest_isis + '[metric_type][value]'})
        kwargs.update({'action': self.get_metric_type})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # topologies
        kwargs.update({'src': src_isis + '[topology]'})
        kwargs.update({'dest': dest_isis + '[topologies]'})
        kwargs.update({'action': self.get_topo})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # interface
        kwargs.update({'cmd': ShowIsisInterface})
        src_interface = src_isis + '[interfaces][(?P<interface>.*)]'
        dest_interface = dest_isis + '[interfaces][(?P<interface>.*)]'

        intf_dict = {'name':'name',
                     'lsp_interval_ms':'lsp_pacing_interval'}
        for src, dest in intf_dict.items():
            kwargs.update({'src': src_interface + src})
            kwargs.update({'dest': dest_interface + dest})
            self.add_leaf(**kwargs)

        # passive
        kwargs.update({'src': src_interface + '[passive]'})
        kwargs.update({'dest': dest_interface + '[passive]'})
        kwargs.update({'action': self.get_passive})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # level_type
        kwargs.update({'src': src_interface + '[circuit_type]'})
        kwargs.update({'dest': dest_interface + '[level_type]'})
        kwargs.update({'action': self.get_interface_level_type})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # hello_interval, hello_multiplier, priority
        hello_dict = {'hello':['hello_interval', 'interval'], 
                      'multi':['hello_multiplier', 'multiplier'], 
                      'pri':['priority', 'priority']}
        src_lvl = src_interface + '[levels][(?P<lk>{lk})][{src}]'
        dest_lvl = dest_interface + '[{dest}][(?P<lk>{lk})][{key}]'
        for src, dest in hello_dict.items():
            kwargs.update({'src': src_lvl.format(src=src, lk='{lk}')})
            kwargs.update({'dest': dest_lvl.format(dest=dest[0], key=dest[1], lk='{lk}')})
            kwargs.update({'action': self.to_int})
            self.add_leaf(**kwargs)
            kwargs.pop('action')

        # interface topologies
        src_topo = src_interface + '[topologies]'
        dest_topo = dest_interface + '[topologies]'
        kwargs.update({'src': src_topo})
        kwargs.update({'dest': dest_topo})
        kwargs.update({'action': self.get_interface_topo})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # adjacency
        src_adjacency = src_interface + '[adjacencies][(?P<adjacencies>.*)]' \
            '[neighbor_snpa][(?P<neighbor_snpa>.*)][level][(?P<lv>{lv})]'
        dest_adjacency = dest_interface + '[adjacencies][(?P<adjacencies>.*)]' \
            '[neighbor_snpa][(?P<neighbor_snpa>.*)][level][(?P<lv>{lv})]'

        kwargs.update({'cmd': ShowIsisAdjacency})

        # hold_timer
        kwargs.update({'src': src_adjacency + '[hold_time]'})
        kwargs.update({'dest': dest_adjacency + '[hold_timer]'})
        kwargs.update({'action': self.get_hold_timer})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # state
        kwargs.update({'src': src_adjacency + '[state]'})
        kwargs.update({'dest': dest_adjacency + '[state]'})
        kwargs.update({'action': self.get_adj_state})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # hostname
        src_hostname = src_isis + '[hostname_db][hostname]' \
            '[(?P<hostname>.*)][hostname]'
        dest_hostname = dest_isis + '[hostname_db][hostname]' \
            '[(?P<hostname>.*)][hostname]'
        kwargs.update({'cmd': ShowIsisHostnameDetail})
        kwargs.update({'src': src_hostname})
        kwargs.update({'dest': dest_hostname})
        self.add_leaf(**kwargs)

        self.make()

        # ===========================================================
        #                         lsdb
        # ===========================================================
        # instance
        #   process_id
        #     vrf
        #       vrf
        #         level_db
        #           level
        #             lsp_id
        #               decoded_completed                        N/A
        #               raw_data                                 N/A
        #               lsp_id
        #               checksum
        #               remaining_lifetime
        #               sequence
        #               attributes                               N/A
        #               ipv4_addresses
        #               ipv6_addresses
        #               ipv4_te_routerid                         N/A
        #               ipv6_te_routerid                         N/A
        #               protocol_supported                       N/A
        #               dynamic_hostname
        #               authentication                           N/A
        #               mt_entries
        #                 topology
        #                   mt_id
        #                   attributes
        #               router_capabilities                      N/A
        #               is_neighbor                              N/A
        #               extended_is_neighbor
        #                 neighbor
        #                   neighbor_id
        #                   metric
        #               ipv4_internal_reachability               N/A
        #               ipv4_external_reachability               N/A
        #               extended_ipv4_reachability
        #                 prefix
        #                   up_down
        #                   ip_prefix
        #                   prefix_len
        #                   metric
        #                   tag                                  N/A
        #                   tag64                                N/A
        #                   external_prefix_flag                 N/A
        #                   readvertisement_flag                 N/A
        #                   node_flag                            N/A
        #                   ipv4_source_router_id                N/A
        #                   ipv6_source_router_id                N/A
        #               mt_is_neighbor
        #                 neighbor
        #                   mt_id
        #                   neighbor_id
        #                   metric
        #               mt_extended_ipv4_reachability            N/A
        #               mt_ipv6_reachability
        #                 prefix
        #                   mt_id
        #                   up_down
        #                   ip_prefix
        #                   prefix_len
        #                   metric
        #                   tag                                  N/A
        #                   tag64                                N/A
        #                   external_prefix_flag                 N/A
        #                   readvertisement_flag                 N/A
        #                   node_flag                            N/A
        #                   ipv4_source_router_id                N/A
        #                   ipv6_source_router_id                N/A
        #               ipv6_reachability                        N/A

        src_level = src_isis + '[level_db][(?P<level_db>.*)][(?P<lsp_id>.*)]'
        dest_level = 'lsdb' + src_level
        key_dict = {'sequence':'sequence', 'checksum':'checksum', 'lsp_id':'lsp_id',
                    'lifetime':'remaining_lifetime', 'hostname':'dynamic_hostname'}
        
        kwargs.update({'cmd': ShowIsisDatabaseDetail})
        for key, value in key_dict.items():
            kwargs.update({'src': src_level + '[{}]'.format(key)})
            kwargs.update({'dest': dest_level + '[{}]'.format(value)})
            self.add_leaf(**kwargs)

        ip_dict = {'ip_address':'ipv4_addresses', 'ipv6_address': 'ipv6_addresses'}
        for key, value in ip_dict.items():
            kwargs.update({'src': src_level + '[{}]'.format(key)})
            kwargs.update({'dest': dest_level + '[{}]'.format(value)})
            kwargs.update({'action': self.to_list})
            self.add_leaf(**kwargs)
            kwargs.pop('action')

        # mt_entries
        entry_src = src_level + '[mt_entries]'
        entry_dest = dest_level + '[mt_entries]'
        kwargs.update({'src': entry_src})
        kwargs.update({'dest': entry_dest})
        kwargs.update({'action': self.get_mt_entries})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # extended_is_neighbor
        ext_nbr_src = src_level + '[extended_is_neighbor][(?P<nbr>.*)]'
        ext_nbr_dest = dest_level + '[extended_is_neighbor][(?P<nbr>.*)]'
        kwargs.update({'src': ext_nbr_src})
        kwargs.update({'dest': ext_nbr_dest})
        self.add_leaf(**kwargs)

        # mt_is_neighbor
        mt_nbr_src = src_level + '[mt_is_neighbor][(?P<nbr>.*)]'
        mt_nbr_dest = dest_level + '[mt_is_neighbor][(?P<nbr>.*)]'
        kwargs.update({'src': mt_nbr_src})
        kwargs.update({'dest': mt_nbr_dest})
        kwargs.update({'action': self.get_mt_is_neighbor})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # extended_ipv4_reachability
        ext_r_src = src_level + '[extended_ip]'
        ext_r_dest = dest_level + '[extended_ipv4_reachability]'
        kwargs.update({'src': ext_r_src})
        kwargs.update({'dest': ext_r_dest})
        kwargs.update({'action': self.get_extended_ipv4_reachability})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        # mt_ipv6_reachability
        mt_r_src = src_level + '[mt_ipv6_prefix]'
        mt_r_dest = dest_level + '[mt_ipv6_reachability]'
        kwargs.update({'src': mt_r_src})
        kwargs.update({'dest': mt_r_dest})
        kwargs.update({'action': self.get_mt_ipv6_reachability})
        self.add_leaf(**kwargs)
        kwargs.pop('action')

        self.make(final_call=True)
