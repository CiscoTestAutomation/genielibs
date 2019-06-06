''' 
MLD Genie Ops Object for IOSXR - CLI.
'''

# super class
from genie.libs.ops.mld.mld import Mld as SuperMld

# Parser
from genie.libs.parser.iosxr.show_mld import ShowMldSummaryInternal, \
                                             ShowMldInterface, \
                                             ShowMldGroupsDetail

# iosxr show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail

class Mld(SuperMld):
    '''MLD Genie Ops Object'''

    def keys(self, item):
        '''return only the key as list from the item'''
        if isinstance(item, dict):
            return list(item.keys())

    def learn(self):
        '''Learn MLD Ops'''

        # get vrf list
        self.add_leaf(cmd = ShowVrfAllDetail,
                      src = '',
                      dest = 'list_of_vrfs',
                      action = self.keys)

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
        
            ####################################################################
            #                               info                               #
            ####################################################################

            # 'vrfs'
            #   vrf
            #     'groups_count'
            self.add_leaf(cmd = ShowMldInterface,
                          src = '[vrf][(?P<vrf>.*)][active_groups]',
                          dest = 'info[vrfs][(?P<vrf>.*)][groups_count]',
                          vrf = vrf_name)

            # Interface path
            intf_src = '[vrf][(?P<vrf>.*)][interface][(?P<interface>.*)]'
            intf_dest = 'info[vrfs][(?P<vrf>.*)][interfaces][(?P<interface>.*)]'

            # 'interfaces'
            #   interface
            #     'enable'
            #     'group_policy' - N/A
            #     'immediate_leave' - N/A
            #     'max_groups'
            #     'query_interval'
            #     'query_max_response_time'
            #     'robustness_variable' - N/A
            #     'version'
            #     'oper_status'
            #     'querier'
            #     'joined_group' - N/A
            for key in ['enable', 'max_groups', 'query_interval', 
                        'query_max_response_time', 'version', 
                        'oper_status', 'querier']:
                self.add_leaf(cmd = ShowMldInterface,
                              src = intf_src + '[{}]'.format(key),
                              dest = intf_dest + '[{}]'.format(key),
                              vrf = vrf_name)

            # 'interfaces'
            #   interface
            #     'join_group'
            #       'group'
            #       'source'
            #     'static_group'
            #       'group'
            #       'source'
            for key in ['group', 'source']:
                self.add_leaf(cmd = ShowMldGroupsDetail,
                              src = intf_src + '[join_group][(?P<join_group>.*)][{}]'.format(key),
                              dest = intf_dest + '[join_group][(?P<join_group>.*)][{}]'.format(key),
                              vrf = vrf_name)

                self.add_leaf(cmd = ShowMldGroupsDetail,
                              src = intf_src + '[static_group][(?P<static_group>.*)][{}]'.format(key),
                              dest = intf_dest + '[static_group][(?P<static_group>.*)][{}]'.format(key),
                              vrf = vrf_name)

            # 'group'
            #   mcast_group
            #     'expire'
            #     'filter_mode'
            #     'host_count' - N/A
            #     'up_time'
            #     'host' - N/A
            #     'last_reporter'
            for key in ['expire', 'filter_mode', 'up_time','last_reporter']:
                self.add_leaf(cmd = ShowMldGroupsDetail,
                              src = intf_src + '[group][(?P<group>.*)][{}]'.format(key),
                              dest = intf_dest + '[group][(?P<group>.*)][{}]'.format(key),
                              vrf = vrf_name)

            # 'group'
            #   mcast_group
            #     'source'
            #       source
            #         'expire'
            #         'up_time'
            #         'last_reporter' - N/A
            for key in ['expire', 'up_time']:
                self.add_leaf(cmd = ShowMldGroupsDetail,
                              src = intf_src + '[group][(?P<group>.*)][source][(?P<source>.*)][{}]'.format(key),
                              dest = intf_dest + '[group][(?P<group>.*)][source][(?P<source>.*)][{}]'.format(key),
                              vrf = vrf_name)


            # make to write in cache
            self.make(final_call = True)
