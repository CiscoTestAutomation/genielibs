'''
ISIS Genie Ops Object for IOSXR - CLI.
'''

# pyats
from pyats.utils.objects import find, R

# Genie
from genie.libs.ops.isis.isis import Isis as SuperIsis
from genie.libs.ops.utils.common import get_enable, to_int, to_list

# iosxr parsers
from genie.libs.parser.iosxr.show_isis import (ShowIsis,
                                               ShowIsisSpfLog,
                                               ShowIsisLspLog,
                                               ShowIsisHostname,
                                               ShowIsisAdjacency,
                                               ShowIsisInterface,
                                               ShowIsisStatistics,
                                               ShowIsisDatabaseDetail)

class Isis(SuperIsis):
    '''Isis Genie Ops Object'''

    def get_vrf(self, item):
        ret_dict = {}
        for vrf, data in item.items():
            ret_dict.setdefault(vrf, {}).update({'vrf': vrf})
        return ret_dict

    def get_topo(self, item):
        ret_dict = {}
        for topo, data in item.items():
            sub = ret_dict.setdefault(str(topo), {})
            sub.update({'topology': str(topo)})
            for vrf, vrf_dict in data.get('vrf', {}).items():
                default = vrf_dict.get('distance', 0)
                sub.setdefault('preference', {}).setdefault('coarse', {}).\
                    setdefault('default', default)
        return ret_dict

    def get_level(self, item):
        ret_dict = {}
        for lvl, data in item.items():
            level = 'level-' + str(lvl)
            ret_dict.setdefault(level, {}).update({'level': level})
        return ret_dict

    def get_level_key(self, item):
        return 'level_' + str(item)

    def get_level_value(self, item):
        return 'level-' + str(item)

    def get_interface_name(self, item):
        ret_dict = {}
        for intf, data in item.items():
            ret_dict.setdefault(intf, {}).update({'name': intf})
        return ret_dict

    def get_interface_level_type(self, item):
        mapping = {'level-1':'level-1-only',
                   'level-2':'level-2-only',
                   'level-1-2':'level-1-2',}
        return mapping.get(item) or item

    def get_interface_type(self, item):
        mapping = {'LAN':'broadcast',
                   'Loop':'loopback'}
        return mapping.get(item) or item

    def get_topo_name(self, item):
        ret_dict = {}
        for name, data in item.items():
            ret_dict.setdefault(name, {}).update({'name': name})
        return ret_dict

    def get_log_id(self, item):
        ret_dict = {}
        for log_id, data in item.items():
            ret_dict.setdefault(log_id, {}).update({'id': log_id})
        return ret_dict

    def get_lsp_id(self, item):
        ret_dict = {}
        for lsp_id, data in item.items():
            ret_dict.setdefault(lsp_id, {}).update({'lsp_id': lsp_id})
        return ret_dict

    def get_sfp_type(self, item):
        mapping = {'FSPF':'full',}
        return mapping.get(item) or item

    def get_state(self, item):
        return item.lower() != 'enabled'

    def get_adjacencies(self, item):
        ret_dict = {}
        reqs = R(['level','(?P<level>.*)','interfaces','(?P<intf>.*)','system_id','(?P<sys_id>.*)','(?P<data>.*)'])
        found = find([item], reqs, filter_=False, all_keys=True)
        if found:
            for (data, index) in found: 
                sysid = index[-1]
                level = index[1].lower()
                intf = data.get('interface', '')
                snpa = data.get('snpa', '')
                state = data.get('state', '')
                hold_timer = data.get('hold', '0')
                lastuptime = data.get('changed', '')

                sub_dict = ret_dict.setdefault('interfaces', {}).setdefault(intf, {})\
                                   .setdefault('adjacencies', {}).setdefault(sysid, {})\
                                   .setdefault('neighbor_snpa', {}).setdefault(snpa, {})\
                                   .setdefault('level', {}).setdefault(level, {})
                sub_dict.update({'state': state,
                                 'hold_timer': int(hold_timer),
                                 'lastuptime': lastuptime})
        return ret_dict

    def get_mt_entries(self,item):
        ret_dict = {}
        for entry, data in item.items():
            mt_id = entry
            attributes = data.get('attach_bit')

            sub_dict = ret_dict.setdefault(entry, {})
            sub_dict.update({'mt_id':mt_id})
            if attributes:
                sub_dict.update({'attributes':str(attributes)})
        return ret_dict

    def get_neighbor_id(self, item):
        ret_dict = {}
        for neighbor_id, data in item.items():
            ret_dict.setdefault(neighbor_id, {}).update({'neighbor_id': neighbor_id})
        return ret_dict

    def get_reachability_block(self, item):
        ret_dict = {}
        ip_prefix = item.get('ip_prefix')
        prefix_length = item.get('prefix_length')
        metric = item.get('metric')
        
        ret_dict.update({'ip_prefix': ip_prefix})
        ret_dict.update({'metric': int(metric)})
        if prefix_length:
            ret_dict.update({'prefix_len': prefix_length})
        return ret_dict

    def get_ipv4_internal_reachability(self, item):
        ret_dict = {}
        ip_prefix = item.get('ip_prefix')
        prefix_length = item.get('prefix_length')
        metric = item.get('metric')
        
        ret_dict.update({'ip_prefix': ip_prefix})
        ret_dict.update({'default_metric': int(metric)})
        if prefix_length:
            ret_dict.update({'prefix_len': prefix_length})
        return ret_dict


    def learn(self):
        '''Learn Isis object'''

        # Global callable
        self.callables = {'lk': self.get_level_key,
                          'lv': self.get_level_value}

        # Place holder to make it more readable
        # ===========================================================
        #                         info
        # ===========================================================
        # instance
        #   instance_id:
        #     process_id
        #     vrf
        #       vrf
        #         vrf
        #         enable
        #         system_id
        #         area_address
        #         nsel                                           N/A
        #         maximum_area_addresses                         N/A
        #         mpls                                           N/A
        #         lsp_mtu                                        N/A
        #         lsp_lifetime                                   N/A
        #         lsp_refresh                                    N/A
        #         graceful_restart                               N/A
        #         nsr                                            N/A
        #           enable                                       N/A
        #         authentication                                 N/A
        #         metric_type                                    N/A
        #         default_metric                                 N/A
        #         overload                                       N/A
        #           status                                       N/A
        #         fast_reroute                                   N/A
        #         spf_control                                    N/A
        #         spf_log
        #           spf_log_id
        #             id
        #             level
        #             spf_type
        #             start_timestamp
        #             schedule_timestamp                         N/A
        #             end_timestamp                              N/A
        #             trigger_lsp                                N/A
        #         lsp_log
        #           lsp_log_id
        #             id
        #             level
        #             received_timestamp
        #             lsp                                        N/A
        #             change                                     N/A
        #         hostname_db
        #           hostname
        #             system_id
        #               hostname
        #         topologies
        #           topology
        #             topology
        #             local_rib                                  N/A
        #             preference
        #               detail                                   N/A
        #               coarse
        #                   default
        #         local_rib                                      N/A
        #         system_counters                                N/A
        #         interfaces
        #           if_name
        #             name
        #             level_type
        #             lsp_pacing_interval
        #             lsp_retransmit_interval
        #             passive
        #             hello_padding                              N/A
        #             interface_type
        #             tag                                        N/A
        #             hello_authentication                       N/A
        #             hello_interval
        #               interval                                 N/A
        #               level_1
        #                 interval
        #               level_2
        #                 interval
        #             hello_multiplier
        #               multiplier                               N/A
        #               level_1
        #                 multiplier
        #               level_2
        #                 multiplier
        #             priority
        #               priority                                 N/A
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
        #                         neighbor_systype               N/A
        #                         neighbor_extended_circuit_id   N/A
        #                         hold_timer
        #                         neighbor_priority              N/A
        #                         lastuptime
        #                         state
        #             event_counters                             N/A
        #             topologies
        #               if_topology
        #                 name
        #                 metric
        #                   metric                               N/A
        #                   level_1
        #                     metric
        #                   level_2
        #                     metric
        #                 adjacencies                            N/A
        #             packet_counters
        #               level
        #                 level
        #                   level
        #                   iih                                  N/A
        #                   ish                                  N/A
        #                   esh                                  N/A
        #                   lsp
        #                     in
        #                     out
        #                   psnp
        #                     in
        #                     out
        #                   csnp
        #                     in
        #                     out
        #                   unknown                              N/A
        #             address_family                             N/A

        vrf = 'default'
        # process_id
        src_inst = '[instance][(?P<instance>.*)]'
        dest_inst = 'info' + src_inst
        self.add_leaf(cmd=ShowIsis,
                      src=src_inst + '[process_id]',
                      dest=dest_inst + '[process_id]')

        # vrf
        self.add_leaf(cmd=ShowIsis,
                      src=src_inst + '[vrf]',
                      dest=dest_inst + '[vrf]',
                      action=self.get_vrf)
        self.make()

        # enable
        src_vrf = src_inst + '[vrf][(?P<vrf>.*)]'
        dest_vrf = dest_inst + '[vrf][(?P<vrf>.*)]'
        self.add_leaf(cmd=ShowIsis,
                      src=src_vrf + '[system_id]',
                      dest=dest_vrf + '[enable]',
                      action=get_enable)

        # system_id
        self.add_leaf(cmd=ShowIsis,
                      src=src_vrf + '[system_id]',
                      dest=dest_vrf + '[system_id]')

        # area_address
        self.add_leaf(cmd=ShowIsis,
                      src=src_vrf + '[routing_area_address]',
                      dest=dest_vrf + '[area_address]')

        # interfaces place holder
        self.add_leaf(cmd=ShowIsis,
                      src=src_vrf + '[interfaces][(?P<intf>.*)]',
                      dest=dest_vrf + '[interfaces][(?P<intf>.*)]',
                      action=lambda x: {})

        # topologies
        self.add_leaf(cmd=ShowIsis,
                      src=src_vrf +'[topology]',
                      dest=dest_vrf + '[topologies]',
                      action=self.get_topo)

        # tmp
        src_tmp = '[instance][(?P<instance>.*)]'
        dest_tmp = 'tmp' + src_tmp

        # hostname_db
        src_host = '[isis][(?P<instance>.*)][vrf][(?P<vrf>.*)][level][(?P<level>.*)][system_id][(?P<sys_id>.*)][dynamic_hostname]'
        dest_host = dest_tmp + '[hostname_db][hostname][(?P<sys_id>.*)][hostname]'
        self.add_leaf(cmd=ShowIsisHostname,
                      src=src_host,
                      dest=dest_host)

        # lsp_log
        src_lsp = src_inst + '[lsp_log]'
        dest_lsp = dest_tmp + '[lsp_log]'

        # id
        self.add_leaf(cmd=ShowIsisLspLog,
                      src=src_lsp,
                      dest=dest_lsp,
                      action=self.get_log_id)

        keys = ['level', 'received_timestamp']
        for key in keys:
            self.add_leaf(cmd=ShowIsisLspLog,
                          src=src_lsp + '[(?P<id>.*)][{}]'.format(key),
                          dest=dest_lsp + '[(?P<id>.*)][{}]'.format(key))

        # spf_log
        src_spf = src_inst + '[address_family][(?P<af>.*)][spf_log]'
        dest_spf = dest_tmp + '[spf_log]'

        # id
        self.add_leaf(cmd=ShowIsisSpfLog,
                      src=src_spf,
                      dest=dest_spf,
                      action=self.get_log_id)

        keys_dict = {'level':'level', 'start_timestamp':'start_timestamp'}
        for src, dest in keys_dict.items():
            self.add_leaf(cmd=ShowIsisSpfLog,
                          src=src_spf + '[(?P<id>.*)][{}]'.format(src),
                          dest=dest_spf + '[(?P<id>.*)][{}]'.format(dest))

        # spf_type
        self.add_leaf(cmd=ShowIsisSpfLog,
                      src=src_spf + '[(?P<id>.*)][type]',
                      dest=dest_spf + '[(?P<id>.*)][spf_type]',
                      action=self.get_sfp_type)

        # interfaces_tmp
        src_name = src_tmp + '[interface]'
        dest_name = dest_tmp + '[interfaces]'

        # name
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_name,
                      dest=dest_name,
                      action=self.get_interface_name)

        src_intf = src_name + '[(?P<intf>.*)]'
        dest_intf = dest_name + '[(?P<intf>.*)]'

        # lsp_retransmit_interval
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[lsp_rexmit_queue_size]',
                      dest=dest_intf + '[lsp_retransmit_interval]')

        # level_type
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[circuit_type]',
                      dest=dest_intf + '[level_type]',
                      action=self.get_interface_level_type)

        # interface_type
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[media_type]',
                      dest=dest_intf + '[interface_type]',
                      action=self.get_interface_type)

        # passive
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[state]',
                      dest=dest_intf + '[passive]',
                      action=self.get_state)

        # lsp_pacing_interval
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[level][(?P<lvl>.*)][lsp_pacing_interval_ms]',
                      dest=dest_intf + '[lsp_pacing_interval]')

        # hello_interval
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[level][(?P<lk>{lk})][hello_interval_sec]',
                      dest=dest_intf + '[hello_interval][(?P<lk>{lk})][interval]')

        # hello_multiplier
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[level][(?P<lk>{lk})][hello_multiplier]',
                      dest=dest_intf + '[hello_multiplier][(?P<lk>{lk})][multiplier]')

        # priority
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[level][(?P<lk>{lk})][priority][local]',
                      dest=dest_intf + '[priority][(?P<lk>{lk})][priority]',
                      action=to_int)

        # adjacencies
        self.add_leaf(cmd=ShowIsisAdjacency,
                      src='[isis][(?P<instance>.*)][vrf][(?P<vrf>.*)]',
                      dest=dest_tmp,
                      action=self.get_adjacencies)

        # topologies
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[topology][(?P<topo>.*)][metric][level][(?P<lk>{lk})]',
                      dest=dest_intf + '[topologies][(?P<topo>.*)][metric][(?P<lk>{lk})][metric]')

        # name
        self.add_leaf(cmd=ShowIsisInterface,
                      src=src_intf + '[topology]',
                      dest=dest_intf + '[topologies]',
                      action=self.get_topo_name)

        # packet_counters
        src_pkt = '[isis][(?P<instance>.*)][interface][(?P<intf>.*)][level][(?P<lv>{lv})]'
        dest_pkt = dest_intf + '[packet_counters][level][(?P<lv>{lv})]'
        keys_dict = {'lsps_sourced': 'lsp', 'csnp': 'csnp', 'psnp': 'psnp'}
        for src, dest in keys_dict.items():
            # in
            self.add_leaf(cmd=ShowIsisStatistics,
                          src=src_pkt + '[{}][received]'.format(src),
                          dest=dest_pkt + '[{}][in]'.format(dest))
            # out
            self.add_leaf(cmd=ShowIsisStatistics,
                          src=src_pkt + '[{}][sent]'.format(src),
                          dest=dest_pkt + '[{}][out]'.format(dest))

        # level
        self.add_leaf(cmd=ShowIsisStatistics,
                      src='[isis][(?P<instance>.*)][interface][(?P<intf>.*)][level]',
                      dest=dest_intf + '[packet_counters][level]',
                      action=self.get_level)

        self.make()

        if hasattr(self,'info') and hasattr(self,'tmp'):
            for instance in self.info['instance']:
                for vrf in self.info['instance'][instance]['vrf']:
                    if 'interfaces' in self.info['instance'][instance]['vrf'][vrf]:
                        for interface in self.info['instance'][instance]['vrf'][vrf]['interfaces']:
                            # get interface dict from self.tmp
                            intf_dict = self.tmp.get('instance', {}).get(instance, {}).get('interfaces', {}).get(interface, {})
                            # get hostname_db dict from self.tmp
                            host_dict = self.tmp.get('instance', {}).get(instance, {}).get('hostname_db', {})
                            # get lsp_log dict from self.tmp
                            lsp_dict = self.tmp.get('instance', {}).get(instance, {}).get('lsp_log', {})
                            # get spf_log dict from self.tmp
                            spf_dict = self.tmp.get('instance', {}).get(instance, {}).get('spf_log', {})

                            if intf_dict:
                                self.info['instance'][instance]['vrf'][vrf]['interfaces'][interface].update(intf_dict)
                            if host_dict:
                                self.info['instance'][instance]['vrf'][vrf].update({'hostname_db': host_dict})
                            if lsp_dict:
                                self.info['instance'][instance]['vrf'][vrf].update({'lsp_log': lsp_dict})
                            if spf_dict:
                                self.info['instance'][instance]['vrf'][vrf].update({'spf_log': spf_dict})

        try:
            del(self.tmp)
        except Exception:
            pass


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
        #               is_neighbor
        #                 neighbor
        #                   neighbor_id
        #                   i_e                                  N/A
        #                   default_metric
        #                   delay_metric                         N/A
        #                   expense_metric                       N/A
        #                   error_metric                         N/A
        #               extended_is_neighbor
        #                 neighbor
        #                   neighbor_id
        #                   metric
        #               ipv4_internal_reachability
        #                 prefix
        #                   up_down                              N/A
        #                   i_e                                  N/A
        #                   ip_prefix
        #                   prefix_len
        #                   default_metric
        #                   delay_metric                         N/A
        #                   expense_metric                       N/A
        #                   error_metric                         N/A
        #               ipv4_external_reachability               N/A
        #               extended_ipv4_reachability
        #                 prefix
        #                   up_down                              N/A
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
        #               mt_extended_ipv4_reachability
        #                 prefix
        #                   mt_id                                N/A
        #                   up_down                              N/A
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
        #               mt_ipv6_reachability
        #                 prefix
        #                   mt_id                                N/A
        #                   up_down                              N/A
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
        #               ipv6_reachability
        #                 prefix
        #                   up_down                              N/A
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

        src_level = '[instance][(?P<instance>.*)][level][(?P<level>.*)][lspid]'
        dest_level = 'lsdb[instance][(?P<instance>.*)][vrf][{vrf}][level_db][(?P<level>.*)]'.format(vrf=vrf)

        # lspid
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=src_level,
                      dest=dest_level,
                      action=self.get_lsp_id)

        # lsp
        src_lsp = src_level + '[(?P<lspid>.*)]'
        dest_lsp = dest_level + '[(?P<lspid>.*)]'

        key_dict = {'seq_num':'sequence', 'checksum':'checksum',
                    'holdtime':'remaining_lifetime',}
        for key, value in key_dict.items():
            self.add_leaf(cmd=ShowIsisDatabaseDetail,
                          src=src_lsp + '[lsp][{}]'.format(key),
                          dest=dest_lsp + '[{}]'.format(value))

        ip_dict = {'ip_address':'ipv4_addresses', 'ipv6_address': 'ipv6_addresses'}
        for key, value in ip_dict.items():
            self.add_leaf(cmd=ShowIsisDatabaseDetail,
                          src=src_lsp + '[{}]'.format(key),
                          dest=dest_lsp + '[{}]'.format(value),
                          action=to_list)

        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=src_lsp + '[hostname]',
                      dest=dest_lsp + '[dynamic_hostname]')

        # mt_entries
        entry_src = src_lsp + '[mt_entries]'
        entry_dest = dest_lsp + '[mt_entries]'
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=entry_src,
                      dest=entry_dest,
                      action=self.get_mt_entries)

        # is_neighbor
        is_nbr_src = src_lsp + '[is_neighbor]'
        is_nbr_dest = dest_lsp + '[is_neighbor]'

         # neighbor_id
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=is_nbr_src,
                      dest=is_nbr_dest,
                      action=self.get_neighbor_id)

        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=is_nbr_src + '[(?P<nbr>.*)][metric]',
                      dest=is_nbr_dest + '[(?P<nbr>.*)][default_metric]')

        # extended_is_neighbor
        ext_nbr_src = src_lsp + '[extended_is_neighbor]'
        ext_nbr_dest = dest_lsp + '[extended_is_neighbor]'

        # neighbor_id
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=ext_nbr_src,
                      dest=ext_nbr_dest,
                      action=self.get_neighbor_id)

        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=ext_nbr_src + '[(?P<nbr>.*)][metric]',
                      dest=ext_nbr_dest + '[(?P<nbr>.*)][metric]')

        # mt_is_neighbor
        mt_nbr_src = src_lsp + '[mt_is_neighbor]'
        mt_nbr_dest = dest_lsp + '[mt_is_neighbor]'

        # neighbor_id
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=mt_nbr_src,
                      dest=mt_nbr_dest,
                      action=self.get_neighbor_id)

        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=mt_nbr_src + '[(?P<nbr>.*)]',
                      dest=mt_nbr_dest + '[(?P<nbr>.*)]')

        # extended_ipv4_reachability
        ext_ip_src = src_lsp + '[extended_ipv4_reachability][(?P<prefix>.*)]'
        ext_ip_dest = dest_lsp + '[extended_ipv4_reachability][(?P<prefix>.*)]'
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=ext_ip_src,
                      dest=ext_ip_dest,
                      action=self.get_reachability_block)

        # mt_ipv4_reachability
        mt_ip_src = src_lsp + '[mt_ipv4_reachability][(?P<prefix>.*)]'
        mt_ip_dest = dest_lsp + '[mt_extended_ipv4_reachability][(?P<prefix>.*)]'
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=mt_ip_src,
                      dest=mt_ip_dest,
                      action=self.get_reachability_block)

        # ipv4_internal_reachability
        ip_in_src = src_lsp + '[ipv4_reachability][(?P<prefix>.*)]'
        ip_in_dest = dest_lsp + '[ipv4_internal_reachability][(?P<prefix>.*)]'
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=ip_in_src,
                      dest=ip_in_dest,
                      action=self.get_ipv4_internal_reachability)

        # mt_ipv6_reachability
        mt_ipv6_src = src_lsp + '[mt_ipv6_reachability][(?P<prefix>.*)]'
        mt_ipv6_dest = dest_lsp + '[mt_ipv6_reachability][(?P<prefix>.*)]'
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=mt_ipv6_src,
                      dest=mt_ipv6_dest,
                      action=self.get_reachability_block)

        # ipv6_reachability
        ipv6_src = src_lsp + '[ipv6_reachability][(?P<prefix>.*)]'
        ipv6_dest = dest_lsp + '[ipv6_reachability][(?P<prefix>.*)]'
        self.add_leaf(cmd=ShowIsisDatabaseDetail,
                      src=ipv6_src,
                      dest=ipv6_dest,
                      action=self.get_reachability_block)

        self.make(final_call=True)
