''' 
MCAST Genie Ops Object for NXOS - CLI.
'''
# super class
from genie.libs.ops.mcast.mcast import Mcast as SuperMacst

# nxos show_mcast
from genie.libs.parser.nxos.show_mcast import ShowIpMrouteVrfAll, ShowIpv6MrouteVrfAll,\
                                   ShowIpStaticRouteMulticast,\
                                   ShowIpv6StaticRouteMulticast

# nxos show_feature
from genie.libs.parser.nxos.show_feature import ShowFeature


class Mcast(SuperMacst):
    '''Mcast Genie Ops Object'''

    def set_enable(self, key):
        if key == 'enabled':
            return True

    def learn(self):
        '''Learn Mcast Ops'''

        ########################################################################
        #                               info
        ########################################################################

        # enable - pim
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][pim][instance][(?P<instance>.*)][state]',
                      dest='info[vrf][default][address_family][ipv4][enable]',
                      action=self.set_enable)
        
        # enable - pim6
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][pim6][instance][(?P<instance>.*)][state]',
                      dest='info[vrf][default][address_family][ipv6][enable]',
                      action=self.set_enable)

        # multipath - N/A

        # vrf
        #   vrf_name
        #     address_family
        #       af_name
        #         mroute
        #           address/prefix
        #             path
        #               path_name
        info_src_v4 = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>ipv4)][mroute][(?P<mroute>.*)][path][(?P<path>.*)]'
        info_dest_v4 = 'info' + info_src_v4
        info_src_v6 = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>ipv6)][mroute][(?P<mroute>.*)][path][(?P<path>.*)]'
        info_dest_v6 = 'info' + info_src_v6

        # neighbor_address
        # interface_name
        # admin_distance
        for key in ['neighbor_address', 'interface_name', 'admin_distance']:

            # ipv4 & ipv6
            for cmd, info_src, info_dest in [\
                (ShowIpStaticRouteMulticast, info_src_v4, info_dest_v4), 
                (ShowIpv6StaticRouteMulticast, info_src_v6, info_dest_v6)]:

                self.add_leaf(cmd=cmd,
                              src=info_src+'[{key}]'.format(key=key),
                              dest=info_dest+'[{key}]'.format(key=key))

        ########################################################################
        #                               table
        ########################################################################

        # vrf
        #   vrf_name
        #     address_family
        #       af_name
        #         multicast_group
        #           group_name
        #             source_address
        #               address_name
        tbl_src_v4 = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>ipv4)][multicast_group][(?P<mcast_group>.*)][source_address][(?P<source_address>.*)]'
        tbl_dest_v4 = 'table' + tbl_src_v4
        tbl_src_v6 = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>ipv6)][multicast_group][(?P<mcast_group>.*)][source_address][(?P<source_address>.*)]'
        tbl_dest_v6 = 'table' + tbl_src_v6

        # flags
        # uptime
        # incoming_interface_list
        # outgoing_interface_list
        for key in ['flags', 'uptime', 'incoming_interface_list', 'outgoing_interface_list']:

            # ipv4 & ipv6
            for cmd, tbl_src, tbl_dest in [\
                (ShowIpMrouteVrfAll, tbl_src_v4, tbl_dest_v4), 
                (ShowIpv6MrouteVrfAll, tbl_src_v6, tbl_dest_v6)]:

                if key == 'incoming_interface_list':
                     for key2 in ['rpf_nbr', 'rpf_info']:
                        self.add_leaf(cmd=cmd,
                                      src=tbl_src+'[incoming_interface_list][(?P<iil>.*)][{key2}]'.format(key2=key2),
                                      dest=tbl_dest+'[incoming_interface_list][(?P<iil>.*)][{key2}]'.format(key2=key2))

                elif key == 'outgoing_interface_list':
                    for key2, src_key in zip(['flags', 'uptime'], ['oil_flags', 'oil_uptime']):
                        self.add_leaf(cmd=cmd,
                                      src=tbl_src+'[outgoing_interface_list][(?P<oil>.*)][{src_key}]'.format(src_key=src_key),
                                      dest=tbl_dest+'[outgoing_interface_list][(?P<oil>.*)][{key2}]'.format(key2=key2))

                else:
                    self.add_leaf(cmd=cmd,
                                  src=tbl_src+'[{key}]'.format(key=key),
                                  dest=tbl_dest+'[{key}]'.format(key=key))

        # Make final Ops structure
        self.make(final_call=True)