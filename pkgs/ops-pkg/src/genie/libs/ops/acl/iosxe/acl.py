''' 
ACL Genie Ops Object for IOSXE - CLI.
'''
# # super class
from genie.libs.ops.acl.acl import Acl as SuperAcl
# Parser
from genie.libs.parser.iosxe.show_acl import ShowAccessLists


class Acl(SuperAcl):
    '''ACL Genie Ops Object'''

    def learn(self):
        '''Learn access-list Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        # unsupported keys
        # ecn, length, ihl, flags, offset, identification
        # flow_label, acknowledgement_number, data_offset
        # reserved, flags, window_size, urgent_pointer
        # rest_of_header, egress_interface, ingress_interface
        # ingress_interface, attachment_points, sequence_number

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
        l4_udp_src = '[(?P<name>.*)][aces][(?P<aces>.*)][matches][l4][udp]'
        l4_udp_dest = 'info[acls]' + l4_udp_src
        l4_icmp_src = '[(?P<name>.*)][aces][(?P<aces>.*)][matches][l4][icmp]'
        l4_icmp_dest = 'info[acls]' + l4_icmp_src

        # prepare the keys
        # dictonary as {src: dest,}
        keys = {
            '[(?P<name>.*)][name]': 'info[acls][(?P<name>.*)][name]',
            '[(?P<name>.*)][type]': 'info[acls][(?P<name>.*)][type]',
            '[(?P<name>.*)][aces][(?P<aces>.*)][name]': 
                'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][name]',
            '[(?P<name>.*)][aces][(?P<aces>.*)][actions]': 
                'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][actions]',
            '[(?P<name>.*)][aces][(?P<aces>.*)][statistics]': 
                'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][statistics]',
            l2_src + '[destination_mac_address]': l2_dest + '[destination_mac_address]',
            l2_src + '[source_mac_address]': l2_dest + '[source_mac_address]',
            l2_src + '[ether_type]': l2_dest + '[ether_type]',
            l3_v4_src + '[dscp]': l3_v4_dest + '[dscp]',
            l3_v4_src + '[ttl]': l3_v4_dest + '[ttl]',
            l3_v4_src + '[ttl_operator]': l3_v4_dest + '[ttl_operator]',
            l3_v4_src + '[protocol]': l3_v4_dest + '[protocol]',
            l3_v4_src + '[precedence]': l3_v4_dest + '[precedence]',
            l3_v4_src + '[destination_network][(?P<ipv4>.*)][destination_network]': 
                l3_v4_dest + '[destination_ipv4_network][(?P<ipv4>.*)][destination_ipv4_network]',
            l3_v4_src + '[source_network][(?P<ipv4_s>.*)][source_network]': 
                l3_v4_dest + '[source_ipv4_network][(?P<ipv4_s>.*)][source_ipv4_network]',
            l3_v6_src + '[dscp]': l3_v6_dest + '[dscp]',
            l3_v6_src + '[ttl]': l3_v6_dest + '[ttl]',
            l3_v6_src + '[ttl_operator]': l3_v6_dest + '[ttl_operator]',
            l3_v6_src + '[destination_network][(?P<ipv6>.*)][destination_network]': 
                l3_v6_dest + '[destination_ipv6_network][(?P<ipv6>.*)][destination_ipv6_network]',
            l3_v6_src + '[source_network][(?P<ipv6_s>.*)][source_network]': 
                l3_v6_dest + '[source_ipv6_network][(?P<ipv6_s>.*)][source_ipv6_network]',
            l3_v6_src + '[protocol]': l3_v6_dest + '[protocol]',
            l4_tcp_src + '[options]': l4_tcp_dest + '[options]',
            l4_tcp_src + '[established]': l4_tcp_dest + '[established]',
            l4_tcp_src + '[source_port]': l4_tcp_dest + '[source_port]',
            l4_tcp_src + '[destination_port]': l4_tcp_dest + '[destination_port]',
            l4_udp_src + '[source_port]': l4_udp_dest + '[source_port]',
            l4_udp_src + '[destination_port]': l4_udp_dest + '[destination_port]',
            l4_icmp_src + '[type]': l4_icmp_dest + '[type]',
            l4_icmp_src + '[code]': l4_icmp_dest + '[code]',
        }

        for src, dst in keys.items():       

            self.add_leaf(cmd='show access-lists',
                          src=src,
                          dest=dst)

        # make to write in cache
        self.make(final_call=True)
