# super class
from genie.libs.ops.vxlan.vxlan import Vxlan as SuperVxlan
from genie.libs.parser.iosxe.show_nve import ShowNveInterfaceDetail,\
                                             ShowNveVni
from genie.libs.parser.iosxe.show_run import ShowRunInterface


class Vxlan(SuperVxlan):
    '''Vxlan Ops Object'''

    def learn(self):
        '''Learn vxlan object'''

        #  nve_name
        #    vni
        #        nve_vni
        #            interface
        #            vni
        #            mcast
        #            vni_state
        #            mode
        #            Optional(vlan)
        #            Optional(bd)
        #            cfg
        #            vrf
        #            Optional(ingress_replication)
        #                enabled
        #                Optional(remote_peer_ip)

        src_nve_vni = '[(?P<nve_name>^nve.*)][(?P<nve_vni>.*)]'
        dest_nve_vni = 'nve[(?P<nve_name>^nve.*)][vni][(?P<nve_vni>.*)]'

        req_key = [ 'mcast', 'vni_state', 'mode', 'vlan', 'bd','cfg', 'vrf']
        for key in req_key:
            self.add_leaf(cmd=ShowNveVni,
                          src=src_nve_vni + '[{}]'.format(key),
                          dest=dest_nve_vni + '[{}]'.format(key))
        self.make()

        try:
            nve_name_list = self.nve.keys()
        except:
            nve_name_list = []

        for nve_name in nve_name_list:
            if 'nve' in nve_name:
                src_nve = '[interfaces][(?P<nve_name>.*)]'
                dest_nve = 'nve[(?P<nve_name>^nve.*)][vni][(?P<nve_vni>.*)]'

                req_key = ['enabled', 'remote_peer_ip']
                for key in req_key:
                    self.add_leaf(cmd=ShowRunInterface,
                                  src=src_nve + '[member_vni][(?P<nve_vni>.*)][ingress_replication]'
                                                '[{}]'.format(key),
                                  dest=dest_nve + '[ingress_replication][{}]'.format(key),
                                  interface=nve_name)
        self.make()

        # nve_name
        #    admin_state
        #    oper_state
        #    encap
        #    bgp_host_reachability
        #    vxlan_dport
        #    num_l3vni_cp
        #    num_l2vni_cp
        #    num_l2vni_dp
        #    tunnel_intf
        #       counters
        #          pkts_in
        #          bytes_in
        #          pkts_out
        #          bytes_out
        #    src_intf
        #        intf
        #            primary_ip
        #            vrf

        try:
            nve_name_list = self.nve.keys()
        except:
            nve_name_list = []

        for nve_name in nve_name_list:
            if 'nve' in nve_name:
                dest_nve = 'nve[{nve_name}]'.format(nve_name=nve_name)

            nve, nve_itf_num= nve_name.split('nve')
            req_key =['admin_state', 'oper_state', 'encap', 'bgp_host_reachability',\
                      'vxlan_dport', 'num_l3vni_cp', 'num_l2vni_cp', 'num_l2vni_dp', 'tunnel_intf']
            for key in req_key:
                self.add_leaf(cmd=ShowNveInterfaceDetail,
                              src='[{}]'.format(key),
                              dest=dest_nve + '[{}]'.format(key),
                              nve_num=nve_itf_num)

            self.add_leaf(cmd=ShowNveInterfaceDetail,
                          src='[src_intf][(?P<source_if>.*)]',
                          dest=dest_nve + '[src_intf][(?P<source_if>.*)]',
                          nve_num=nve_itf_num)
            self.add_leaf(cmd=ShowNveInterfaceDetail,
                          src='[src_intf][(?P<source_if>.*)][primary_ip]',
                          dest=dest_nve + '[src_intf][(?P<source_if>.*)][primary_ip]',
                          nve_num=nve_itf_num)
            self.add_leaf(cmd=ShowNveInterfaceDetail,
                          src='[src_intf][(?P<source_if>.*)][vrf]',
                          dest=dest_nve + '[src_intf][(?P<source_if>.*)][vrf]',
                          nve_num=nve_itf_num)

            req_key =['pkts_in', 'bytes_in', 'pkts_out', 'bytes_out']
            for key in req_key:
                self.add_leaf(cmd=ShowNveInterfaceDetail,
                              src='[tunnel_intf][(?P<tun_intf>.*)][counters][{}]'.format(key),
                              dest=dest_nve + '[tunnel_intf][(?P<tun_intf>.*)]'
                                              '[counters][{}]'.format(key),
                              nve_num=nve_itf_num)
        self.make(final_call=True)
