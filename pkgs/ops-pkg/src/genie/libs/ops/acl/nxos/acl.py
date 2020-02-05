"""
ACL Genie Ops Object for NXOS
"""
import re
# super class
from genie.libs.ops.acl.acl import Acl as SuperAcl
# parser
from genie.libs.parser.nxos.show_acl import ShowAccessLists, ShowAccessListsSummary


# helper function
def create_dict(src_dict, dest_dict, list_of_keys):
    result = {}
    tail = ''
    for i in list_of_keys:
        # 'KEY1, KEY2, KEY3'
        if ',' in i:
            list_of_i = i.split(', ')  # ['KEY1', 'KEY2', 'KEY3']
            tail = ''.join(['[%s]' % j for j in list_of_i])  # '[KEY1][KEY2][KEY3]'
        else:
            tail = '[%s]' % i
        k = src_dict + tail
        k = re.sub(r'destination_ipv6_network', 'destination_network', k)
        k = re.sub(r'destination_ipv4_network', 'destination_network', k)
        k = re.sub(r'source_ipv6_network', 'source_network', k)
        k = re.sub(r'source_ipv4_network', 'source_network', k)
        v = dest_dict + tail
        result[k] = v

    return result

class Acl(SuperAcl):
    """Acl Genie Ops Object"""

    def actions_forwarding(self, item):
        """return accept when forwarding is permit and return drop if forwarding is deny"""
        if 'permit' == item['forwarding']:
            return 'accept'
        elif 'deny' == item['forwarding']:
            return 'drop'
        else:
            return 'reject'

    def learn(self, acl=''):
        """Learn access-list Ops"""

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

        ace_src = '[(?P<name>.*)][aces][(?P<aces>.*)][matches]'

        # l2
        l2_src = ace_src+'[l2][eth]'
        l2_dest = 'info[acls]' + l2_src

        #                     l3
        #                         ipv4
        #                             dscp - N/A
        #                             ecn - N/A
        #                             length - N/A
        #                             ttl
        #                             ttl_operator N/A
        #                             protocol
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
        #                             protocol
        #                             destination_ipv6_network
        #                                 dst
        #                                     destination_ipv6_network
        #                             source_ipv6_network
        #                                 src
        #                                     source_ipv6_network
        #                             flow_label - N/A

        # l3
        l3_v4_src = ace_src+'[l3][ipv4]'
        l3_v4_dest = 'info[acls]' + l3_v4_src
        l3_v6_src = ace_src+'[l3][ipv6]'
        l3_v6_dest = 'info[acls]' + l3_v6_src

        #                     l4
        #                         tcp
        #                             sequence_number - N/A
        #                             acknowledgement_number N/A
        #                             data_offset N/A
        #                             reserved N/A
        #                             flags N/A
        #                             window_size N/A
        #                             urgent_pointer N/A
        #                             options N/A
        #                             established
        #                             source-port
        #                                 range - N/A
        #                                     lower_port - N/A
        #                                     upper_port - N/A
        #                                 operator
        #                                     operator
        #                                     port
        #                             destination_port
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
        #                 actions
        #                     forwarding
        #                     logging
        #                 statistics - N/A
        #                     matched_packets - N/A
        #                     matched_octets - N/A

        # l4
        l4_tcp_src = ace_src+'[l4][tcp]'
        l4_tcp_dest = 'info[acls]' + l4_tcp_src

        action_src = '[(?P<name>.*)][aces][(?P<aces>.*)][actions]'
        action_dest = 'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][actions]'

        # prepare the keys
        base_dict = {'[(?P<name>.*)][name]': 'info[acls][(?P<name>.*)][name]',
                     '[(?P<name>.*)][type]': 'info[acls][(?P<name>.*)][type]',
                     '[(?P<name>.*)][aces][(?P<aces>.*)][name]':'info[acls][(?P<name>.*)][aces][(?P<aces>.*)][name]',
                     action_src + '[logging]': action_dest + '[logging]'}

        l2_keys = ['destination_mac_address', 'source_mac_address', 'ether_type']
        l2_dict = create_dict(l2_src, l2_dest, l2_keys)

        # Note: use comma plus one space to separate two keys: 'KEY1, KEY2'
        l3_v4_keys = ['ttl', 'ttl_operator', 'protocol', 'precedence',
                      'destination_ipv4_network, (?P<ipv4>.*), destination_ipv4_network',
                      'source_ipv4_network, (?P<ipv4_s>.*), source_ipv4_network']
        l3_v4_dict = create_dict(l3_v4_src, l3_v4_dest, l3_v4_keys)

        l3_v6_keys = ['protocol',
                      'destination_ipv6_network, (?P<ipv6>.*), destination_ipv6_network',
                      'source_ipv6_network, (?P<ipv6_s>.*), source_ipv6_network']
        l3_v6_dict = create_dict(l3_v6_src, l3_v6_dest, l3_v6_keys)

        l4_tcp_keys = ['established', 'source-port', 'destination_port']
        l4_tcp_dict = create_dict(l4_tcp_src, l4_tcp_dest, l4_tcp_keys)

        keys_show_access_lists = {}
        for dictionary in [base_dict, l2_dict, l3_v4_dict, l3_v6_dict, l4_tcp_dict]:
            keys_show_access_lists.update(dictionary)

        for src, dst in keys_show_access_lists.items():
            self.add_leaf(cmd=ShowAccessLists,
                          src=src,
                          dest=dst)

        # enabled
        self.add_leaf(cmd=ShowAccessLists,
                      src=action_src,
                      dest=action_dest + '[forwarding]',
                      action=self.actions_forwarding)

        # attachment_points
        #     interface_id
        #         interface_id
        #         ingress
        #             acl_sets
        #                 acl_name
        #                     name
        #                     ace_statistics - N/A
        #                         matched_packets - N/A
        #                         matched_octets - N/A
        #         egress
        #             acl_sets
        #                 acl_name
        #                     name
        #                     ace_statistics - N/A
        #                         matched_packets - N/A
        #                         matched_octets - N/A

        ap_src = '[attachment_points][(?P<interface_id>.*)]'
        ap_dest = 'info'+ap_src
        self.add_leaf(cmd=ShowAccessListsSummary,
                      src=ap_src+'[interface_id]',
                      dest=ap_dest+'[interface_id]')

        for i in ['ingress', 'egress']:
            self.add_leaf(cmd=ShowAccessListsSummary,
                          src=ap_src+'[{i}][(?P<name>.*)][name]'.format(i=i),
                          dest=ap_dest+'[{i}][acl_sets][(?P<name>.*)][name]'.format(i=i))

        self.make(final_call=True)

