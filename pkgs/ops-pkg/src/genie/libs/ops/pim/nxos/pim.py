''' 
PIM Genie Ops Object for NXOS - CLI.
'''
# super class
from genie.libs.ops.pim.pim import Pim as SuperPim

# Parser
from genie.libs.parser.nxos.show_pim import ShowIpPimInterface,\
                                 ShowIpv6PimVrfAllDetail,\
                                 ShowIpPimRp,\
                                 ShowIpPimGroupRange,\
                                 ShowIpPimVrfDetail,\
                                 ShowIpPimNeighbor,\
                                 ShowIpv6PimGroupRange,\
                                 ShowIpPimRoute,\
                                 ShowIpv6PimNeighbor,\
                                 ShowIpv6PimRoute,\
                                 ShowIpPimDf,\
                                 ShowIpv6PimDf,\
                                 ShowIpv6PimRp,\
                                 ShowIpv6PimInterface, \
                                 ShowIpPimPolicyStaticticsRegisterPolicy

from genie.libs.parser.nxos.show_feature import ShowFeature

from genie.libs.parser.nxos.show_mcast import ShowIpMrouteVrfAll, \
                                   ShowIpv6MrouteVrfAll


class Pim(SuperPim):
    '''Pim Genie Ops Object'''

    def transfer_to_bool(self, item):
        try:
            for inst in item:
                if item[inst]['state'] == 'enabled':
                    ret_val = True
                    break
                else:
                    ret_val = False
                    continue
        except:
            ret_val = False
        return ret_val

    def keys(self, item):
        return list(item.keys())

    def check_exists(self, item):
        if 'bidir' in item:
            return True
        else:
            return False


    def learn(self):
        '''Learn Pim Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        # feature_pim
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][pim][instance]',
                      dest='info[feature_pim]',
                      action=self.transfer_to_bool)

        # feature_pim6
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][pim6][instance]',
                      dest='info[feature_pim6]',
                      action=self.transfer_to_bool)

        # ---------      topology_tree_info     --------------

        # topology_tree_info path
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][topology_tree_info][(?P<topo>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][topology_tree_info][(?P<topo>.*)]'

        # topology_tree_info
        #     --  group, , source_address, is_rpt, expiration
        #     --  incoming_interface, rpf_neighbor, rp_address
        #     --  mode
        #
        #     -- msdp_learned, up_time, outgoing_interface will be learned from mroute
        # 
        topo_tree_keys = ['[group]', '[source_address]', '[is_rpt]',
                         '[expiration]', '[incoming_interface]', '[rpf_neighbor]',
                         '[rp_address]', '[mode]']

        for cmd in [ShowIpPimRoute, ShowIpv6PimRoute]:
            for key in topo_tree_keys:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')

        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][multicast_group]'\
              '[(?P<group>.*)][source_address][(?P<src>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][multicast_group]'\
              '[(?P<group>.*)][source_address][(?P<src>.*)]'
        mroute_keys = {'[uptime]': '[up_time]',
                       '[flags]': '[msdp_learned]',
                       '[outgoing_interface_list][(?P<intf>.*)]'\
                       '[oil_uptime]': '[outgoing_interface][(?P<intf>.*)][up_time]'}

        # up_time
        for cmd in [ShowIpMrouteVrfAll, ShowIpv6MrouteVrfAll]:
            for src_key, dest_key in mroute_keys.items():
                self.add_leaf(cmd=cmd,
                              src=src + src_key,
                              dest=dest + dest_key)

        # make to get the group and source address
        self.make()

        if hasattr(self, 'info'):
            if 'vrf' in self.info:
                for vrf in self.info['vrf']:
                    if 'address_family' not in self.info['vrf'][vrf]:
                        continue
                    for af in self.info['vrf'][vrf]['address_family']:
                        if 'topology_tree_info' not in \
                          self.info['vrf'][vrf]['address_family'][af]:
                            continue
                        for group_info in \
                          self.info['vrf'][vrf]['address_family'][af]['topology_tree_info']:

                            group, src_addr, is_rpt = group_info.split()

                            # up_time
                            # outgoing_interface - up_time
                            # msdp_learned
                            try:
                                ret = self.info['vrf'][vrf]['address_family'][af]\
                                      ['multicast_group'][group]['source_address'][src_addr]
                                if 'msdp' in self.info['vrf'][vrf]['address_family'][af]\
                                    ['multicast_group'][group]['source_address']\
                                        [src_addr]['msdp_learned']:
                                    self.info['vrf'][vrf]['address_family'][af]\
                                      ['multicast_group'][group]['source_address']\
                                          [src_addr]['msdp_learned'] = True
                                else:
                                    self.info['vrf'][vrf]['address_family'][af]\
                                      ['multicast_group'][group]['source_address']\
                                          [src_addr]['msdp_learned'] = False

                                self.info['vrf'][vrf]['address_family'][af]\
                                  ['topology_tree_info'][group_info].update(ret)
                            except:
                                pass
                        # delete none-used keys
                        try:
                            del(self.info['vrf'][vrf]['address_family'][af]\
                                  ['multicast_group'])
                        except:
                            pass


        # ---------      rp     --------------
        # static_rp
        #    sm
        #     --  policy_name, route_map
        #     -- override, policy, prefix_list are not supoorted on NXOS
        #    bidir
        #     --  policy_name, route_map
        #     -- override, policy, prefix_list are not supoorted on NXOS

        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][static_rp][(?P<s_rp>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][static_rp][(?P<s_rp>.*)]'

        for key in ['[sm]', '[bidir]']:
            for cmd in [ShowIpv6PimRp, ShowIpPimRp]:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')
        # autorp
        #    send_rp_announce
        #     --  group, scope, group_list, bidir
        #     --  route-map, prefix_list, interval are not supported on NXOS
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][autorp][send_rp_announce]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][autorp][send_rp_announce]'

        for key in ['[group]', '[scope]', '[group_list]', '[bidir]', '[rp_source]']:
            for cmd in [ShowIpv6PimRp, ShowIpPimRp]:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')

        # get address under atuorp for interface under send_rp_discover
        for cmd in [ShowIpv6PimRp, ShowIpPimRp]:        
            self.add_leaf(cmd=cmd,
                          src='[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][autorp][address]',
                          dest='info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][autorp][address]',
                          vrf='all')

        # autorp
        #     --  scope is not supported on NXOS
        #
        # listener  -- not supported on NXOS



        # bsr
        #    bsr_candidate
        #     --  address, hash_mask_length, priority
        #     -- if_name, accept_rp_acl are missing
        #    bsr
        #     --  address, hash_mask_length, priority
        #     -- up_time, expires
        #
        #    election_state not supported on NXOS
        #
        #    bsr_next_bootstrap
        #    rp
        #     -- rp_address, group_policy, up_time
        #     -- up_time, expires
        #    rp_candidate_next_advertisement
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr]'

        bsr_keys = ['[bsr_candidate][address]', '[bsr_candidate][hash_mask_length]',
                    '[bsr_candidate][priority]', '[bsr][address]', '[bsr][up_time]', 
                    '[bsr][address]', '[bsr][hash_mask_length]', '[bsr][priority]',
                    '[bsr][expires]', '[bsr_next_bootstrap]', '[rp]',
                    '[rp_candidate_next_advertisement]']

        for cmd in [ShowIpPimRp, ShowIpv6PimRp]:
            for key in bsr_keys:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')

        # bsr   
        #
        #    'bsr_rp_candidate_interface|bsr_rp_candidate_address
        #     --  address, policy, priority, mode
        #     --  hash_mask_length
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr][bsr_address][(?P<bsr>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr][(?P<bsr>.*)]'
        for cmd in [ShowIpPimRp, ShowIpv6PimRp]:
            self.add_leaf(cmd=cmd,
                          src=src,
                          dest=dest,
                          vrf='all')

        # rp_list
        #     --  address, mode, info_source_address
        #     --  info_source_type, up_time, expiration
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_list][(?P<rp_list>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_list][(?P<rp_list>.*)]'

        rp_list_keys = ['[address]', '[mode]', '[info_source_address]',
                        '[info_source_type]', '[up_time]', '[expiration]']

        for cmd in [ShowIpPimRp, ShowIpv6PimRp]:
            for key in rp_list_keys:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')

        # rp_mappings
        #     --  group, rp_address, protocol, up_time, expiration
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_mappings][(?P<rp_map>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_mappings][(?P<rp_map>.*)]'

        rp_map_keys = ['[group]', '[rp_address]', '[protocol]',
                        '[up_time]', '[expiration]']

        for cmd in [ShowIpPimRp, ShowIpv6PimRp]:
            for key in rp_map_keys:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')


        # bidir
        #    df_election    --- not supported on NXOS
        #
        #    interface_df_election
        #     --  address, interface_name, df_address, interface_state
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bidir]'\
                  '[interface_df_election][(?P<df_elec>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bidir]'\
                  '[interface_df_election][(?P<df_elec>.*)]'

        df_keys = ['[address]', '[interface_name]',
                   '[df_address]', '[interface_state]']

        for cmd in [ShowIpPimRp, ShowIpv6PimDf]:
            for key in df_keys:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')

        # ---------      sm     --------------
        # asm
        #    anycast_rp         
        #     --  anycast_address
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][sm][asm]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][sm][asm]'

        for cmd in [ShowIpPimRp, ShowIpv6PimRp]:
            self.add_leaf(cmd=cmd,
                          src=src + '[anycast_rp]',
                          dest=dest + '[anycast_rp]',
                          vrf='all')

        #    accept_register
        self.add_leaf(cmd=ShowIpPimPolicyStaticticsRegisterPolicy,
                      src=src + '[accept_register]',
                      dest=dest + '[accept_register]',
                      vrf='all')


        #    spt_switch
        #     --  policy_name   --- not support on NXOS
        #    register_source
        #    spt_switch
        #     --  policy_name   --- not support on NXOS
        #    sg_expiry_timer
        #     --  sg_list, infinity
        #     --  prefix_list is not support on NXOS
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][sm][asm]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][sm][asm]'

        asm_keys = ['[register_source]',
                    '[sg_expiry_timer][sg_list]',
                    '[sg_expiry_timer][infinity]']

        for key in asm_keys:
            self.add_leaf(cmd=ShowIpPimVrfDetail,
                          src=src + key,
                          dest=dest + key,
                          vrf='all')
        # ssm
        #    range_policy
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][sm][ssm]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][sm][ssm]'

        for cmd in [ShowIpPimGroupRange, ShowIpv6PimGroupRange]:
            self.add_leaf(cmd=cmd, src=src, dest=dest,
                          vrf='all')

        # dm is not supported on NXOS

        # ---------      bidir     --------------
        src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp]'
        dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][bidir]'

        for cmd in [ShowIpPimDf, ShowIpv6PimDf]:
            self.add_leaf(cmd=cmd, src=src, dest=dest,
                          vrf='all', action=self.check_exists)

        # log_neighbor_changes is missing


        # ---------      interfaces     --------------
        src = '[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)][address_family][(?P<af>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)][address_family][(?P<af>.*)]'

        # bfd, dr_priority, hello_interval, jp_interval
        # address, dr_address, oper_status, hello_expiration
        # sm, neighbor_filter, bsr_border
        #
        # propagation_delay, override_interval, dm, bidir missing

        intf_keys = ['[bfd][enable]', '[dr_priority]', '[hello_interval]',
                    '[jp_interval]', '[address]', '[oper_status]', '[bsr_border]',
                    '[hello_expiration]', '[sm][passive]', '[neighbor_filter]',
                    '[dr_address]', '[genid]']

        for cmd in [ShowIpPimInterface, ShowIpv6PimInterface]:
            for key in intf_keys:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')


        # ---------      neighbors     --------------
        src = '[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)]\
               [address_family][(?P<af>.*)][neighbors][(?P<nei>.*)]'
        dest = 'info[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)]\
               [address_family][(?P<af>.*)][neighbors][(?P<nei>.*)]'
 
        # bfd_status, expiration, dr_priority, up_time
        # interface, bidir_capable
        nei_keys = ['[bfd_status]', '[expiration]', '[dr_priority]',
                    '[up_time]', '[interface]', '[bidir_capable]']

        for cmd in [ShowIpPimNeighbor, ShowIpv6PimNeighbor]:
            for key in nei_keys:
                self.add_leaf(cmd=cmd,
                              src=src + key,
                              dest=dest + key,
                              vrf='all')
        # make to write in cache
        self.make(final_call=True)

        # gen_id
        if hasattr(self, 'info'):
            if 'vrf' in self.info:
                for vrf in self.info['vrf']:
                    if 'interfaces' not in self.info['vrf'][vrf]:
                        continue
                    for intf in self.info['vrf'][vrf]['interfaces']:
                        if 'address_family' not in self.info['vrf'][vrf]['interfaces'][intf]:
                            continue
                        for af in self.info['vrf'][vrf]['interfaces'][intf]['address_family']:

                            # autorp
                            #    send_rp_announce
                            #     --  interface
                            try:
                                rp_source = self.info['vrf'][vrf]['address_family'][af]\
                                      ['rp']['autorp']['send_rp_announce']['rp_source']

                                if rp_source in self.info['vrf'][vrf]['interfaces'][intf]\
                                      ['address_family'][af]['address']:
                                    self.info['vrf'][vrf]['address_family'][af]\
                                      ['rp']['autorp']['send_rp_announce']['interface'] = intf

                                    try:
                                        del(self.info['vrf'][vrf]['address_family'][af]\
                                                  ['rp']['autorp']['send_rp_announce']['rp_source'])
                                    except:
                                        pass
                            except:
                                pass
                            #    send_rp_discovery
                            #     --  interface
                            try:
                                address = self.info['vrf'][vrf]['address_family'][af]\
                                      ['rp']['autorp']['address']

                                if address in self.info['vrf'][vrf]['interfaces'][intf]\
                                      ['address_family'][af]['address']:
                                    if 'send_rp_discovery' not in self.info['vrf'][vrf]\
                                      ['address_family'][af]['rp']['autorp']:
                                        self.info['vrf'][vrf]['address_family'][af]\
                                      ['rp']['autorp']['send_rp_discovery'] = {}
                                    self.info['vrf'][vrf]['address_family'][af]\
                                      ['rp']['autorp']['send_rp_discovery']['interface'] = intf

                                    try:
                                        del(self.info['vrf'][vrf]['address_family'][af]\
                                                  ['rp']['autorp']['address'])
                                    except:
                                        pass
                            except:
                                pass


                            if 'neighbors' not in self.info['vrf'][vrf]['interfaces'][intf]\
                              ['address_family'][af]:
                                continue
                            for nei in self.info['vrf'][vrf]['interfaces'][intf]\
                              ['address_family'][af]['neighbors']:

                                # gen_id
                                try:
                                    self.info['vrf'][vrf]['interfaces'][intf]\
                                      ['address_family'][af]['neighbors'][nei]['gen_id'] = \
                                        self.info['vrf'][vrf]['interfaces'][intf]\
                                          ['address_family'][af]['genid']
                                except:
                                    pass

                            try:
                                del(self.info['vrf'][vrf]['interfaces'][intf]\
                                    ['address_family'][af]['genid'])
                            except:
                                pass