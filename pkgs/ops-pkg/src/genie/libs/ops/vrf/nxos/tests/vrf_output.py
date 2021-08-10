''' 
Vrf Genie Ops Object Outputs for NXOS.
'''


class VrfOutput(object):
    ShowVrfDetail = {
        "management": {
            "max_routes": 0,
            "state": "up",
            "vrf_id": 2,
            "address_family": {
                "ipv6": {
                    "table_id": "0x80000002",
                    "state": "up",
                    "fwd_id": "0x80000002"
                },
                "ipv4": {
                    "table_id": "0x00000002",
                    "state": "up",
                    "fwd_id": "0x00000002"
                }
            },
            "mid_threshold": 0,
            "route_distinguisher": "0:0"
        },
        "default": {
            "max_routes": 0,
            "state": "up",
            "vrf_id": 1,
            "address_family": {
                "ipv6": {
                    "table_id": "0x80000001",
                    "state": "up",
                    "fwd_id": "0x80000001"
                },
                "ipv4": {
                    "table_id": "0x00000001",
                    "state": "up",
                    "fwd_id": "0x00000001"
                }
            },
            "mid_threshold": 0,
            "route_distinguisher": "0:0"
        },
        "VRF2": {
            "max_routes": 0,
            "state": "up",
            "vrf_id": 4,
            "address_family": {
                "ipv6": {
                    "table_id": "0x80000004",
                    "state": "up",
                    "fwd_id": "0x80000004"
                },
                "ipv4": {
                    "table_id": "0x00000004",
                    "state": "up",
                    "fwd_id": "0x00000004"
                }
            },
            "mid_threshold": 0,
            "route_distinguisher": "400:1"
        },
        "VRF1": {
            "max_routes": 20000,
            "state": "up",
            "vrf_id": 3,
            "address_family": {
                "ipv6": {
                    "table_id": "0x80000003",
                    "state": "up",
                    "fwd_id": "0x80000003"
                },
                "ipv4": {
                    "table_id": "0x00000003",
                    "state": "up",
                    "fwd_id": "0x00000003"
                }
            },
            "mid_threshold": 17000,
            "route_distinguisher": "300:1"
        }
    }
    ShowVrfDetailCustom = {
        "default": {
            "max_routes": 0,
            "state": "up",
            "vrf_id": 1,
            "address_family": {
                "ipv6": {
                    "table_id": "0x80000001",
                    "state": "up",
                    "fwd_id": "0x80000001"
                },
                "ipv4": {
                    "table_id": "0x00000001",
                    "state": "up",
                    "fwd_id": "0x00000001"
                }
            },
            "mid_threshold": 0,
            "route_distinguisher": "0:0"
        },
    }

    VrfInfo = {
    "vrfs": {
        "management": {
            "route_distinguisher": "0:0",
            "address_family": {
                "ipv4": {"table_id": "0x00000002"},
                "ipv6": {"table_id": "0x80000002"},
            },
        },
        "default": {
            "route_distinguisher": "0:0",
            "address_family": {
                "ipv4": {"table_id": "0x00000001"},
                "ipv6": {"table_id": "0x80000001"},
            },
        },
        "VRF2": {
            "route_distinguisher": "400:1",
            "address_family": {
                "ipv4": {"table_id": "0x00000004"},
                "ipv6": {"table_id": "0x80000004"},
            },
        },
        "VRF1": {
            "route_distinguisher": "300:1",
            "address_family": {
                "ipv4": {"table_id": "0x00000003"},
                "ipv6": {"table_id": "0x80000003"},
            },
        },
    }
}

    showVrfDetail_default = '''
VRF-Name: default, VRF-ID: 1, State: Up
        VPNID: unknown
        RD: 0:0
        Max Routes: 0  Mid-Threshold: 0
        Table-ID: 0x80000001, AF: IPv6, Fwd-ID: 0x80000001, State: Up
        Table-ID: 0x00000001, AF: IPv4, Fwd-ID: 0x00000001, State: Up
    '''
    showVrfDetail_all = '''
        VRF-Name: VRF1, VRF-ID: 3, State: Up
            VPNID: unknown
            RD: 300:1
            Max Routes: 20000  Mid-Threshold: 17000
            Table-ID: 0x80000003, AF: IPv6, Fwd-ID: 0x80000003, State: Up
            Table-ID: 0x00000003, AF: IPv4, Fwd-ID: 0x00000003, State: Up

        VRF-Name: VRF2, VRF-ID: 4, State: Up
            VPNID: unknown
            RD: 400:1
            Max Routes: 0  Mid-Threshold: 0
            Table-ID: 0x80000004, AF: IPv6, Fwd-ID: 0x80000004, State: Up
            Table-ID: 0x00000004, AF: IPv4, Fwd-ID: 0x00000004, State: Up

        VRF-Name: default, VRF-ID: 1, State: Up
            VPNID: unknown
            RD: 0:0
            Max Routes: 0  Mid-Threshold: 0
            Table-ID: 0x80000001, AF: IPv6, Fwd-ID: 0x80000001, State: Up
            Table-ID: 0x00000001, AF: IPv4, Fwd-ID: 0x00000001, State: Up

        VRF-Name: management, VRF-ID: 2, State: Up
            VPNID: unknown
            RD: 0:0
            Max Routes: 0  Mid-Threshold: 0
            Table-ID: 0x80000002, AF: IPv6, Fwd-ID: 0x80000002, State: Up
            Table-ID: 0x00000002, AF: IPv4, Fwd-ID: 0x00000002, State: Up
    '''

    VrfCustomInfo = {
    "vrfs": {
        "default": {
            "route_distinguisher": "0:0",
            "address_family": {
                "ipv4": {"table_id": "0x00000001"},
                "ipv6": {"table_id": "0x80000001"},
            },
        }
    }
}




