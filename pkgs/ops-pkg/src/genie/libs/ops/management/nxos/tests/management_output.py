class ManagementOutput(object):

    showIPRoute = """
        S1-P1-L101# show ip route vrf management
        IP Route Table for VRF "management"
        '*' denotes best ucast next-hop
        '**' denotes best mcast next-hop
        '[x/y]' denotes [preference/metric]
        '%<string>' in via output denotes VRF <string>
        192.168.1.0/24, ubest/mbest: 1/0, attached, direct, pervasive
            *via 10.11.200.98%overlay-1, [1/0], 02w00d, static, tag 4294967294
        192.168.1.1/32, ubest/mbest: 1/0, attached, pervasive
            *via 192.168.1.1, vlan60, [0/0], 02w00d, local, local
        192.168.100.0/24, ubest/mbest: 1/0, attached, direct, pervasive
            *via 10.11.200.98%overlay-1, [1/0], 02w00d, static, tag 4294967294
        192.168.100.1/32, ubest/mbest: 1/0, attached, pervasive
            *via 192.168.100.1, vlan14, [0/0], 02w00d, local, local
        192.168.254.0/24, ubest/mbest: 1/0, attached, direct, pervasive
            *via 10.11.200.98%overlay-1, [1/0], 02w00d, static, tag 4294967294
        192.168.254.1/32, ubest/mbest: 1/0, attached, pervasive
            *via 192.168.254.1, vlan39, [0/0], 02w00d, local, local
        S1-P1-L101#
    """

    ManagementOpsOutput = {
        "management": {
            "ipv4_address": "192.168.1.1",
            "ipv4": {
                "routes": {
                    "192.168.254.1/32": {
                        "next_hop": "192.168.254.1",
                        "outgoing_interface": "Vlan39",
                        "source_protocol": "local"
                    },
                    "192.168.254.0/24": {
                        "next_hop": "10.11.200.98",
                        "source_protocol": "static"
                    },
                    "192.168.100.1/32": {
                        "next_hop": "192.168.100.1",
                        "outgoing_interface": "Vlan14",
                        "source_protocol": "local"
                    },
                    "192.168.100.0/24": {
                        "next_hop": "10.11.200.98",
                        "source_protocol": "static"
                    },
                    "192.168.1.1/32": {
                        "next_hop": "192.168.1.1",
                        "outgoing_interface": "Vlan60",
                        "source_protocol": "local"
                    },
                    "192.168.1.0/24": {
                        "next_hop": "10.11.200.98",
                        "source_protocol": "static"
                    }
                }
            },
            "interface": "mgmt0",
            "vrf": "management"
        }
    }