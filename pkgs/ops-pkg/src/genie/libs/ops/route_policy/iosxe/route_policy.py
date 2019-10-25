''' 
RoutePolicy Genie Ops Object for IOSXE - CLI.
'''

# Genie
from genie.libs.ops.route_policy.route_policy import RoutePolicy as SuperRoutePolicy


class RoutePolicy(SuperRoutePolicy):
    '''RoutePolicy Genie Ops Object'''

    def learn(self):
        '''Learn RoutePolicy Ops'''

        self.add_leaf(cmd='show route-map all',
                      src='[(?P<policy>.*)][description]',
                      dest='info[(?P<policy>.*)][description]')

        #####################################################################
        #                        Section "conditions"
        #####################################################################

        # Place holder to make it more readable
        cond_src = '[(?P<policy>.*)][statements][(?P<statements>.*)][conditions]'
        cond_dest = 'info[(?P<policy>.*)][statements][(?P<statements>.*)][conditions]'

        condition_keys = ['match_med_eq',\
            'match_nexthop_in',\
            'match_nexthop_in_v6', 'match_local_pref_eq',\
            'match_route_type', 'match_community_list',\
            'match_ext_community_list', 'match_as_path_list',\
            'match_level_eq', 'match_interface',\
            'match_prefix_list', 'match_prefix_list_v6', 'match_tag_list']

        for key in condition_keys:

            self.add_leaf(cmd='show route-map all',
                          src='{cond_src}[{key}]'.format(cond_src=cond_src,
                                                         key=key),
                          dest='{cond_dest}[{key}]'.format(cond_dest=cond_dest,
                                                           key=key))

        # # BGP
        # 'match_med_eq'
        # 'match_origin_eq' N/A
        # 'match_nexthop_in'
        # 'match_nexthop_in_v6'
        # 'match_local_pref_eq'
        # 'match_route_type'
        # 'match_community_list'
        # 'match_ext_community_list'
        # 'match_ext_community_list_type' N/A
        # 'match_as_path_list'
        # 'match_as_path_length' - N/A
        # 'match_as_path_length_oper' - N/A
        # # ISIS
        # 'match_level_eq'
        # # OSPF
        # 'match_area_eq' - N/A
        # # Other(Common)
        # 'match_interface'
        # 'match_prefix_list'
        # 'match_prefix_list_v6'
        # 'match_tag_list'

        #####################################################################
        #                        Section "actions"
        #####################################################################

        # Place holder to make it more readable
        cond_src = '[(?P<policy>.*)][statements][(?P<statements>.*)][actions]'
        cond_dest = 'info[(?P<policy>.*)][statements][(?P<statements>.*)][actions]'

        condition_keys = ['set_local_pref', 'set_next_hop',\
            'set_next_hop_v6', 'set_next_hop_self',\
            'set_as_path_prepend',\
            'set_as_path_prepend_repeat_n', 'set_community',\
            'set_community_no_export', 'set_community_no_advertise',\
            'set_community_additive', 'set_community_delete',\
            'set_ext_community_rt', 'set_ext_community_rt_additive',\
            'set_ext_community_soo', 'set_ext_community_vpn',\
            'set_ext_community_delete', 'set_level', 'set_metric_type',\
            'set_metric', 'route_disposition', 'set_tag', 'set_weight',\
            'actions', 'set_ospf_metric_type']

        for key in condition_keys:
            self.add_leaf(cmd='show route-map all',
                          src='{cond_src}[{key}]'.format(cond_src=cond_src,
                                                         key=key),
                          dest='{cond_dest}[{key}]'.format(cond_dest=cond_dest,
                                                           key=key))

            if key == 'set_metric':
                self.add_leaf(cmd='show route-map all',
                              src='{cond_src}[{key}]'.format(cond_src=cond_src,
                                                             key=key),
                              dest='{cond_dest}[{key}]'.format(cond_dest=cond_dest,
                                                               key='set_med'))
                self.add_leaf(cmd='show route-map all',
                              src='{cond_src}[{key}]'.format(cond_src=cond_src,
                                                             key=key),
                              dest='{cond_dest}[{key}]'.format(cond_dest=cond_dest,
                                                               key='set_ospf_metric'))

        # # BGP
        # 'set_local_pref'
        # 'set_next_hop'
        # 'set_next_hop_v6'
        # 'set_next_hop_self'
        # 'set_med'
        # 'set_as_path_prepend'
        # 'set_as_path_prepend_repeat_n'
        # 'set_community'
        # 'set_community_no_export'
        # 'set_community_no_advertise'
        # 'set_community_additive'
        # 'set_community_delete'
        # 'set_ext_community_rt'
        # 'set_ext_community_rt_additive'
        # 'set_ext_community_soo'
        # 'set_ext_community_vpn'
        # 'set_ext_community_delete'
        # 'set_ext_community_delete_type' - N/A
        # # ISIS
        # 'set_level'
        # 'set_metric_type'
        # 'set_metric'
        # # OSPF
        # 'set_ospf_metric_type'
        # 'set_ospf_metric'
        # # Other(Common)
        # 'route_disposition'
        # 'set_tag'
        # 'set_weight'
        # 'actions' - N/A

        self.make(final_call=True)

        # Delete 'clause' under every statement 'actions' key
        if hasattr(self, 'info'):
            for key in self.info:
              for key2 in self.info[key]['statements']:
                if 'clause' in self.info[key]['statements'][key2]['actions']:
                  del self.info[key]['statements'][key2]['actions']['clause']