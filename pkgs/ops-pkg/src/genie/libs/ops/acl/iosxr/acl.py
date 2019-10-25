''' 
ACL Genie Ops Object for IOSXR - CLI.
'''
# # super class
from genie.libs.ops.acl.acl import Acl as SuperAcl
from genie.ops.base import Context

# Parser
from genie.libs.parser.iosxr.show_acl import ShowAclAfiAll, \
                                        ShowAclEthernetServices

class Acl(SuperAcl):
    '''ACL Genie Ops Object'''
    def actions_forwarding(self, item):
        '''return accept when forwarding is permit and return drop if forwarding is deny'''
        if 'permit' == item['forwarding']:
            return 'accept'
        elif 'deny' == item['forwarding']:
            return 'drop'
        else:
            return 'reject'

    # ethernet types
    ether_types = {
        '0800' : 'ipv4',
        '0806' : 'arp',
        '0842' : 'wlan',
        '22F3' : 'trill',
        '22EA' : 'srp',
        '6003' : 'decnet',
        '8035' : 'rarp',
        '809B' : 'appletalk',
        '80F3' : 'aarp',
        '8100' : 'vlan',
        '8137' : 'ipx',
        '8204' : 'qnx',
        '86DD' : 'ipv6',
        '8808' : 'efc',
        '8809' : 'esp',
        '8819' : 'cobranet',
        '8847' : 'mpls-unicast',
        '8848' : 'mpls-multicast',
        '8863' : 'pppoe-discovery',
        '8864' : 'pppoe-session',
        '886D' : 'intel-ans', 
        '887B' : 'homeplug', 
        '888E' : 'eap',
        '8892' : 'profinet',
        '889A' : 'hyperscsi', 
        '88A2' : 'aoe', 
        '88A4' : 'ethercat', 
        '88A8' : 'provider-bridging',
        '88AB' : 'ethernet-powerlink',
        '88B8' : 'goose',
        '88B9' : 'gse',
        '88BA' : 'sv',
        '88CC' : 'lldp',
        '88CD' : 'sercos',
        '88DC' : 'wsmp', 
        '88E1' : 'homeplug-av-mme',
        '88E3' : 'mrp',
        '88E5' : 'macsec',
        '88E7' : 'pbb',
        '8902' : 'cfm',
        '8906' : 'fcoe',
        '8914' : 'fcoe-ip',
        '8915' : 'roce',
        '891D' : 'tte',
        '892F' : 'hsr'
    }

    def ethernet_type_conversion(self, item):
        item = item.upper()
        val = self.ether_types.get(item, "")
        if val:
            return val
        return item

    def learn(self):
        '''Learn access-list Ops'''

        ########################################################################
        #                               info
        ########################################################################

        # acls
        #     acl_name
        #         name
        #         type
        #         aces
        #             seq
        #                 name
        #                 matches
        #                     l2
        #                         eth
        #                             destination_mac_address
        #                             source_mac_address
        #                             ether_type
        #                     l3
        #                         ipv4
        #                             dscp - N/A
        #                             ecn - N/A
        #                             length - N/A
        #                             ttl
        #                             ttl_operator
        #                             protocol - N/A
        #                             ihl - N/A
        #                             flags - N/A
        #                             offset - N/A
        #                             precedence
        #                             identification - N/A
        #                             destination_ipv4_network
        #                                 dst
        #                                     destination_ipv4_network
        #                             source_ipv4_network
        #                                 src
        #                                     source_ipv4_network
        #                         ipv6 
        #                             dscp - N/A
        #                             ecn - N/A
        #                             length - N/A
        #                             ttl - N/A
        #                             ttl_operator - N/A
        #                             protocol - N/A
        #                             destination_ipv6_network
        #                                 dst
        #                                     destination_ipv6_network
        #                             source_ipv6_network
        #                                 src
        #                                     source_ipv6_network
        #                             flow_label - N/A
        #                     l4
        #                         tcp 
        #                             sequence_number - N/A
        #                             acknowledgement_number - N/A
        #                             data_offset - N/A
        #                             reserved - N/A
        #                             flags - N/A
        #                             window_size - N/A
        #                             urgent_pointer - N/A
        #                             options - N/A
        #                             source-port - N/A
        #                                 range - N/A
        #                                     lower_port - N/A
        #                                     upper_port - N/A
        #                                 operator
        #                                     operator
        #                                     port
        #                             destination_port - N/A
        #                                 range - N/A
        #                                     lower_port - N/A
        #                                     upper_port - N/A
        #                                 operator
        #                                     operator
        #                                     port
        #                         udp - N/A
        #                             length - N/A
        #                             source-port - N/A
        #                                 range - N/A
        #                                     lower_port - N/A
        #                                     upper_port - N/A
        #                                 operator - N/A
        #                                     operator - N/A
        #                                     port - N/A
        #                             destination_port - N/A
        #                                 range - N/A
        #                                     lower_port - N/A
        #                                     upper_port - N/A
        #                                 operator - N/A
        #                                     operator - N/A
        #                                     port - N/A
        #                         icmp - N/A
        #                             type - N/A
        #                             code - N/A
        #                             rest_of_header - N/A
        #                     egress_interface - N/A
        #                     ingress_interface - N/A
        #                 statistics - N/A
        #                     matched_packets - N/A
        #                     matched_octets - N/A
        # attachment_points - N/A
        #     interface_id - N/A
        #         interface_id - N/A
        #         ingress - N/A
        #             acl_sets - N/A
        #                 acl_name - N/A
        #                     name - N/A
        #                     ace_statistics - N/A
        #                         matched_packets - N/A
        #                         matched_octets - N/A
        #         egress - N/A
        #             acl_sets - N/A
        #                 acl_name - N/A
        #                     name - N/A
        #                     ace_statistics - N/A
        #                         matched_packets - N/A
        #                         matched_octets - N/A

        # l2
        l2_src = '[(?P<name>.*)][aces][(?P<aces>.*)][matches][l2][eth]'
        l2_dest = 'info[acls]' + l2_src

        # l3
        l3_v4_src = '[(?P<name>.*)][aces][(?P<aces>.*)][matches][l3][ipv4]'
        l3_v4_dest = 'info[acls]' + l3_v4_src
        l3_v6_src = '[(?P<name>.*)][aces][(?P<aces>.*)][matches][l3][ipv6]'
        l3_v6_dest = 'info[acls]' + l3_v6_src

        # l4
        l4_tcp_src = '[(?P<name>.*)][aces][(?P<aces>.*)][matches][l4][tcp]'
        l4_tcp_dest = 'info[acls]' + l4_tcp_src

        action_src = '[(?P<name>.*)][aces][(?P<aces>.*)][actions]'
        action_dest = 'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][actions]'

        # prepare the keys
        # dictonary as {src: dest,}
        keys_show_acl_afi_all = {
            '[(?P<name>.*)][name]': 'info[acls][(?P<name>.*)][name]',
            '[(?P<name>.*)][type]': 'info[acls][(?P<name>.*)][type]',
            '[(?P<name>.*)][aces][(?P<aces>.*)][name]': 
                'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][name]',
            action_src + '[logging]' : action_dest + '[logging]',
            l3_v4_src + '[ttl]': l3_v4_dest + '[ttl]',
            l3_v4_src + '[ttl_operator]': l3_v4_dest + '[ttl_operator]',
            l3_v4_src + '[precedence]': l3_v4_dest + '[precedence]',
            l3_v4_src + '[destination_ipv4_network][(?P<ipv4>.*)][destination_ipv4_network]': 
                l3_v4_dest + '[destination_ipv4_network][(?P<ipv4>.*)][destination_ipv4_network]',
            l3_v4_src + '[source_ipv4_network][(?P<ipv4_s>.*)][source_ipv4_network]': 
                l3_v4_dest + '[source_ipv4_network][(?P<ipv4_s>.*)][source_ipv4_network]',
            
            l3_v6_src + '[ttl]': l3_v6_dest + '[ttl]',
            l3_v6_src + '[ttl_operator]': l3_v6_dest + '[ttl_operator]',
            l3_v6_src + '[destination_ipv6_network][(?P<ipv6>.*)][destination_ipv6_network]': 
                l3_v6_dest + '[destination_ipv6_network][(?P<ipv6>.*)][destination_ipv6_network]',
            l3_v6_src + '[source_ipv6_network][(?P<ipv6_s>.*)][source_ipv6_network]': 
                l3_v6_dest + '[source_ipv6_network][(?P<ipv6_s>.*)][source_ipv6_network]',
            
            l4_tcp_src + '[established]': l4_tcp_dest + '[established]',
            l4_tcp_src + '[source-port]': l4_tcp_dest + '[source-port]',
            l4_tcp_src + '[destination_port]': l4_tcp_dest + '[destination_port]',
        }

        for src, dst in keys_show_acl_afi_all.items():       
            self.add_leaf(cmd=ShowAclAfiAll,
                          src=src,
                          dest=dst)
        # enabled
        self.add_leaf(cmd=ShowAclAfiAll,
                      src=action_src,
                      dest=action_dest + '[forwarding]',
                      action=self.actions_forwarding)
        # prepare the keys
        # dictonary as {src: dest,}
        keys_ethernet_services = {
            '[(?P<name>.*)][name]': 'info[acls][(?P<name>.*)][name]',
            '[(?P<name>.*)][type]': 'info[acls][(?P<name>.*)][type]',
            '[(?P<name>.*)][aces][(?P<aces>.*)][name]': 
                'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][name]',
                 action_src + '[logging]' : action_dest + '[logging]',
            l2_src + '[destination_mac_address]': l2_dest + '[destination_mac_address]',
            l2_src + '[source_mac_address]': l2_dest + '[source_mac_address]',
        }

        for src, dst in keys_ethernet_services.items():       
            self.add_leaf(cmd=ShowAclEthernetServices,
                          src=src,
                          dest=dst)
        
        # enabled
        self.add_leaf(cmd=ShowAclEthernetServices,
                      src=action_src,
                      dest=action_dest + '[forwarding]',
                      action=self.actions_forwarding)

        # ether_type conversion
        self.add_leaf(cmd=ShowAclEthernetServices,
                      src=l2_src + '[ether_type]',
                      dest=l2_dest + '[ether_type]',
                      action=self.ethernet_type_conversion)
        # make to write in cache
        self.make(final_call=True)