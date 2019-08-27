''' 
Pim Genie Ops Object for IOSXE - CLI
'''
# super class
from genie.libs.ops.pim.pim import Pim as SuperPim

from genie.libs.parser.iosxe.show_mcast import ShowIpMroute,\
                                    ShowIpv6Mroute

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class Pim(SuperPim):
    '''Pim Genie Ops Object'''

    def transfer_to_bool(self, item):
        if item == 'enabled':
            return True
        else:
            return False

    def keys(self, item):
        if isinstance(item, dict):
            return sorted(list(item.keys()))

    def check_exists(self, item):
        if 'bidir' in item:
            return True
        else:
            return False


    def learn(self):
        '''Learn Pim Ops'''

        # get vrf list        
        self.add_leaf(cmd=ShowVrfDetail,
                      src='',
                      dest='list_of_vrfs',
                      action=self.keys)

        self.make()

        vrf_list = ['default']
        try:
            vrf_list.extend(self.list_of_vrfs)
        except:
            pass
        else:            
            # delete the list_of_vrfs in the info table
            del self.list_of_vrfs

        # loop for vrfs
        for vrf in sorted(vrf_list):

            # skip the vrf when it is mgmt-vrf
            if vrf == 'Mgmt-vrf':
                continue

            # create kwargs
            vrf_name = '' if vrf == 'default' else vrf
        
            ########################################################################
            #                               info
            ########################################################################

            # ---------      topology_tree_info     --------------
            # topology_tree_info
            #     --  group, , source_address, is_rpt, expiration
            #     --  incoming_interface, rpf_neighbor, rp_address
            #     -- msdp_learned, rp_bit
            #     -- mode is not supported on IOSXE
            
            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][multicast_group]'\
                  '[(?P<group>.*)][source_address][(?P<src>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][multicast_group]'\
                  '[(?P<group>.*)][source_address][(?P<src>.*)]'

            # up_time
            for cmd in [ShowIpMroute, ShowIpv6Mroute]:
                self.add_leaf(cmd=cmd, src=src, dest=dest, vrf=vrf_name)

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

                                self.info['vrf'][vrf]['address_family'][af]['topology_tree_info'] = {}

                            if 'multicast_group' not in self.info['vrf'][vrf]['address_family'][af]:
                                continue

                            for group in self.info['vrf'][vrf]['address_family'][af]['multicast_group']:

                                  for source in self.info['vrf'][vrf]['address_family']\
                                    [af]['multicast_group'][group]['source_address']:

                                      sub_dict = self.info['vrf'][vrf]['address_family']\
                                        [af]['multicast_group'][group]['source_address'][source]

                                      # create topo_tree
                                      is_rpt = True if source == '*' else False
                                      tp_tree = '{gr} {sr} {rpt}'.format(gr=group, sr=source, rpt=is_rpt)

                                      if tp_tree not in self.info['vrf'][vrf]['address_family'][af]['topology_tree_info']:
                                          self.info['vrf'][vrf]['address_family'][af]['topology_tree_info'][tp_tree] = {}

                                      tp_dict = self.info['vrf'][vrf]['address_family'][af]['topology_tree_info'][tp_tree]

                                      # group
                                      tp_dict['group'] = group
                                      # source_address
                                      tp_dict['source_address'] = source
                                      # is_rpt
                                      tp_dict['is_rpt'] = is_rpt

                                      # expiration
                                      try:
                                          tp_dict['expiration'] = sub_dict['expire']
                                      except:
                                          pass
                                      # incoming_interface
                                      try:
                                          tp_dict['incoming_interface'] = list(sub_dict['incoming_interface_list'].keys())[0]
                                      except:
                                          pass
                                      # rp_address
                                      try:
                                          tp_dict['rp_address'] = sub_dict['rp']
                                      except:
                                          pass
                                      # rpf_neighbor
                                      try:
                                          tp_dict['rpf_neighbor'] = sub_dict['rpf_nbr']
                                      except:
                                          pass
                                      # up_time
                                      try:
                                          tp_dict['up_time'] = sub_dict['uptime']
                                      except:
                                          pass
                                      # msdp_learned
                                      try:
                                          tp_dict['msdp_learned'] = sub_dict['msdp_learned']
                                      except:
                                          pass
                                      # rp_bit
                                      try:
                                          tp_dict['rp_bit'] = sub_dict['rp_bit']
                                      except:
                                          pass
                                      # outgoing_interface
                                      try:
                                        for intf in sub_dict['outgoing_interface_list']:
                                            if 'outgoing_interface' not in tp_dict:
                                                tp_dict['outgoing_interface'] = {}
                                            if intf not in tp_dict['outgoing_interface']:
                                                tp_dict['outgoing_interface'][intf] = {}
                                            tp_dict['outgoing_interface'][intf]['up_time'] = \
                                              sub_dict['outgoing_interface_list'][intf]['uptime']
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
            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][static_rp][(?P<static>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][static_rp[(?P<static>.*)]]'

            static_keys = ['[sm][policy_name]', '[sm][override]','[bidir]']

            for key in static_keys:
                self.add_leaf(cmd='show ip pim vrf {vrf} rp mapping'.format(vrf=vrf),
                              src=src + key,
                              dest=dest + key,
                              vrf=vrf_name)

            # autorp is not supported on IOSXE
            # listener is not supported on IOSXE


            # bsr
            #    bsr_candidate
            #     --  address, hash_mask_length, priority
            #     -- if_name, accept_rp_acl not supported on IOSXE
            #    bsr
            #     --  address, hash_mask_length, priority
            #     -- up_time, expires
            #
            #    election_state is not supported on IOSXE
            #
            #    bsr_next_bootstrap, rp_candidate_next_advertisement
            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr]'

            bsr_keys = ['[bsr_candidate][address]', '[bsr_candidate][hash_mask_length]',
                        '[bsr_candidate][priority]', '[bsr_next_bootstrap]',
                        '[bsr][address]', '[bsr][hash_mask_length]', '[bsr][priority]',
                        '[bsr][up_time]', '[bsr][expires]']

            for cmd in ['show ip pim vrf {vrf} bsr-router'.format(vrf=vrf), 'show ipv6 pim vrf {vrf} bsr election'.format(vrf=vrf)]:
                for key in bsr_keys:
                    self.add_leaf(cmd=cmd,
                                  src=src + key,
                                  dest=dest + key,
                                  vrf=vrf_name)

            # rp_candidate_next_advertisement
            self.add_leaf(cmd='show ipv6 pim vrf {vrf} bsr candidate-rp'.format(vrf=vrf),
                          src=src + '[rp_candidate_next_advertisement]',
                          dest=dest + '[rp_candidate_next_advertisement]',
                          vrf=vrf_name)

            # bsr
            #    rp
            #     --  rp_address, up_time, group_policy
            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr][rp]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr][rp]'
            self.add_leaf(cmd='show ip pim vrf {vrf} rp mapping'.format(vrf=vrf),
                          src=src,
                          dest=dest,
                          vrf=vrf_name)

            # bsr
            #    bsr_rp_candidate_interface|bsr_rp_candidate_address:
            #     --  address, interface, priority
            #     -- mode, interval
            #     -- policy, route_map, prefix_list are not supported on IOSXE

            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr][(?P<bsr>^(?![bsr]).*)]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][bsr][(?P<bsr>^(?![bsr]).*)]'
            bsr_keys = ['[address]', '[interface]', '[priority]',
                        '[mode]', '[interval]']

            for cmd in ['show ip pim vrf {vrf} bsr-router'.format(vrf=vrf), 'show ipv6 pim vrf {vrf} bsr candidate-rp'.format(vrf=vrf)]:
                for key in bsr_keys:
                    self.add_leaf(cmd=cmd,
                                  src=src + key,
                                  dest=dest + key,
                                  vrf=vrf_name)

            # rp_list
            #     --  address, mode, info_source_address
            #     --  info_source_type, up_time, expiration
            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_list][(?P<rp_list>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_list][(?P<rp_list>.*)]'

            rp_list_keys = ['[address]', '[mode]', '[info_source_address]',
                            '[info_source_type]', '[up_time]', '[expiration]']

            for key in rp_list_keys:
                self.add_leaf(cmd='show ip pim vrf {vrf} rp mapping'.format(vrf=vrf),
                              src=src + key,
                              dest=dest + key,
                              vrf=vrf_name)

            # rp_mappings
            #     --  group, rp_address, protocol
            #     --  up_time, expiration
            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_mappings][(?P<rp_map>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][rp][rp_mappings][(?P<rp_map>.*)]'

            rp_list_keys = ['[group]', '[rp_address]', '[protocol]',
                            '[up_time]', '[expiration]']

            for key in rp_list_keys:
                self.add_leaf(cmd='show ip pim vrf {vrf} rp mapping'.format(vrf=vrf),
                              src=src + key,
                              dest=dest + key,
                              vrf=vrf_name)


            # bidir
            #    df_election is not supported on IOSXE
            #
            #    interface_df_election
            #     --  address, interface_name, df_address
            #     --  interface_state is not supported on IOSXE
            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)]'\
                  '[rp][bidir][interface_df_election][(?P<df_key>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)]'\
                   '[rp][bidir][interface_df_election][(?P<df_key>.*)]'

            df_election_keys = ['[address]', '[interface_name]', '[df_address]']

            for key in df_election_keys:
                self.add_leaf(cmd='show ip pim vrf {vrf} interface df'.format(vrf=vrf),
                              src=src + key,
                              dest=dest + key,
                              vrf=vrf_name)           

            # asm
            #    anycast_rp, spt_switch, accept_register, register_source are not supported on IOSXE
            #    spt_switch, sg_expiry_timer are not supported on IOSXE
            # log_neighbor_changes  not supported on IOSXE


            # ---------      interfaces     --------------
            src = '[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)][address_family][(?P<af>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)][address_family][(?P<af>.*)]'

            # bfd, , hello_interval, jp_interval
            # address, dr_address, oper_status, bsr_border
            # dm, neighbor_filter, sm-passive
            # propagation_delay, override_interval, hello_expiration, bidir are not supported on IOSXE

            intf_keys = ['[bfd][enable]', '[hello_interval]', '[oper_status]',
                        '[jp_interval]', '[address]', '[bsr_border]',
                        '[neighbor_filter]', '[dm]', '[sm]']

            for key in intf_keys:
                self.add_leaf(cmd='show ip pim vrf {vrf} interface detail'.format(vrf=vrf),
                              src=src + key,
                              dest=dest + key,
                              vrf=vrf_name)

            # dr_priority
            self.add_leaf(cmd='show ip pim vrf {vrf} interface'.format(vrf=vrf),
                          src=src + '[dr_priority]',
                          dest=dest + '[dr_priority]',
                          vrf=vrf_name)

            # mode for dm under ssm
            self.add_leaf(cmd='show ip pim vrf {vrf} interface'.format(vrf=vrf),
                          src=src + '[mode]',
                          dest=dest + '[mode]',
                          vrf=vrf_name)

            # ipv6 interface
            src = '[vrf][(?P<vrf>.*)][interface][(?P<intf>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)][address_family][ipv6]'

            intf_keys = ['[hello_interval]', '[address]', '[dr_priority]']

            for key in intf_keys:
                self.add_leaf(cmd='show ipv6 pim vrf {vrf} interface'.format(vrf=vrf),
                              src=src + key,
                              dest=dest + key,
                              vrf=vrf_name)


            # ---------      neighbors     --------------
            src = '[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)]\
                   [address_family][(?P<af>.*)][neighbors][(?P<nei>.*)]'
            dest = 'info[vrf][(?P<vrf>.*)][interfaces][(?P<intf>.*)]\
                   [address_family][(?P<af>.*)][neighbors][(?P<nei>.*)]'
     
            # expiration, dr_priority, up_time
            # interface, bidir_capable
            # bfd_status, gen_id are not supported on IOSXE
            nei_keys = ['[expiration]', '[dr_priority]',
                        '[up_time]', '[interface]', '[bidir_capable]']

            for cmd in ['show ip pim neighbor', 'show ipv6 pim neighbor detail']:
                for key in nei_keys:
                    self.add_leaf(cmd=cmd,
                                  src=src + key,
                                  dest=dest + key,
                                  vrf=vrf_name)

        # make to write in cache
        self.make(final_call=True)

        # ---------      dm   --------------
        # ---------      bidir   -----------
        if hasattr(self, 'info'):
            if 'vrf' in self.info:
                for vrf in self.info['vrf']:
                    if 'interfaces' not in self.info['vrf'][vrf]:
                        continue
                    for intf in self.info['vrf'][vrf]['interfaces']:
                        if 'address_family' not in self.info['vrf'][vrf]\
                          ['interfaces'][intf]:
                            continue
                        for af in self.info['vrf'][vrf]\
                          ['interfaces'][intf]['address_family']:
                            if 'mode' in self.info['vrf'][vrf]\
                              ['interfaces'][intf]['address_family'] and \
                              'dense' in self.info['vrf'][vrf]\
                                ['interfaces'][intf]['address_family']['mode']:
                                try:
                                    self.info['vrf'][vrf]['address_family'][af]['dm'] = {}
                                except:
                                    pass

                                try:
                                    del(self.info['vrf'][vrf]['address_family']\
                                          ['interfaces'][intf]['address_family']['mode'])
                                except:
                                    pass

                            #  bidir
                            if af in self.info['vrf'][vrf]['address_family'] and \
                                'rp' in  self.info['vrf'][vrf]['address_family'][af] and \
                                'bidir' in self.info['vrf'][vrf]['address_family'][af]['rp']:
                                try:
                                    self.info['vrf'][vrf]['address_family'][af]['bidir'] = {}
                                except:
                                    pass

                            

