'''
ISIS Genie Ops Object for IOSXE - CLI.
'''

# Python
import re

# pyats
from pyats.utils.objects import find, R

# Genie
from genie.libs.ops.isis.isis import Isis as SuperIsis
from genie.libs.ops.utils.common import get_enable, to_int, to_list
from genie.libs.sdk.libs.utils.normalize import GroupKeys

# iosxe parsers
from genie.libs.parser.iosxe.show_isis import (ShowIsisLspLog,
                                               ShowIsisHostname,
                                               ShowRunSectionIsis,
                                               ShowIsisDatabaseDetail)

from genie.libs.parser.iosxe.show_clns import (ShowClnsTraffic,
                                               ShowClnsProtocol,
                                               ShowClnsInterface,
                                               ShowClnsNeighborsDetail,
                                               ShowClnsIsNeighborsDetail)

class Isis(SuperIsis):
    '''Isis Genie Ops Object'''

    def keys(self, item):
        key_dict = {}
        if isinstance(item, dict):
            for instance , v in item['instance'].items():
                for vrf , key in v['vrf'].items():
                    key_dict.update({instance:vrf})
            return key_dict

    def get_level_key(self, item):
        lvl = str(item).split('-')[-1]
        return 'level_' + lvl

    def get_level_value(self, item):
        return 'level-' + str(item)

    def get_levels_list(self, item):
        if item == 'none':
            return []
        r1 = re.compile(r'level-(?P<levels>\S+)')
        result = r1.match(item)
        if result:
            group = result.groupdict()
            level = [l for l in group['levels'].split('-')]
            return level

    def get_metric_type(self, item):
        ret_dict = {}
        generate_narrow_list = self.get_levels_list(item['generate_narrow'])
        accept_narrow_list = self.get_levels_list(item['accept_narrow'])
        generate_wide_list = self.get_levels_list(item['generate_wide'])
        accept_wide_list = self.get_levels_list(item['accept_wide'])

        all_levels = set([*generate_narrow_list, *accept_narrow_list, *generate_wide_list, *accept_wide_list])
        for level in all_levels:
            if ((level in generate_narrow_list and level in generate_wide_list) or 
                (level in accept_narrow_list and level in accept_wide_list)):
                metric_dict = ret_dict.setdefault('level_'+level, {})
                metric_dict['value'] = 'both'
            elif (level in generate_narrow_list or level in accept_narrow_list):
                metric_dict = ret_dict.setdefault('level_'+level, {})
                metric_dict['value'] = 'old-only'
            elif (level in generate_wide_list or level in accept_wide_list):
                metric_dict = ret_dict.setdefault('level_'+level, {})
                metric_dict['value'] = 'wide-only'
        return ret_dict

    def get_interfaces(self, item):
        ret_dict = {}
        for intf in item.keys():
            ret_dict.setdefault(intf, {})
        return ret_dict

    def get_lsp_log(self, item):
        ret_dict = {}
        lsp_log_index = 1
        for lvl, data in item.items():
            for idx,  log_dict in data.get('index', {}).items():
                when = log_dict['when']
                triggers = log_dict['triggers']
                sub_dict = ret_dict.setdefault(lsp_log_index, {})

                sub_dict.update({'id': lsp_log_index})
                sub_dict.update({'level': int(lvl)})
                sub_dict.update({'received_timestamp': when})
                sub_dict.update({'change': triggers})
                lsp_log_index += 1
        return ret_dict

    def get_spf_runs(self, item):
        ret_dict = {}
        for lvl, value in item.items():
            level = int(lvl.split('-')[-1])
            sub_dict = ret_dict.setdefault(level, {})
            sub_dict.update({'level': level, 'spf_runs': value})
        return ret_dict

    def get_hello_interval(self, item):
        if isinstance(item, dict):
            interval = item.get('next_is_is_lan_hello_in_ms') or item.get('next_is_is_lan_hello_in')
            return {'interval': interval}

    def get_lsp_id(self, item):
        ret_dict = {}
        for lsp_id, data in item.items():
            ret_dict.setdefault(lsp_id, {}).update({'lsp_id': lsp_id})
        return ret_dict

    def get_mt_entries(self,item):
        ret_dict = {}
        for entry, data in item.items():
            mt_id = entry
            attributes = data.get('code')

            sub_dict = ret_dict.setdefault(entry, {})
            sub_dict.update({'mt_id':mt_id})
            if attributes:
                sub_dict.update({'attributes':str(attributes)})
        return ret_dict

    def get_is_neighbor(self, item):
        ret_dict = {}
        for entry, data in item.items():
            sub_dict = ret_dict.setdefault(entry, {})
            neighbor_id = data.get('neighbor_id')
            metric = data.get('metric')
            sub_dict.update({'neighbor_id': neighbor_id,
                             'default_metric':metric})
        return ret_dict

    def get_ipv4_internal_reachability(self, item):
        ret_dict = {}
        for entry, data in item.items():
            sub_dict = ret_dict.setdefault(entry, {})
            ip_prefix = data.get('ip_prefix')
            prefix_len = data.get('prefix_len')
            metric = data.get('metric')

            sub_dict.update({'ip_prefix': ip_prefix})
            sub_dict.update({'prefix_len': prefix_len})
            sub_dict.update({'default_metric': metric})
        return ret_dict

    def get_adjacencies(self, tmp, instance, intf):
        ret_dict = {}
        mapping = {'L1':'level-1',
                   'L2':'level-2',
                   'L1L2':'level-all'}

        adj_dict = tmp.get('adjacencies', {}).get(instance, {})
        reqs = R(['(?P<nbr_id>.*)', '(?P<lvl>.*)', 'interface', intf])
        found = find([adj_dict], reqs, filter_=False, all_keys=True)

        if found:
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, source=found, all_keys=True)
            nbr_id = keys[0]['nbr_id']
            lvl = keys[0]['lvl']

            target = adj_dict[nbr_id][lvl]
            snpa = target.get('snpa', '')
            state = target.get('state', '')
            uptime = target.get('uptime', '')
            holdtime = target.get('holdtime')
            priority = target.get('priority')
            circuit_id = target.get('circuit_id', '')

            sub_dict = ret_dict.setdefault(nbr_id, {}).setdefault('neighbor_snpa', {}).\
                                setdefault(snpa, {}).setdefault('level', {}).\
                                setdefault(mapping.get(lvl), {})

            sub_dict.update({'neighbor_extended_circuit_id': circuit_id,
                             'hold_timer': holdtime, 'neighbor_priority': priority,
                             'lastuptime': uptime, 'state': state.capitalize()})
        return ret_dict

    def get_topologies(self, tmp, instance, intf):
        ret_dict = {}
        mapping = {'L1':'level-1',
                   'L2':'level-2',
                   'L1L2':'level-all'}

        adj_dict = tmp.get('adjacencies', {}).get(instance, {})
        reqs = R(['(?P<nbr_id>.*)', '(?P<lvl>.*)', 'interface', intf])
        found = find([adj_dict], reqs, filter_=False, all_keys=True)

        if found:
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, source=found, all_keys=True)
            nbr_id = keys[0]['nbr_id']
            lvl = keys[0]['lvl']

            target = adj_dict[nbr_id][lvl]
            snpa = target.get('snpa', '')
            state = target.get('state', '')
            uptime = target.get('uptime', '')
            holdtime = target.get('holdtime')
            priority = target.get('priority')
            circuit_id = target.get('circuit_id', '')
            topology = target.get('topology', [])

            for topo in topology:
                topo_dict = ret_dict.setdefault(topo, {})
                topo_dict.update({'name': topo})
                sub_dict = topo_dict.setdefault('adjacencies', {}).setdefault(nbr_id, {})\
                                    .setdefault('neighbor_snpa', {}).setdefault(snpa, {})\
                                    .setdefault('level', {}).setdefault(mapping.get(lvl), {})

                sub_dict.update({'neighbor_extended_circuit_id': circuit_id,
                                'hold_timer': holdtime, 'neighbor_priority': priority,
                                'lastuptime': uptime, 'state': state.capitalize()})
        return ret_dict


    def learn(self):
        '''Learn Isis object'''

        # Callables
        self.callables = {'lk': self.get_level_key,
                          'lv': self.get_level_value}

        # get instance:vrf dictionary
        self.add_leaf(cmd=ShowRunSectionIsis,
                      src='',
                      dest='instance_vrf',
                      action=self.keys)

        # initial vrf list
        self.make()

        if not hasattr(self, 'instance_vrf'):
            self.instance_vrf = {}

        # loop for vrfs
        if self.instance_vrf:
            for instance, vrf in self.instance_vrf.items():
                instance = instance or 'null'
    
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
                #         nsel
                #         maximum_area_addresses                               N/A
                #         mpls                                                 N/A
                #         lsp_mtu                                              N/A
                #         lsp_lifetime                                         N/A
                #         lsp_refresh                                          N/A
                #         graceful_restart                                     N/A
                #         nsr                                                  N/A
                #           enable                                             N/A
                #         authentication                                       N/A
                #         metric_type
                #           value                                              N/A
                #           level_1
                #             value
                #           level_2
                #             value
                #         default_metric                                       N/A
                #         overload                                             N/A
                #           status                                             N/A
                #         fast_reroute                                         N/A
                #         spf_control                                          N/A
                #         spf_log                                              N/A
                #         lsp_log
                #           lsp_log_id
                #             id
                #             level
                #             lsp                                              N/A
                #             received_timestamp
                #             change
                #         hostname_db
                #           hostname
                #             system_id
                #               hostname
                #         topologies                                           N/A
                #         local_rib                                            N/A
                #         system_counters
                #           level
                #             level
                #             corrupted_lsps                                   N/A
                #             authentication_type_fails                        N/A
                #             authentication_fails                             N/A
                #             database_overload                                N/A
                #             own_lsp_purge                                    N/A
                #             manual_address_drop_from_area                    N/A
                #             max_sequence                                     N/A
                #             sequence_number_skipped                          N/A
                #             id_len_mismatch                                  N/A
                #             partition_change                                 N/A
                #             lsp_errors                                       N/A
                #             spf_runs
                #         interfaces
                #           if_name
                #             name
                #             level_type
                #             lsp_pacing_interval                              N/A
                #             lsp_retransmit_interval                          N/A
                #             passive                                          N/A
                #             hello_padding                                    N/A
                #             interface_type                                   N/A
                #             tag                                              N/A
                #             hello_authentication                             N/A
                #             hello_interval
                #               interval                                       N/A
                #               level_1
                #                 interval
                #               level_2
                #                 interval
                #             hello_multiplier                                 N/A
                #             priority
                #               priority                                       N/A
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
                #                         neighbor_systype                     N/A
                #                         neighbor_extended_circuit_id
                #                         hold_timer
                #                         neighbor_priority
                #                         lastuptime
                #                         state
                #             event_counters                                   N/A
                #             topologies
                #               if_topology
                #                 name
                #                 metric                                       N/A
                #                 adjacencies
                #                   neighbor_sysid
                #                     neighbor_snpa
                #                       neighbor_snpa
                #                         level
                #                           level
                #                             neighbor_systype                 N/A
                #                             neighbor_extended_circuit_id
                #                             hold_timer
                #                             neighbor_priority
                #                             lastuptime
                #                             state
                #             packet_counters                                  N/A
                #             address_family
                #               address_family
                #                 metric
                #                   metric                                     N/A
                #                   level_1
                #                     metric
                #                   level_2
                #                     metric
                #                 bfd                                          N/A
                #                 mpls                                         N/A
                #                 fast_reroute                                 N/A
    
                src_inst = '[instance][{instance}]'.format(instance=instance)
                dest_vrf = 'info[instance][{instance}][vrf][{vrf}]'.format(instance=instance,vrf=vrf)
    
                key_dict = {'system_id': 'system_id', 'nsel': 'nsel',
                            'manual_area_address': 'area_address'}
                for src, dest in key_dict.items():
                    self.add_leaf(cmd=ShowClnsProtocol,
                                  src=src_inst +'[{}]'.format(src),
                                  dest=dest_vrf + '[{}]'.format(dest))
    
                # enable
                self.add_leaf(cmd=ShowClnsProtocol,
                              src=src_inst,
                              dest=dest_vrf + '[enable]',
                              action=get_enable)
    
                # metric_type
                self.add_leaf(cmd=ShowClnsProtocol,
                              src=src_inst +'[metrics]',
                              dest=dest_vrf + '[metric_type]',
                              action=self.get_metric_type)
    
                # interfaces place holder
                self.add_leaf(cmd=ShowClnsProtocol,
                              src=src_inst +'[interfaces]',
                              dest=dest_vrf + '[interfaces]',
                              action=self.get_interfaces)
    
                # hostname_db
                db_tag = 'notag' if instance == 'null' else instance
                src_host = '[tag][{instance}][hostname_db][hostname][(?P<hostname>.*)][hostname]'.format(instance=db_tag)
                dest_host = 'info[instance][{instance}][vrf][{vrf}][hostname_db][hostname][(?P<hostname>.*)][hostname]'.format(instance=instance,vrf=vrf)
                self.add_leaf(cmd=ShowIsisHostname,
                              src=src_host,
                              dest=dest_host)
    
                # lsp_log
                src_lsp = '[tag][{instance}][lsp_log][level]'.format(instance=instance)
                dest_lsp = dest_vrf + '[lsp_log]'
                self.add_leaf(cmd=ShowIsisLspLog,
                              src=src_lsp,
                              dest=dest_lsp,
                              action=self.get_lsp_log)
    
                # system_counters: spf_runs
                src_spf_runs = '[tag][{instance}][IS-IS][spf_calculation]'.format(instance=instance)
                dest_spf_runs = dest_vrf + '[system_counters]'
                self.add_leaf(cmd=ShowClnsTraffic,
                              src=src_spf_runs,
                              dest=dest_spf_runs,
                              action=self.get_spf_runs)
    
                src_adj = '[tag][{instance}][system_id][(?P<system_id>.*)][type][(?P<type>.*)]'.format(instance=instance)
                dest_adj = 'tmp[adjacencies][{instance}][(?P<system_id>.*)][(?P<type>.*)]'.format(instance=instance)
                dest_topo = 'tmp[topologies][{instance}][(?P<system_id>.*)][(?P<type>.*)]'.format(instance=instance)
    
                # adjacencies temp
                self.add_leaf(cmd=ShowClnsNeighborsDetail,
                              src=src_adj,
                              dest=dest_adj)
    
                # topologies temp
                self.add_leaf(cmd=ShowClnsNeighborsDetail,
                              src=src_adj,
                              dest=dest_topo)
    
                key_list = {'circuit_id', 'priority'}
                for key in key_list:
                    self.add_leaf(cmd=ShowClnsIsNeighborsDetail,
                                  src=src_adj + '[{}]'.format(key),
                                  dest=dest_adj + '[{}]'.format(key))
    
                    self.add_leaf(cmd=ShowClnsIsNeighborsDetail,
                                  src=src_adj + '[{}]'.format(key),
                                  dest=dest_topo + '[{}]'.format(key))
                self.make()
    
                if hasattr(self, 'info'):
                    # process_id and vrf
                    self.info['instance'][instance].setdefault('process_id', instance)
                    self.info['instance'][instance]['vrf'][vrf].setdefault('vrf', vrf)
    
                    if 'interfaces' in self.info['instance'][instance]['vrf'][vrf]:
                        for intf in self.info['instance'][instance]['vrf'][vrf]['interfaces']:
                            # name
                            intf_dict = self.info['instance'][instance]['vrf'][vrf]['interfaces'][intf]
                            intf_dict.update({'name': intf})
    
                            # interfaces
                            src_intf = '[interfaces][{intf}][routing_protocol][(?P<pro>.*)][process_id][(?P<inst>.*)]'.format(intf=intf)
                            dest_intf = dest_vrf + '[interfaces][{intf}]'.format(intf=intf)
    
                            # level_type
                            self.add_leaf(cmd=ShowClnsInterface,
                                          src=src_intf + '[level_type]',
                                          dest=dest_intf + '[level_type]')
    
                            # hello_interval
                            src_hello_interval = src_intf + '[hello_interval][(?P<lk>{lk})]'
                            dest_hello_interval = dest_intf + '[hello_interval][(?P<lk>{lk})]'
                            key_dict = {'next_is_is_lan_hello_in': 'interval',
                                        'next_is_is_lan_hello_in_ms': 'interval'}
                            for src, dest in key_dict.items():
                                self.add_leaf(cmd=ShowClnsInterface,
                                              src=src_hello_interval + '[{}]'.format(src),
                                              dest=dest_hello_interval + '[{}]'.format(dest))
    
                            # priority
                            src_priority = src_intf + '[priority][(?P<lk>{lk})][priority]'
                            dest_priority = dest_intf + '[priority][(?P<lk>{lk})][priority]'
                            self.add_leaf(cmd=ShowClnsInterface,
                                          src=src_priority,
                                          dest=dest_priority)
    
                            # address_family: metric
                            dest_af = dest_vrf + '[interfaces][{interface}][address_family]'.format(interface=intf)
    
                            self.add_leaf(cmd=ShowClnsInterface,
                                          src=src_intf + '[(?P<lk>{lk})][ipv6_metric]',
                                          dest=dest_af + '[ipv6][metric][(?P<lk>{lk})][metric]')
    
                            self.add_leaf(cmd=ShowClnsInterface,
                                          src=src_intf + '[(?P<lk>{lk})][metric]',
                                          dest=dest_af + '[ipv4][metric][(?P<lk>{lk})][metric]')
    
                            if hasattr(self, 'tmp'):
                                adj_dict = self.get_adjacencies(self.tmp, instance, intf)
                                if adj_dict:
                                    intf_dict.update({'adjacencies': adj_dict})
    
                                topo_dict = self.get_topologies(self.tmp, instance, intf)
                                if topo_dict:
                                    intf_dict.update({'topologies': topo_dict})
    
    
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
                #               extended_ipv4_reachability               N/A
                #               mt_is_neighbor
                #                 neighbor
                #                   mt_id                                N/A
                #                   neighbor_id
                #                   metric
                #               mt_extended_ipv4_reachability            N/A
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
    
                src_level = '[tag][{instance}][level][(?P<level>.*)]'.format(instance=instance)
                dest_level = 'lsdb[instance][{instance}][vrf][{vrf}][level_db][(?P<level>.*)]'.format(instance=instance, vrf=vrf)
    
                # lsp_id
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_level,
                              dest=dest_level,
                              action=self.get_lsp_id)
    
                # lsp
                src_lsp = src_level + '[(?P<lspid>.*)]'
                dest_lsp = dest_level + '[(?P<lspid>.*)]'
    
                key_dict = {'lsp_sequence_num':'sequence',
                            'lsp_checksum': 'checksum',
                            'hostname': 'dynamic_hostname'}
                for key, value in key_dict.items():
                    self.add_leaf(cmd=ShowIsisDatabaseDetail,
                                  src=src_lsp + '[{}]'.format(key),
                                  dest=dest_lsp + '[{}]'.format(value))
    
                ip_dict = {'ip_address':'ipv4_addresses',
                           'ipv6_address': 'ipv6_addresses'}
                for key, value in ip_dict.items():
                    self.add_leaf(cmd=ShowIsisDatabaseDetail,
                                  src=src_lsp + '[{}]'.format(key),
                                  dest=dest_lsp + '[{}]'.format(value),
                                  action=to_list)
    
                # remaining_lifetime
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[lsp_holdtime]',
                              dest=dest_lsp + '[remaining_lifetime]',
                              action=to_int)
    
                # mt_entries
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[topology]',
                              dest=dest_lsp + '[mt_entries]',
                              action=self.get_mt_entries)
    
                # is_neighbor
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[is_neighbor]',
                              dest=dest_lsp + '[is_neighbor]',
                              action=self.get_is_neighbor)
    
                # extended_is_neighbor
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[extended_is_neighbor]',
                              dest=dest_lsp + '[extended_is_neighbor]')
    
                # mt_is_neighbor
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[mt_is_neighbor]',
                              dest=dest_lsp + '[mt_is_neighbor]')
    
                # ipv4_internal_reachability
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[ipv4_internal_reachability]',
                              dest=dest_lsp + '[ipv4_internal_reachability]',
                              action=self.get_ipv4_internal_reachability)
    
                # mt_ipv6_reachability
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[mt_ipv6_reachability]',
                              dest=dest_lsp + '[mt_ipv6_reachability]')
    
                # ipv6_reachability
                self.add_leaf(cmd=ShowIsisDatabaseDetail,
                              src=src_lsp + '[ipv6_reachability]',
                              dest=dest_lsp + '[ipv6_reachability]')

        try:
            del(self.instance_vrf)
        except Exception:
            pass
        try:
            del(self.tmp)
        except Exception:
            pass

        self.make(final_call=True)
