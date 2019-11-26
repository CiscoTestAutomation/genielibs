''' 
IGMP Genie Ops Object for IOSXR - CLI.
'''

from genie.ops.base import Base
from genie.ops.base import Context

# iosxr show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail
from genie.libs.parser.iosxr.show_igmp import ShowIgmpInterface, ShowIgmpSummary, ShowIgmpGroupsDetail


class Igmp(Base):
    '''IGMP Genie Ops Object'''

    def keys(self, item):
        '''return only the key as list from the item'''
        if isinstance(item, dict):
            return sorted(list(item.keys()))

    def update_enable(self, item):
        '''update enable values to boolean'''
        if item == 'enabled':
            return True
        else:
            return False
            
    def learn(self):
        '''Learn IGMP Ops'''

        # get vrf list 
        # 'vrfs'
        #     vrf
        self.add_leaf(cmd=ShowVrfAllDetail,
                      src='',
                      dest='list_of_vrfs',
                      action=self.keys)
                      
        # 'vrfs'
        #     vrf
        #         ssm_map - N/A

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

            # skip the vrf when it is management
            if vrf == 'management':
                continue

            # create kwargs
            vrf_name = '' if vrf == 'default' else vrf
        
            ########################################################################
            #                               info
            ########################################################################
           
            # 'vrfs'
            #     vrf
            #         max_groups
            #         groups_count
            
            self.add_leaf(cmd=ShowIgmpSummary,
                            src='[vrf][(?P<vrf>.*)][maximum_number_of_groups_for_vrf]',
                            dest='info[vrfs][(?P<vrf>.*)][max_groups]',
                            vrf=vrf_name)
                            
            self.add_leaf(cmd=ShowIgmpSummary,
                            src='[vrf][(?P<vrf>.*)][no_of_group_x_interface]',
                            dest='info[vrfs][(?P<vrf>.*)][groups_count]',
                            vrf=vrf_name)
                      
            # 'interfaces'
            #     interface
            src = '[vrf][(?P<vrf>.*)][interfaces][(?P<interface>.*)]'
            dest = 'info[vrfs][(?P<vrf>.*)][interfaces][(?P<interface>.*)]'
            
            # enable
            self.add_leaf(cmd=ShowIgmpInterface,
                            src=src + '[igmp_state]',
                            dest=dest + '[enable]',
                            vrf=vrf_name,
                            action=self.update_enable)
            
            # oper_status
            self.add_leaf(cmd=ShowIgmpInterface,
                            src=src + '[oper_status]',
                            dest=dest + '[oper_status]',
                            vrf=vrf_name)
                              
            # last_member_query_interval
            self.add_leaf(cmd=ShowIgmpInterface,
                            src=src + '[last_member_query_response_interval]',
                            dest=dest + '[last_member_query_interval]',
                            vrf=vrf_name)
                          
            # query_max_response_time
            self.add_leaf(cmd=ShowIgmpInterface,
                            src=src + '[igmp_max_query_response_time]',
                            dest=dest + '[query_max_response_time]',
                            vrf=vrf_name) 
                          
            # query_interval
            self.add_leaf(cmd=ShowIgmpInterface,
                            src=src + '[igmp_query_interval]',
                            dest=dest + '[query_interval]',
                            vrf=vrf_name)
                           

            # version
            self.add_leaf(cmd=ShowIgmpInterface,
                            src=src + '[igmp_version]',
                            dest=dest + '[version]',
                            vrf=vrf_name)
                            
            # querier
            self.add_leaf(cmd=ShowIgmpInterface,
                            src=src + '[igmp_querying_router]',
                            dest=dest + '[querier]',
                            vrf=vrf_name)
                            
            # max_groups
            self.add_leaf(cmd=ShowIgmpSummary,
                            src=src + '[max_groups]',
                            dest=dest + '[max_groups]',
                            vrf=vrf_name)
            
            # 'interfaces'
            #     interface
            #         join_group - N/A
            #         static_group - N/A
            #         joined_group - N/A
            #         robustness_variable - N/A
            #         immediate_leave - N/A
            #         group_policy - N/A
                                                                              
            # interface
            #     group
            #         mcast_group
            #             up_time
            #             last_reporter
            req_keys = ['[group][(?P<group>.*)][up_time]',
                        '[group][(?P<group>.*)][last_reporter]',
                        ]
            for key in req_keys:
                self.add_leaf(cmd=ShowIgmpGroupsDetail,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              vrf=vrf_name)
                              
            # interface
            #     group
            #         mcast_group
            #             source
            #                 expire
            #                 up_time
            self.add_leaf(cmd=ShowIgmpGroupsDetail,
                            src=src + '[group][(?P<group>.*)][source]',
                            dest=dest + '[group][(?P<group>.*)][source]',
                            vrf=vrf_name)
         
            req_keys = ['[group][(?P<group>.*)][source][(?P<source>.*)][up_time]',
                        '[group][(?P<group>.*)][source][(?P<source>.*)][expire]',
                        ]
            for key in req_keys:
                self.add_leaf(cmd=ShowIgmpGroupsDetail,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              vrf=vrf_name)
                            
            # expire - N/A
            # host_count - N/A
            # host - N/A
            
            # interface
            #         group
            #             mcast_group
            #                 source
            #                     source
            #                         last_reporter - N/A
                                        
            # make to write in cache
            self.make()
            
            if not hasattr(self, 'info'):
                continue

            if 'vrfs' not in self.info:
                continue
            
            if 'interfaces' not in self.info['vrfs'][vrf]:
                continue
          
            src = '[vrf][(?P<vrf>.*)]'
            dest = 'info[vrfs][(?P<vrf>.*)]'

            for intf in self.info['vrfs'][vrf]['interfaces']:
                if 'group' not in self.info['vrfs'][vrf]['interfaces'][intf]:
                    continue

            # make to write in cache
            self.make(final_call=True)
