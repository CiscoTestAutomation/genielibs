# super class
from genie.libs.ops.vxlan.vxlan import Vxlan as SuperVxlan

from genie.libs.parser.nxos.show_vxlan import ShowNvePeers,\
                                   ShowNveInterfaceDetail,\
                                   ShowNveEthernetSegment,\
                                   ShowNveVni,\
                                   ShowNveVniSummary,\
                                   ShowNveMultisiteDciLinks,\
                                   ShowNveMultisiteFabricLinks,\
                                   ShowL2routeEvpnEternetSegmentAll,\
                                   ShowL2routeTopologyDetail,\
                                   ShowL2routeMacAllDetail,\
                                   ShowL2routeMacIpAllDetail,\
                                   ShowL2routeSummary,\
                                   ShowL2routeFlAll,\
                                   ShowRunningConfigNvOverlay, \
                                   ShowFabricMulticastGlobals, \
                                   ShowFabricMulticastIpSaAdRoute, \
                                   ShowFabricMulticastIpL2Mroute,\
                                   ShowRunningConfigNvOverlay,\
                                   ShowNveVniIngressReplication

from genie.libs.parser.nxos.show_bgp import ShowBgpL2vpnEvpnSummary,\
                                   ShowBgpL2vpnEvpnRouteType,\
                                   ShowBgpL2vpnEvpnNeighbors,\
                                   ShowBgpIpMvpnRouteType, \
                                   ShowBgpIpMvpnSaadDetail

from genie.libs.parser.nxos.show_feature import ShowFeature
from genie.libs.parser.nxos.show_mcast import ShowForwardingDistributionMulticastRoute

