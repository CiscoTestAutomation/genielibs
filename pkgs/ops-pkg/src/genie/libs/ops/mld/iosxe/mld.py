''' 
MLD Genie Ops Object for IOSXE - CLI.
'''
# super class
from genie.libs.ops.mld.mld import Mld as SuperMld

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class Mld(SuperMld):
    '''MLD Genie Ops Object'''

    def keys(self, item):
        '''return only the key as list from the item'''        
        if isinstance(item, dict):
            return list(item.keys())

    def learn(self):
        '''Learn MLD Ops'''

        # get vrf list        
        self.add_leaf(cmd=ShowVrfDetail,
                      src='',
                      dest='list_of_vrfs',
                      action=self.keys)

        self.make()

        vrf_list = ['default']
        try:
            vrf_list.extend(self.list_of_vrfs)
        except AttributeError:
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

            # max_groups
            self.add_leaf(cmd='show ipv6 mld interface',
                          src='[vrf][(?P<vrf>.*)][max_groups]',
                          dest='info[vrfs][(?P<vrf>.*)][max_groups]',
                          vrf=vrf_name)

            # groups_count is not supported on IOSXE

            # Interface path
            src = '[vrf][(?P<vrf>.*)][interface][(?P<interface>.*)]'
            dest = 'info[vrfs][(?P<vrf>.*)][interfaces][(?P<interface>.*)]'

            # interfaces
            #     --  enable, group_policy
            #     --  max_groups, query_interval, query_max_response_time
            #     --  oper_status, querier, version
            # 
            # immediate_leave, robustness_variable, joined_group are not supported on iosxe
            req_keys = ['[enable]', 
                        '[group_policy]', '[max_groups]', '[query_interval]',
                        '[query_max_response_time]', '[oper_status]',
                        '[querier]', '[version]']
            for key in req_keys:
                self.add_leaf(cmd='show ipv6 mld interface',
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              vrf=vrf_name)

            # interfaces
            #     --  join_group
            #         --  group, source
            #     --  static_group
            #         --  group, source
            #     --  group
            #         --  up_time, expire, last_reporter, filter_mode, source
            #         --  host_count, host, source<last-reporter> are not supported on iosxe
            req_keys = ['[join_group][(?P<join_group>.*)]',
                        '[static_group][(?P<static_group>.*)]',
                        '[group][(?P<group>.*)][up_time]',
                        '[group][(?P<group>.*)][expire]',
                        '[group][(?P<group>.*)][filter_mode]',
                        '[group][(?P<group>.*)][last_reporter]',
                        '[group][(?P<group>.*)][source][(?P<source>.*)][up_time]',
                        '[group][(?P<group>.*)][source][(?P<source>.*)][expire]']
            for key in req_keys:
                self.add_leaf(cmd='show ipv6 mld groups detail',
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              vrf=vrf_name)

            # make to write in cache
            self.make()

            if not hasattr(self, 'info') or \
               'vrfs' not in self.info or \
               'interfaces' not in self.info['vrfs'][vrf]:
                continue

            src = '[vrf][(?P<vrf>.*)]'
            dest = 'info[vrfs][(?P<vrf>.*)]'

            for intf in self.info['vrfs'][vrf]['interfaces']:
                if 'group' not in self.info['vrfs'][vrf]['interfaces'][intf]:
                    continue

                for group in self.info['vrfs'][vrf]['interfaces'][intf]['group']:
                    # ssm_map
                    # group_range is not supported on iosxe
                    req_keys = ['[ssm_map][(?P<ssm_map>.*)][source_addr]',
                                '[ssm_map][(?P<ssm_map>.*)][group_address]']
                    for key in req_keys:
                        self.add_leaf(cmd='show ipv6 mld vrf {vrf} ssm-map {group}'.format(vrf=vrf, group=group),
                                      src=src + '[{}]'.format(key),
                                      dest=dest + '[{}]'.format(key),
                                      group=group, vrf=vrf_name)


            # make to write in cache
            self.make(final_call=True)