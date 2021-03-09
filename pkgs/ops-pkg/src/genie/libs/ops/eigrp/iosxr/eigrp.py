# Genie
from genie.ops.base import Base

# iosxr show_eigrp
from genie.libs.parser.iosxr.show_eigrp import ShowEigrpIpv4NeighborsDetail,\
                                               ShowEigrpIpv6NeighborsDetail


class Eigrp(Base):
    '''
        Eigrp Ops object
    '''

    def learn(self):
        '''
            Learn Eigrp object
        '''
        # N/A -> Keys are not supported by this OS
        # eigrp_instance
        #   vrf
        #       address_family
        #           router_id                       N/A
        #           named_mode
        #           name
        #           eigrp_interface
        #               passive                     N/A
        #               hello_interval              N/A
        #               hold_timer                  N/A
        #               auth_val                    N/A
        #               eigrp_nbr
        #                   nbr_sw_ver
        #                       os_majorver
        #                       os_minorver
        #                       tlv_majorrev
        #                       tlv_minorrev
        #                   nbr_stubinfo            N/A
        #                   retransmit_count
        #                   retry_count
        #                   last_seq_number
        #                   srtt
        #                   rto
        #                   q_cnt
        #                   hold
        #                   uptime
        #                   peer_handle
        #                   prefixes
        #                   topology_ids_from_peer  N/A

        # eigrp_instance
        #   vrf
        #     address_family


        # ShowEigrpIpv4NeighborsDetail
        # ShowEigrpIpv6NeighborsDetail

        # Adding these keys
        # eigrp_instance
        #     vrf
        #         address_family
        #             name
        #             named_mode
        #             eigrp_interface
        #                 eigrp_nbr
        #                     retransmit_count
        #                     retry_count
        #                     last_seq_number
        #                     srtt
        #                     rto
        #                     q_cnt
        #                     peer_handle
        #                     nbr_sw_ver
        #                         os_majorver
        #                         os_minorver
        #                         tlv_majorrev
        #                         tlv_minorrev 
        #                     hold
        #                     uptime
        #                     prefixes  

        for cmd in [ShowEigrpIpv4NeighborsDetail, ShowEigrpIpv6NeighborsDetail]:

            for vrf in ['', 'all']:

                # address_family
                #   name
                #   named_mode
                #   eigrp_interface
                for key in ['name', 'named_mode']:
                    info_src = '[eigrp_instance][(?P<as_num>.*)][vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)]'
                    info_dest = 'info' + info_src

                    # address_family
                    #   name
                    self.add_leaf(cmd=cmd,
                                src=info_src+'[{key}]'.format(key=key),
                                dest=info_dest+'[{key}]'.format(key=key),
                                vrf=vrf
                                )

                info_src = '[eigrp_instance][(?P<as_num>.*)][vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)][eigrp_interface][(?P<eigrp_interface>.*)][eigrp_nbr][(?P<eigrp_nbr>.*)]'
                info_dest = 'info' + info_src

                # eigrp_interface
                #   eigrp_nbr
                #     retransmit_count
                #     retry_count
                #     last_seq_number
                #     srtt
                #     rto
                #     q_cnt
                #     peer_handle
                #     nbr_sw_ver
                #     hold
                #     uptime
                #     prefixes
                for key in ['retransmit_count', 'retry_count', 'last_seq_number',
                            'srtt', 'rto', 'q_cnt', 'peer_handle',
                            'nbr_sw_ver', 'hold', 'uptime', 'prefixes']:

                    self.add_leaf(cmd=cmd,
                                src=info_src+'[{key}]'.format(key=key),
                                dest=info_dest+'[{key}]'.format(key=key),
                                vrf=vrf
                                )

                # eigrp_interface
                #   eigrp_nbr
                #       nbr_sw_ver
                #           os_majorver
                #           os_minorver
                #           tlv_majorrev
                #           tlv_minorrev
                for key in ['os_majorver', 'os_minorver', 'tlv_majorrev',
                            'tlv_minorrev']:
                    self.add_leaf(cmd=cmd,
                                src=info_src+'[eigrp_interface][(?P<eigrp_interface>.*)][eigrp_nbr][(?P<eigrp_nbr>.*)][nbr_sw_ver][(?P<nbr_sw_ver>.*)][{key}]'.format(key=key),
                                dest=info_dest+'[eigrp_interface][(?P<eigrp_interface>.*)][eigrp_nbr][(?P<eigrp_nbr>.*)][nbr_sw_ver][(?P<nbr_sw_ver>.*)][{key}]'.format(key=key),
                                vrf=vrf
                                )

        self.make(final_call=True)
