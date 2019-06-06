''' 
MLD Genie Ops Object for NXOS - CLI.
'''
# super class
from genie.libs.ops.mld.mld import Mld as SuperMld

# Parser
from genie.libs.parser.nxos.show_mld import ShowIpv6MldInterface, \
                                 ShowIpv6MldGroups, \
                                 ShowIpv6MldLocalGroups

class Mld(SuperMld):
    '''MLD Genie Ops Object'''

    def learn(self):
        '''Learn MLD Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        # max_groups, ssm_map is not supported on NXOS ops

        # groups_count
        self.add_leaf(cmd=ShowIpv6MldGroups,
                      src='[vrfs][(?P<vrf>.*)][groups_count]',
                      dest='info[vrfs][(?P<vrf>.*)][groups_count]',
                      vrf='all')

        # Interface path
        src = '[vrfs][(?P<vrf>.*)][interface][(?P<interface>.*)]'
        dest = 'info[vrfs][(?P<vrf>.*)][interfaces][(?P<interface>.*)]'

        # interfaces
        #     --  enable, , group_policy, immediate_leave, version
        #     --  max_groups, query_interval, query_max_response_time
        #     --  oper_status, querier, robustness_variable
        # 
        # joined_group are not supported on iosxe
        intf_req_keys = ['[enable]', '[immediate_leave]', '[robustness_variable]',
                         '[group_policy]', '[max_groups]', '[query_interval]',
                         '[query_max_response_time]', '[oper_status]',
                         '[querier]', '[version]']
        # interfaces
        #     --  join_group
        #         --  group, source
        #     --  static_group
        #         --  group, source
        local_groups_req_keys = ['[join_group][(?P<join_group>.*)]',
                                 '[static_group][(?P<static_group>.*)]']
        # interfaces
        #     --  group
        #         --  up_time, expire, source, last_reporter, source
        #         --  host_count, host are not supported on nxos
        #         --  filter_mode is not supproted on nxos
        groups_req_keys = ['[group][(?P<group>.*)][up_time]',
                           '[group][(?P<group>.*)][expire]',
                           '[group][(?P<group>.*)][last_reporter]',
                           '[group][(?P<group>.*)][source][(?P<source>.*)][up_time]',
                           '[group][(?P<group>.*)][source][(?P<source>.*)][expire]',
                           '[group][(?P<group>.*)][source][(?P<source>.*)][last_reporter]']

        # create cmd list dictionary
        req_dict = {ShowIpv6MldInterface: intf_req_keys,
                    ShowIpv6MldLocalGroups: local_groups_req_keys,
                    ShowIpv6MldGroups: groups_req_keys}

        for cmd, req_keys in req_dict.items():
            for key in req_keys:
                self.add_leaf(cmd=cmd,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              vrf='all')

        # make to write in cache
        self.make(final_call=True)