class Vxlan(SuperVxlan):
    '''Vxlan Ops Object'''

    def set_enable(self, key):
        if 'enabled' in key:
            return True

    def set_nv_enabled(self, key):
        if key:
            return True
    
    def convert_intf_name(self, item):
        return item.capitalize()

    def learn(self):
        '''Learn vxlan object'''
        # Place holder to make it more readable

        #  nve_name
        #    vni
        #       nve_vni
        #           vni
        #           mcast
        #           vni_state
        #           mode
        #           type
        #           flags
        src_nve_vni = '[(?P<nve_name>^nve.*)][vni][(?P<nve_vni>.*)]'
        dest_nve_vni = 'nve' + src_nve_vni

        req_key = ['vni', 'mcast', 'vni_state', 'mode', 'type', 'flags']
        for key in req_key:
            self.add_leaf(cmd=ShowNveVni,
                          src=src_nve_vni + '[{}]'.format(key),
                          dest=dest_nve_vni + '[{}]'.format(key))

        req_key = ['associated_vrf','multisite_ingress_replication']
        for key in req_key:
            self.add_leaf(cmd=ShowRunningConfigNvOverlay,
                          src=src_nve_vni + '[{}]'.format(key),
                          dest=dest_nve_vni + '[{}]'.format(key))
        self.make()
        # nve_name
        #     nve_name
        #     if_state
        #     encap_type
        #     vpc_capability
        #     local_rmac
        #     host_reach_mode
        #     source_if
        #     primary_ip
        #     secondary_ip
        #     src_if_state
        #     ir_cap_mode
        #     adv_vmac
        #     nve_flags
        #     nve_if_handle
        #     src_if_holddown_tm
        #     src_if_holdup_tm
        #     src_if_holddown_left
        #     multisite_convergence_time
        #     multisite_convergence_time_left
        #     vip_rmac
        #     vip_rmac_ro
        #     sm_state
        #     peer_forwarding_mode
        #     dwn_strm_vni_cfg_mode
        #     src_intf_last_reinit_notify_type
        #     mcast_src_intf_last_reinit_notify_type
        #     multi_src_intf_last_reinit_notify_type
        #     multisite_bgw_if
        #     multisite_bgw_if_ip
        #     multisite_bgw_if_admin_state
        #     multisite_bgw_if_oper_state
        #     multisite_bgw_if_oper_state_down_reason
        try:
            nve_name_list = self.nve.keys()
        except:
            nve_name_list = []

        for nve_name in nve_name_list:
            if 'nve' in nve_name:
                src_nve = '[(?P<nve_name>.*)]'
                dest_nve = 'nve' + src_nve

                req_key =['nve_name','if_state','encap_type', 'vpc_capability', 'local_rmac',\
                          'host_reach_mode','primary_ip','secondary_ip','src_if_state',\
                          'ir_cap_mode', 'adv_vmac','nve_flags','nve_if_handle','src_if_holddown_tm',\
                          'src_if_holdup_tm','src_if_holddown_left','vip_rmac','vip_rmac_ro','multisite_convergence_time',\
                          'sm_state','peer_forwarding_mode', 'src_intf_last_reinit_notify_type','multisite_convergence_time_left',\
                          'mcast_src_intf_last_reinit_notify_type','multi_src_intf_last_reinit_notify_type',\
                          'multisite_bgw_if_ip','multisite_bgw_if_admin_state',\
                          'multisite_bgw_if_oper_state','multisite_bgw_if_oper_state_down_reason']
                for key in req_key:
                    self.add_leaf(cmd=ShowNveInterfaceDetail,
                                  src=src_nve + '[{}]'.format(key),
                                  dest=dest_nve + '[{}]'.format(key),
                                  interface=nve_name)

                self.add_leaf(cmd=ShowNveInterfaceDetail,
                              src=src_nve + '[source_if][(?P<source_if>.*)]',
                              dest=dest_nve + '[source_if][(?P<source_if>.*)]',
                              interface=nve_name,
                              action=self.convert_intf_name)
                self.add_leaf(cmd=ShowNveInterfaceDetail,
                              src=src_nve + '[multisite_bgw_if][(?P<multisite_bgw_if>.*)]',
                              dest=dest_nve + '[multisite_bgw_if][(?P<multisite_bgw_if>.*)]',
                              interface=nve_name,
                              action=self.convert_intf_name)
        # nve - enabled
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][nve][instance][(?P<instance>.*)][state]',
                      dest='nve[enabled_nv_overlay]',
                      action=self.set_enable)

        # vnseg_vlan - enabled
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][vnseg_vlan][instance][(?P<instance>.*)][state]',
                      dest='nve[enabled_vn_segment_vlan_based]',
                      action=self.set_enable)

        # nv overlay evpn - enbaled
        self.add_leaf(cmd=ShowBgpL2vpnEvpnSummary,
                      src='[instance][(?P<instance>.*)]',
                      dest='nve[enabled_nv_overlay_evpn]',
                      action=self.set_nv_enabled)

        # evpn multisite border-gateway
        self.add_leaf(cmd=ShowRunningConfigNvOverlay,
                      src='[evpn_multisite_border_gateway]',
                      dest='nve[evpn_multisite_border_gateway]')

        # ngmvpn - enbaled
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][ngmvpn][instance][(?P<instance>.*)][state]',
                      dest='nve[enabled_ngmvpn]',
                      action=self.set_enable)

        # vni
        #   summary
        #      cp_vni_count
        #      cp_vni_up
        #      cp_vni_down
        #      dp_vni_count
        #      dp_vni_up
        #      dp_vni_down

        src_nve = '[vni][summary]'
        dest_nve = 'nve' + src_nve

        req_key = ['cp_vni_count', 'cp_vni_up', 'cp_vni_down', 'dp_vni_count', 'dp_vni_up', 'dp_vni_down']
        for key in req_key:
            self.add_leaf(cmd=ShowNveVniSummary,
                          src=src_nve + '[{}]'.format(key),
                          dest=dest_nve + '[{}]'.format(key))

        #  nve_name
        #    vni
        #       nve_vni
        #           repl_ip
        #               repl_ip
        #               source
        #               up_time
        src_nve_vni_ingress = '[(?P<nve_name>^nve.*)][vni][(?P<nve_vni>.*)][repl_ip][(?P<repl_ip>.*)]'
        dest_nve_vni_ingress = 'nve' + src_nve_vni_ingress

        req_key = ['source', 'up_time', 'repl_ip']
        for key in req_key:
            self.add_leaf(cmd=ShowNveVniIngressReplication,
                          src=src_nve_vni_ingress + '[{}]'.format(key),
                          dest=dest_nve_vni_ingress + '[{}]'.format(key))


        # multisite_convergence_time in nv overlay
        self.add_leaf(cmd=ShowRunningConfigNvOverlay,
                      src='[multisite_convergence_time]',
                      dest='nve[multisite_convergence_time]')

        # peer_ip
        #    peer_ip
        #        peer_state
        #        learn_type
        #        uptime
        #        router_mac
        src_nve = '[(?P<nve_name>.*)]'
        src_nve_peer = src_nve + '[peer_ip][(?P<peer_ip>.*)]'
        dest_nve_peer = 'nve' + src_nve_peer

        req_key = ['peer_state', 'learn_type', 'uptime', 'router_mac']
        for key in req_key:
            self.add_leaf(cmd=ShowNvePeers,
                          src=src_nve_peer + '[{}]'.format(key),
                          dest=dest_nve_peer + '[{}]'.format(key))

        # ethernet_segment
        #     esi
        #         esi
        #             esi
        #             if_name
        #             es_state
        #             po_state
        #             nve_if_name
        #             nve_state
        #             host_reach_mode
        #             active_vlans
        #             df_vlans
        #             active_vnis
        #             cc_failed_vlans
        #             cc_timer_left
        #             num_es_mem
        #             local_ordinal
        #             df_timer_st
        #             config_status
        #             df_list
        #             es_rt_added
        #             ead_rt_added
        #             ead_evi_rt_timer_age
        src_nve_seg = '[nve]' + src_nve + '[ethernet_segment][esi][(?P<esi>.*)]'
        dest_nve_seg = 'nve' + src_nve + '[ethernet_segment][esi][(?P<esi>.*)]'

        req_key =['esi', 'if_name', 'es_state', 'po_state','nve_if_name','nve_state','host_reach_mode',\
                   'active_vlans','cc_failed_vlans','df_vlans','active_vnis','cc_failed_vlans','cc_timer_left','num_es_mem',\
                   'local_ordinal','df_timer_st','config_status','df_list','es_rt_added','ead_rt_added','ead_evi_rt_timer_age']
        for key in req_key:
            self.add_leaf(cmd=ShowNveEthernetSegment,
                          src=src_nve_seg + '[{}]'.format(key),
                          dest=dest_nve_seg + '[{}]'.format(key))

        # multisite
        #    dci_links
        #         if_name
        #             if_name
        #             if_state
        src_nve_dci = '[multisite][dci_links][(?P<if_name>.*)]'
        dest_nve_dci = 'nve' + src_nve_dci

        req_key = ['if_name', 'if_state']
        for key in req_key:
            self.add_leaf(cmd=ShowNveMultisiteDciLinks,
                          src=src_nve_dci + '[{}]'.format(key),
                           dest=dest_nve_dci + '[{}]'.format(key))

        # multisite
        #    fabric_links
        #         if_name
        #             if_name
        #             if_state
        src_nve_fabric = '[multisite][fabric_links][(?P<if_name>.*)]'
        dest_nve_fabric = 'nve' + src_nve_fabric

        req_key = ['if_name', 'if_state']
        for key in req_key:
            self.add_leaf(cmd=ShowNveMultisiteFabricLinks,
                          src=src_nve_fabric + '[{}]'.format(key),
                          dest=dest_nve_fabric + '[{}]'.format(key))
        self.make()
        ##############################################################################
        #                       l2route
        #############################################################################
        #  evpn
        #     ethernet_segment
        #         index
        #             ethernet_segment
        #             originating_rtr
        #             prod_name
        #             int_ifhdl
        #             client_nfn
        src_evpn = '[evpn][ethernet_segment][(?P<index>.*)]'
        dest_evpn = 'l2route' + src_evpn

        req_key = ['ethernet_segment', 'originating_rtr','prod_name','int_ifhdl','client_nfn']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeEvpnEternetSegmentAll,
                          src=src_evpn + '[{}]'.format(key),
                          dest=dest_evpn + '[{}]'.format(key))

        #   topology
        #      topo_id
        #          num_of_peer_id
        #          peer_id
        #              peer_id
        #                   topo_id
        #                   peer_id
        #                   flood_list
        #                   is_service_node
        self.add_leaf(cmd=ShowL2routeFlAll,
                      src='[topology][topo_id][(?P<topo_id>.*)][num_of_peer_id]',
                      dest='l2route[topology][topo_id][(?P<topo_id>.*)][num_of_peer_id]')

        src_topology_fl = '[topology][topo_id][(?P<topo_id>.*)][peer_id][(?P<peer_id>.*)]'
        dest_topology_fl = 'l2route' + src_topology_fl

        req_key = ['topo_id', 'peer_id', 'flood_list', 'is_service_node']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeFlAll,
                          src=src_topology_fl + '[{}]'.format(key),
                          dest=dest_topology_fl + '[{}]'.format(key))

        # topology
        #    topo_id
        #       topo_id
        #          topo_name
        #            topo_name
        #                 topo_name
        #                 topo_type
        #                 vni
        #                 encap_type
        #                 iod
        #                 if_hdl
        #                 vtep_ip
        #                 emulated_ip
        #                 emulated_ro_ip
        #                 tx_id
        #                 rcvd_flag
        #                 rmac
        #                 vrf_id
        #                 vmac
        #                 flags
        #                 sub_flags
        #                 prev_flags
        src_topology = '[topology][topo_id][(?P<topo_id>.*)][topo_name][(?P<topo_name>.*)]'
        dest_topology = 'l2route' + src_topology

        req_key = ['topo_name', 'topo_type', 'vni', 'encap_type', 'iod','if_hdl','vtep_ip','emulated_ip',\
                   'emulated_ro_ip','tx_id','rcvd_flag','rmac','vrf_id','vmac','flags','sub_flags','prev_flags']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeTopologyDetail,
                          src=src_topology + '[{}]'.format(key),
                          dest=dest_topology + '[{}]'.format(key))

        # topology
        #   topo_id
        #     topo_id
        #        mac
        #          mac_addr
        #             mac_addr
        #             prod_type
        #             flags
        #             seq_num
        #             next_hop1
        #             rte_res
        #             fwd_state
        #             peer_id
        #             sent_to
        #             soo

        src_mac = '[topology][topo_id][(?P<topo_id>.*)][mac][(?P<mac_addr>.*)]'
        dest_mac = 'l2route' + src_mac

        req_key = ['mac_addr', 'prod_type', 'flags', 'seq_num', 'next_hop1', 'rte_res', 'fwd_state', 'peer_id', 'sent_to',\
                   'soo']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeMacAllDetail,
                          src=src_mac + '[{}]'.format(key),
                          dest=dest_mac + '[{}]'.format(key))

        # topology
        #   topo_id
        #     topo_id
        #        mac_ip
        #           mac_addr
        #                 mac_addr
        #                 mac_ip_prod_type
        #                 mac_ip_flags
        #                 seq_num
        #                 next_hop1
        #                 host_ip
        #                 sent_to
        #                 soo
        #                 l3_info
        src_mac_all = '[topology][topo_id][(?P<topo_id>.*)][mac_ip][(?P<mac_addr>.*)]'
        dest_mac_all = 'l2route' + src_mac_all

        req_key = ['mac_addr', 'mac_ip_prod_type', 'mac_ip_flags', 'seq_num', 'next_hop1', 'host_ip',\
                   'sent_to', 'soo','l3_info']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeMacIpAllDetail,
                          src=src_mac_all + '[{}]'.format(key),
                          dest=dest_mac_all + '[{}]'.format(key))

        # summary
        #   total_memory
        #   numof_converged_tables
        #   table_name
        #        table_name
        #           producer_name
        #               producer_name
        #                  producer_name
        #                  id
        #                  objects
        #                  memory
        #               total_obj
        #               total_mem

        src_summary = '[summary]'
        dest_summary = 'l2route' + src_summary

        req_key = ['total_memory', 'numof_converged_tables']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeSummary,
                          src=src_summary + '[{}]'.format(key),
                          dest=dest_summary + '[{}]'.format(key))

        src_table_name = src_summary + '[table_name][(?P<table_name>.*)][producer_name][(?P<producer_name>.*)]'
        dest_table_name = 'l2route' + src_table_name

        req_key = ['producer_name', 'id', 'objects', 'memory']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeSummary,
                          src=src_table_name + '[{}]'.format(key),
                          dest=dest_table_name + '[{}]'.format(key))

        src_total = src_summary + '[table_name][(?P<table_name>.*)][producer_name]'
        dest_total = 'l2route' + src_total

        req_key = ['total_obj', 'total_mem']
        for key in req_key:
            self.add_leaf(cmd=ShowL2routeSummary,
                          src=src_total + '[{}]'.format(key),
                          dest=dest_total + '[{}]'.format(key))

        ##############################################################################
        #                       bgp_l2vpn_evpn
        #############################################################################
        # instance
        #     instance_name
        #         vrf
        #             vrf_name_out
        #                 vrf_name_out
        #                 vrf_router_id
        #                 vrf_local_as
        #                 address_family
        #                     af_name
        #                         tableversion
        #                         configuredpeers
        #                         capablepeers
        #                         totalnetworks
        #                         totalpaths
        #                         memoryused
        #                         numberattrs
        #                         bytesattrs
        #                         numberpaths
        #                         bytespaths
        #                         numbercommunities
        #                         bytescommunities
        #                         numberclusterlist
        #                         bytesclusterlist
        #                         dampening
        #                         neighbor
        #                             neighbor
        #                                 neighbor
        #                                 version
        #                                 msgrecvd
        #                                 msgsent
        #                                 neighbortableversion
        #                                 inq
        #                                 outq
        #                                 remoteas
        #                                 state
        #                                 prefixreceived
        #
        src_instance ='[instance][(?P<instance>.*)][vrf][(?P<vrf_name_out>.*)]'
        dest_instance = 'bgp_l2vpn_evpn' + src_instance

        req_key = ['vrf_name_out', 'vrf_router_id', 'vrf_local_as']
        for key in req_key:
            self.add_leaf(cmd=ShowBgpL2vpnEvpnSummary,
                          src=src_instance + '[{}]'.format(key),
                          dest=dest_instance + '[{}]'.format(key))

        src_af = src_instance + '[address_family][(?P<af_name>.*)]'
        dest_af = 'bgp_l2vpn_evpn' + src_af

        req_key = ['tableversion', 'configuredpeers', 'capablepeers','totalnetworks','totalpaths','memoryused',\
                   'numberattrs', 'bytesattrs','numberpaths','numberpaths','bytespaths',\
                   'numbercommunities','bytescommunities',\
                   'numberclusterlist','bytesclusterlist','dampening']
        for key in req_key:
            self.add_leaf(cmd=ShowBgpL2vpnEvpnSummary,
                          src=src_af + '[{}]'.format(key),
                          dest=dest_af + '[{}]'.format(key))

        src_neighbor = src_af + '[neighbor][(?P<neighbor>.*)]'
        dest_neighbor = 'bgp_l2vpn_evpn' + src_neighbor

        req_key = ['neighbor', 'version', 'msgrecvd', 'msgsent', 'neighbortableversion', 'inq', 'outq',
                   'remoteas', 'state', 'prefixreceived']
        for key in req_key:
            self.add_leaf(cmd=ShowBgpL2vpnEvpnSummary,
                          src=src_neighbor + '[{}]'.format(key),
                          dest=dest_neighbor + '[{}]'.format(key))
        # instance
        #     instance_name
        #         vrf
        #             vrf_name_out
        #                 address_family
        #                     af_name
        #                         neighbor
        #                             neighbor
        #                                  elapsedtime
        #                                  state
        #                                  localas
        #                                  link
        #                                  index
        #                                  version
        #                                  remote_id  
        #                                  up                             
        #                                  connectedif
        #                                  bfd
        #                                  ttlsecurity
        #                                  password
        #                                  passiveonly
        #                                  localas_inactive
        #                                  remote_privateas
        #                                  lastread
        #                                  holdtime
        #                                  keepalivetime
        #                                  lastwrite
        #                                  keepalive
        #                                  notificationsrcvd
        #                                  recvbufbytes
        #                                  notificationssent
        #                                  sentbytesoutstanding
        #                                  totalbytessent
        #                                  connsestablished
        #                                  connsdropped
        #                                  resettime
        #                                  resetreason
        #                                  peerresettime
        #                                  peerresetreason
        #                                  capsnegotiated
        #                                  capmpadvertised
        #                                  caprefreshadvertised
        #                                  capgrdynamicadvertised
        #                                  capmprecvd
        #                                  caprefreshrecvd
        #                                  capgrdynamicrecvd
        #                                  capolddynamicadvertised
        #                                  capolddynamicrecvd    
        #                                  caprradvertised    
        #                                  caprrrecvd    
        #                                  capoldrradvertised    
        #                                  capoldrrrecvd    
        #                                  capas4advertised    
        #                                  capas4recvd
        #                                  capgradvertised    
        #                                  capgrrecvd
        #                                  grrestarttime
        #                                  grstaletiem
        #                                  grrecvdrestarttime
        #                                  capextendednhadvertised    
        #                                  capextendednhrecvd    
        #                                  epe
        #                                  firstkeepalive
        #                                  openssent
        #                                  opensrecvd
        #                                  updatessent
        #                                  updatesrecvd
        #                                  keepalivesent29
        #                                  keepaliverecvd34
        #                                  rtrefreshsent
        #                                  rtrefreshrecvd
        #                                  capabilitiessent
        #                                  capabilitiesrecvd
        #                                  bytessent0398
        #                                  bytesrecvd614
        #                                  localaddr
        #                                  localport
        #                                  remoteaddr
        #                                  remoteport
        #                                  fd

        src_neighbor = src_af + '[neighbor][(?P<neighbor>.*)]'
        dest_neighbor = 'bgp_l2vpn_evpn' + src_af +'[neighbor][(?P<neighbor>.*)]'

        req_key = ['elapsedtime','localas', 'link', 'index', 'remote_id', 'up', 'connectedif','bfd',\
                   'ttlsecurity', 'password', 'passiveonly', 'localas_inactive','remote_privateas',\
                   'lastread','holdtime','keepalivetime','lastwrite','keepalive','notificationsrcvd',\
                   'recvbufbytes','notificationssent','sentbytesoutstanding',\
                   'connsestablished','connsdropped','resettime','resetreason','peerresettime','peerresetreason',\
                   'capsnegotiated','capmpadvertised','caprefreshadvertised','capgrdynamicadvertised','capmprecvd',\
                   'caprefreshrecvd','capgrdynamicrecvd','capolddynamicadvertised','capolddynamicrecvd',\
                   'caprradvertised','caprrrecvd','capoldrradvertised','capoldrrrecvd','capas4advertised','capas4recvd',\
                   'capgradvertised','capgrrecvd','grrestarttime','grstaletiem','grrecvdrestarttime',\
                   'capextendednhadvertised','capextendednhrecvd','epe','firstkeepalive','openssent',\
                   'opensrecvd','updatessent','updatesrecvd','keepalivesent','keepaliverecvd','rtrefreshsent',\
                   'rtrefreshrecvd','capabilitiessent','capabilitiesrecvd','bytessent','bytesrecvd','localaddr',\
                   'localport','remoteaddr','remoteport','fd']
        for key in req_key:
            self.add_leaf(cmd=ShowBgpL2vpnEvpnNeighbors,
                          src=src_neighbor + '[{}]'.format(key),
                          dest=dest_neighbor + '[{}]'.format(key))

        #  af
        #     af_name
        #          af_advertised
        #          af_recvd
        #          af_name
        src_neighbor_af = src_neighbor +'[af][(?P<af_name>.*)]'
        dest_neighbor_af = 'bgp_l2vpn_evpn' + src_neighbor_af

        req_key = ['af_advertised', 'af_recvd', 'af_name']
        for key in req_key:
            self.add_leaf(cmd=ShowBgpL2vpnEvpnNeighbors,
                          src=src_neighbor_af + '[{}]'.format(key),
                          dest=dest_neighbor_af + '[{}]'.format(key))

        #   graf
        #     graf_af_name
        #          gr_af_name
        #          gr_adv
        #          gr_recv
        #          gr_fwd
        src_neighbor_graf = src_neighbor + '[graf][(?P<graf_af_name>.*)]'
        dest_neighbor_graf = 'bgp_l2vpn_evpn' + src_neighbor_graf

        req_key = ['gr_af_name', 'gr_adv', 'gr_recv', 'gr_fwd']
        for key in req_key:
            self.add_leaf(cmd=ShowBgpL2vpnEvpnNeighbors,
                          src=src_neighbor_graf + '[{}]'.format(key),
                          dest=dest_neighbor_graf + '[{}]'.format(key))

        #   capextendednhaf
        #      capextendednhaf
        #            capextendednh_af_name
        src_neighbor_cap = src_neighbor + '[capextendednhaf][(?P<capextendednhaf>.*)]'
        dest_neighbor_cap = 'bgp_l2vpn_evpn' + src_neighbor_cap

        self.add_leaf(cmd=ShowBgpL2vpnEvpnNeighbors,
                      src=src_neighbor_cap + '[capextendednh_af_name]',
                      dest=dest_neighbor_cap + '[capextendednh_af_name]')
        #   peraf
        #       peraf
        #           per_af_name
        #           tableversion
        #           neighbortableversion
        #           pfxrecvd
        #           pfxbytes
        #           insoftreconfigallowed
        #           sendcommunity
        #           sendextcommunity
        #           asoverride
        #           peerascheckdisabled
        #           rrconfigured
        #           pfxbytes
        src_neighbor_peraf = src_neighbor + '[peraf][(?P<peraf>.*)]'
        dest_neighbor_peraf = 'bgp_l2vpn_evpn' + src_neighbor_peraf

        req_key = ['per_af_name', 'tableversion', 'neighbortableversion', 'pfxrecvd', 'pfxbytes',\
                   'insoftreconfigallowed','sendcommunity','sendextcommunity','asoverride',\
                   'peerascheckdisabled','rrconfigured']
        for key in req_key:
            self.add_leaf(cmd=ShowBgpL2vpnEvpnNeighbors,
                          src=src_neighbor_peraf + '[{}]'.format(key),
                          dest=dest_neighbor_peraf + '[{}]'.format(key))
        
        # rd
        #   rd
        #     rd
        #     rd_vrf
        #     rd_vniid
        #     prefix
        #         prefix
        #             nonipprefix'
        #             prefixversion'
        #             totalpaths
        #             bestpathnr'
        #             mpath
        #             on_newlist
        #             on_xmitlist
        #             suppressed
        #             needsresync
        #             locked
        #             path
        #                 path
        #                     pathnr
        #                     policyincomplete
        #                     pathvalid
        #                     pathbest
        #                     pathdeleted
        #                     pathstaled
        #                     pathhistory
        #                     pathovermaxaslimit
        #                     pathmultipath
        #                     pathnolabeledrnh
        #                     ipnexthop
        #                     nexthopmetric
        #                     neighbor
        #                     neighborid
        #                     origin
        #                     localpref
        #                     weight
        #                     inlabel
        #                     extcommunity
        #                     advertisedto
        #                     originatorid
        #                     clusterlist
        #
        # route_type
        route_types= ["1", "2", "3", "4"]
        for rt in route_types:

            src_rd = src_af + '[rd][(?P<rd>.*)]'
            dest_rd = 'bgp_l2vpn_evpn' + src_rd

            req_key = ['rd', 'rd_vrf', 'rd_vniid']
            for key in req_key:
                self.add_leaf(cmd=ShowBgpL2vpnEvpnRouteType,
                              src=src_rd + '[{}]'.format(key),
                              dest=dest_rd + '[{}]'.format(key),
                              route_type=rt)

                src_prefix = src_rd + '[prefix][(?P<prefix>.*)]'
                dest_prefix = 'bgp_l2vpn_evpn' + src_prefix

                req_key = ['nonipprefix', 'prefixversion', 'totalpaths','bestpathnr','on_newlist',\
                           'on_xmitlist','suppressed','needsresync','locked','mpath']
                for key in req_key:
                    self.add_leaf(cmd=ShowBgpL2vpnEvpnRouteType,
                                  src=src_prefix + '[{}]'.format(key),
                                  dest=dest_prefix + '[{}]'.format(key),
                                  route_type=rt)

                src_path = src_prefix + '[path][(?P<index>.*)]'
                dest_path = 'bgp_l2vpn_evpn' + src_path

                req_key = ['pathnr', 'policyincomplete', 'pathvalid', 'pathbest', 'pathdeleted', \
                           'pathstaled', 'pathhistory', 'pathovermaxaslimit', 'pathmultipath', 'pathnolabeledrnh',\
                           'importdestcount','ipnexthop','nexthopmetric','neighbor','neighborid',\
                           'origin','localpref','weight','inlabel', 'extcommunity', 'advertisedto',\
                           'originatorid', 'clusterlist']
                for key in req_key:
                    self.add_leaf(cmd=ShowBgpL2vpnEvpnRouteType,
                                  src=src_path + '[{}]'.format(key),
                                  dest=dest_path + '[{}]'.format(key),
                                  route_type=rt)

                #          pmsi_tunnel_attribute
                #              label
                #              flags
                #              tunnel_id
                #              tunnel_type
                src_tunnel = src_path + '[pmsi_tunnel_attribute]'
                dest_tunnel = 'bgp_l2vpn_evpn' + src_tunnel

                req_key = ['label', 'flags', 'tunnel_id', 'tunnel_type']
                for key in req_key:
                    self.add_leaf(cmd=ShowBgpL2vpnEvpnRouteType,
                                  src=src_tunnel + '[{}]'.format(key),
                                  dest=dest_tunnel + '[{}]'.format(key),
                                  route_type=rt)

        self.make()
        ###############################################################
        #                   TRM - Fabric                              #
        ###############################################################
        # multicast
        #   globals
        #       pruning
        #       switch_role
        #       fabric_control_seg
        #       peer_fabric_ctrl_addr
        #       advertise_vpc_rpf_routes
        #       created_vni_list
        #       fwd_encap
        #       overlay_distributed_dr
        #       overlay_spt_only

        src_fabric_multicast = '[multicast][globals]'
        dest_fabric_multicast= 'fabric' + src_fabric_multicast

        req_key = ['pruning', 'switch_role', 'fabric_control_seg','peer_fabric_ctrl_addr',
                   'advertise_vpc_rpf_routes', 'created_vni_list', 'fwd_encap',
                   'overlay_distributed_dr','overlay_spt_only']
        for key in req_key:
            self.add_leaf(cmd=ShowFabricMulticastGlobals,
                          src=src_fabric_multicast + '[{}]'.format(key),
                          dest=dest_fabric_multicast + '[{}]'.format(key))

        # multicast
        #   vrf
        #     <vrf>
        #        vnid
        #        address_family
        #           <af_name>
        #             sa_ad_routes
        #               gaddr
        #                 <gaddr>
        #                   grp_len
        #                     saddr
        #                       <saddr>
        #                         src_len
        #                         uptime
        #                         interested_fabric_nodes
        #                             <interested_fabric_nodes>
        #                                 uptime

        src_fabric_vrf = '[multicast][vrf][(?P<vrf_name>.*)]'
        dest_fabric_vrf = 'fabric' + src_fabric_vrf

        self.add_leaf(cmd=ShowFabricMulticastIpSaAdRoute,
                      src=src_fabric_vrf + '[vnid]',
                      dest=dest_fabric_vrf + '[vnid]',
                      vrf='all')

        src_fabric_vrf_gaddr = src_fabric_vrf + '[address_family][(?P<af>.*)][sa_ad_routes][gaddr][(?P<gaddr>.*)]'
        dest_fabric_vrf_gaddr = 'fabric' + src_fabric_vrf_gaddr

        self.add_leaf(cmd=ShowFabricMulticastIpSaAdRoute,
                      src=src_fabric_vrf_gaddr + '[grp_len]',
                      dest=dest_fabric_vrf_gaddr + '[grp_len]',
                      vrf='all')

        src_fabric_vrf_saddr = src_fabric_vrf_gaddr + '[saddr][(?P<saddr>.*)]'
        dest_fabric_vrf_saddr = 'fabric' + src_fabric_vrf_saddr

        req_key = ['src_len', 'uptime']
        for key in req_key:
            self.add_leaf(cmd=ShowFabricMulticastIpSaAdRoute,
                          src=src_fabric_vrf_saddr + '[{}]'.format(key),
                          dest=dest_fabric_vrf_saddr + '[{}]'.format(key),
                          vrf='all')

        src_fabric_vrf_intersted = src_fabric_vrf_saddr + '[interested_fabric_nodes][(?P<interested_fabric_nodes>.*)]'
        dest_fabric_vrf_intersted = 'fabric' + src_fabric_vrf_intersted

        self.add_leaf(cmd=ShowFabricMulticastIpSaAdRoute,
                      src=src_fabric_vrf_intersted + '[uptime]',
                      dest=dest_fabric_vrf_intersted + '[uptime]',
                      vrf='all')

        #  l2_mroute
        #       vni
        #         <vnid>
        #           vnid
        #           fabric_l2_mroutes
        #             gaddr
        #               <gaddr>
        #                 saddr
        #                   <saddr>
        #                     interested_fabric_nodes
        #                         <node>
        #                             node
        src_fabric_l2route = '[multicast][l2_mroute][vni][(?P<vni>.*)]'
        dest_fabric_l2route = 'fabric' + src_fabric_l2route

        self.add_leaf(cmd=ShowFabricMulticastIpL2Mroute,
                      src=src_fabric_l2route + '[vnid]',
                      dest=dest_fabric_l2route + '[vnid]',
                      vni='all')

        src_fabric_l2route_saddr = src_fabric_l2route + '[fabric_l2_mroutes][gaddr][(?P<gaddr>.*)]' \
                                                        '[saddr][(?P<saddr>.*)][interested_fabric_nodes]' \
                                                        '[(?P<interested_fabric_nodes>.*)]'
        dest_fabric_l2route_saddr = 'fabric' + src_fabric_l2route_saddr

        self.add_leaf(cmd=ShowFabricMulticastIpL2Mroute,
                      src=src_fabric_l2route_saddr + '[node]',
                      dest=dest_fabric_l2route_saddr + '[node]',
                      vni='all')

        ######################################################################
        #           TRM - Forwarding                                         #
        ######################################################################

        # distribution
        #     multicast
        #        route
        #           vrf
        #              <vrf>
        #                  address_family
        #                     <af>
        #                         num_groups
        #                         gaddr
        #                             <gaddr>
        #                                 grp_len
        #                                 saddr
        #                                    <saddr>
        #                                         rpf_ifname
        #                                         src_len
        #                                         flags
        #                                         rcv_packets
        #                                         rcv_bytes
        #                                         num_of_oifs
        #                                         oifs
        #                                            oif_index
        #                                            <oif>
        #                                               oif
        #                                               encap
        #                                               mem_l2_ports
        #                                               l2_oiflist_index
        src_forwarding_af = '[distribution][multicast][route][vrf][(?P<vrf_name>.*)][address_family][(?P<af>.*)]'
        dest_forwarding_af = 'forwarding' + src_forwarding_af

        self.add_leaf(cmd=ShowForwardingDistributionMulticastRoute,
                      src=src_forwarding_af + '[num_groups]',
                      dest=dest_forwarding_af+ '[num_groups]',
                      vrf='all')

        src_forwarding_gaddr = src_forwarding_af + '[gaddr][(?P<gaddr>.*)]'
        dest_forwarding_gaddr = 'forwarding' + src_forwarding_gaddr

        self.add_leaf(cmd=ShowForwardingDistributionMulticastRoute,
                      src=src_forwarding_gaddr + '[grp_len]',
                      dest=dest_forwarding_gaddr + '[grp_len]',
                      vrf='all')

        src_forwarding_saddr = src_forwarding_gaddr + '[saddr][(?P<saddr>.*)]'
        dest_forwarding_saddr = 'forwarding' + src_forwarding_saddr

        req_key = ['rpf_ifname', 'src_len', 'flags', 'rcv_packets', 'rcv_bytes', 'num_of_oifs']
        for key in req_key:
            self.add_leaf(cmd=ShowForwardingDistributionMulticastRoute,
                        src=src_forwarding_saddr + '[{}]'.format(key),
                        dest=dest_forwarding_saddr + '[{}]'.format(key),
                        vrf='all')

        src_forwarding_oifs = src_forwarding_saddr + '[oifs]'
        dest_forwarding_oifs = 'forwarding' + src_forwarding_oifs

        self.add_leaf(cmd=ShowForwardingDistributionMulticastRoute,
                      src=src_forwarding_oifs+ '[oif_index]',
                      dest=dest_forwarding_oifs + '[oif_index]',
                      vrf='all')

        src_forwarding_oif = src_forwarding_oifs + '[(?P<oif>.*)]'
        dest_forwarding_oif = 'forwarding' + src_forwarding_oif

        req_key = ['oif', 'encap', 'mem_l2_ports', 'l2_oiflist_index']
        for key in req_key:
            self.add_leaf(cmd=ShowForwardingDistributionMulticastRoute,
                        src=src_forwarding_oif + '[{}]'.format(key),
                        dest=dest_forwarding_oif + '[{}]'.format(key),
                        vrf='all')

        #######################################################################
        #               TRM - bgp_mvpn                                        #
        #######################################################################
        # instance
        #     <instance>
        #         vrf
        #            <vrf_name_out>
        #                 vrf_name_out
        #                 address_family
        #                     <af_name>
        #                         af_name
        #                         table_version
        #                         router_id
        #                         rd
        #                            <rd_val>
        #                                 rd_val
        #                                 rd_vrf
        #                                 prefix
        #                                     <nonipprefix>
        #                                         nonipprefix
        #                                         path
        #                                             <index>
        #                                                 pathnr
        #                                                 policyincomplete        N/A
        #                                                 pathdeleted             N/A
        #                                                 pathstaled              N/A
        #                                                 pathhistory             N/A
        #                                                 pathovermaxaslimit      N/A
        #                                                 pathmultipath           N/A
        #                                                 statuscode
        #                                                 bestcode
        #                                                 typecode
        #                                                 ipnexthop
        #                                                 weight
        #                                                 origin
        #                                                 localpref
        #                                                 pathvalid
        #                                                 pathbest
        #                                                 pathnolabeledrnh
        #                                                 status
        #                                                 best
        #                                                 type
        #                                                 nexthopmetric
        #                                                 neighbor
        #                                                 neighborid
        #                                                 extcommunity
        #                                                 advertisedto

        route_types = ["1", "2", "3", "4", "5", "6", "7"]
        for rt in route_types:
            src_bgp_mvpn_vrf = '[instance][(?P<instance>.*)][vrf][(?P<vrf_name>.*)]'
            dest_bgp_mvpn_vrf = 'bgp_mvpn' + src_bgp_mvpn_vrf

            self.add_leaf(cmd=ShowBgpIpMvpnRouteType,
                          src=src_bgp_mvpn_vrf + '[vrf_name_out]',
                          dest=dest_bgp_mvpn_vrf + '[vrf_name_out]',
                          route_type=rt,
                          vrf='all')

            src_bgp_mvpn_af = src_bgp_mvpn_vrf+ '[address_family][(?P<af>.*)]'
            dest_bgp_mvpn_af = 'bgp_mvpn' + src_bgp_mvpn_af

            req_key = ['af_name', 'table_version', 'router_id']
            for key in req_key:
                self.add_leaf(cmd=ShowBgpIpMvpnRouteType,
                              src=src_bgp_mvpn_af + '[{}]'.format(key),
                              dest=dest_bgp_mvpn_af + '[{}]'.format(key),
                              route_type=rt,
                              vrf='all')


            src_bgp_mvpn_rd = src_bgp_mvpn_af + '[rd][(?P<rd_val>.*)]'
            dest_bgp_mvpn_rd = 'bgp_mvpn' + src_bgp_mvpn_rd

            req_key = ['rd_val', 'rd_vrf']
            for key in req_key:
                self.add_leaf(cmd=ShowBgpIpMvpnRouteType,
                              src=src_bgp_mvpn_rd + '[{}]'.format(key),
                              dest=dest_bgp_mvpn_rd + '[{}]'.format(key),
                              route_type=rt,
                              vrf='all')

            #                                 prefix
            #                                     <nonipprefix>
            #                                         nonipprefix
            #                                         prefixversion
            #                                         totalpaths
            #                                         bestpathnr
            #                                         on_newlist          N/A
            #                                         on_xmitlist
            #                                         suppressed          N/A
            #                                         needsresync         N/A
            #                                         locked              N/A

            src_bgp_mvpn_prefix = src_bgp_mvpn_rd + '[prefix][(?P<nonipprefix>.*)]'
            dest_bgp_mvpn_prefix = 'bgp_mvpn' + src_bgp_mvpn_prefix

            req_key = ['nonipprefix','prefixversion', 'totalpaths', 'bestpathnr', 'on_xmitlist']
            for key in req_key:
                self.add_leaf(cmd=ShowBgpIpMvpnSaadDetail,
                              src=src_bgp_mvpn_prefix + '[{}]'.format(key),
                              dest=dest_bgp_mvpn_prefix + '[{}]'.format(key),
                              vrf='all')

            src_bgp_mvpn_path = src_bgp_mvpn_prefix + '[path][(?P<index>.*)]'
            dest_bgp_mvpn_path = 'bgp_mvpn' + src_bgp_mvpn_path

            req_key = ['pathnr', 'statuscode','bestcode','typecode','ipnexthop',
                       'weight','origin','localpref']
            for key in req_key:
                self.add_leaf(cmd=ShowBgpIpMvpnRouteType,
                              src=src_bgp_mvpn_path + '[{}]'.format(key),
                              dest=dest_bgp_mvpn_path + '[{}]'.format(key),
                              route_type=rt,
                              vrf='all')

            req_key = ['pathtype', 'pathvalid', 'pathbest', 'pathnolabeledrnh', 'nexthopmetric',
                       'neighbor', 'neighborid', 'extcommunity', 'advertisedto']
            for key in req_key:
                self.add_leaf(cmd=ShowBgpIpMvpnSaadDetail,
                              src=src_bgp_mvpn_path + '[{}]'.format(key),
                              dest=dest_bgp_mvpn_path + '[{}]'.format(key),
                              vrf='all')

        self.make(final_call=True)