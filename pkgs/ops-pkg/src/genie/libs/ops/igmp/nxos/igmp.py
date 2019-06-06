''' 
IGMP Genie Ops Object for NXOS - CLI.
'''
# super class
from genie.libs.ops.igmp.igmp import Igmp as SuperIgmp

# Parser
from genie.libs.parser.nxos.show_igmp import ShowIpIgmpInterface, \
                                  ShowIpIgmpGroups, \
                                  ShowIpIgmpLocalGroups


class Igmp(SuperIgmp):
    '''IGMP Genie Ops Object'''

    def learn(self):
        '''Learn IGMP Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        # max_groups
        self.add_leaf(cmd=ShowIpIgmpInterface,
                      src='[vrfs][(?P<vrf>.*)][groups_count]',
                      dest='info[vrfs][(?P<vrf>.*)][groups_count]',
                      vrf='all')

        # ssm_map is not supported on NXOS ops

        # Interface path
        src = '[vrfs][(?P<vrf>.*)][interface][(?P<interface>.*)]'
        dest = 'info[vrfs][(?P<vrf>.*)][interfaces][(?P<interface>.*)]'

        # interfaces
        #     --  enable, , group_policy, immediate_leave, version
        #     --  max_groups, query_interval, query_max_response_time
        #     --  oper_status, querier, robustness_variable
        # 
        # last_member_query_interval, joined_group are not supported on iosxe
        intf_req_keys = ['[enable]', '[immediate_leave]', '[robustness_variable]',
                         '[group_policy]', '[max_groups]', '[query_interval]',
                         '[query_max_response_time]', '[oper_status]',
                         '[querier]', '[version]']
        # interfaces
        #     --  join_group
        #         --  group, source
        #     --  static_group
        #         --  group, source
        local_groups_req_keys = ['[join_group][(?P<join_group>.*)][group]',
                                 '[join_group][(?P<join_group>.*)][source]',
                                 '[static_group][(?P<static_group>.*)][group]',
                                 '[static_group][(?P<static_group>.*)][source]']
        # interfaces
        #     --  group
        #         --  up_time, expire, source, last_reporter, source
        #         --  host_count, host are not supported on nxos
        groups_req_keys = ['[group][(?P<group>.*)][up_time]',
                           '[group][(?P<group>.*)][expire]',
                           '[group][(?P<group>.*)][last_reporter]',
                           '[group][(?P<group>.*)][source][(?P<source>.*)][up_time]',
                           '[group][(?P<group>.*)][source][(?P<source>.*)][expire]',
                           '[group][(?P<group>.*)][source][(?P<source>.*)][last_reporter]']

        # create cmd list dictionary
        req_dict = {ShowIpIgmpInterface: intf_req_keys,
                    ShowIpIgmpLocalGroups: local_groups_req_keys,
                    ShowIpIgmpGroups: groups_req_keys}

        for cmd, req_keys in req_dict.items():
            for key in req_keys:
                self.add_leaf(cmd=cmd,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              vrf='all')

        # make to write in cache
        self.make(final_call=True)