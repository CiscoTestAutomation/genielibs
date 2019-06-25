''' 
Prefix-list Genie Ops Object Outputs for NXOS.
'''


class PrefixListOutput(object):

    ShowIpPrefixList = {        
        "prefix_set_name": {
            "test": {
                 "entries": 6,
                 "protocol": "ipv4",
                 "prefix_set_name": "test",
                 "prefixes": {
                      "10.169.0.0/8 16..24 permit": {
                           "masklength_range": "16..24",
                           "sequence": 25,
                           "prefix": "10.169.0.0/8",
                           "action": "permit"
                      },
                      "10.205.0.0/8 8..16 permit": {
                           "masklength_range": "8..16",
                           "sequence": 10,
                           "prefix": "10.205.0.0/8",
                           "action": "permit"
                      },
                      "10.21.0.0/8 8..16 permit": {
                           "masklength_range": "8..16",
                           "sequence": 15,
                           "prefix": "10.21.0.0/8",
                           "action": "permit"
                      },
                      "10.205.0.0/8 8..8 deny": {
                           "masklength_range": "8..8",
                           "sequence": 5,
                           "prefix": "10.205.0.0/8",
                           "action": "deny"
                      },
                      "10.94.0.0/8 24..32 permit": {
                           "masklength_range": "24..32",
                           "sequence": 20,
                           "prefix": "10.94.0.0/8",
                           "action": "permit"
                      },
                      "192.0.2.0/24 25..25 permit": {
                           "masklength_range": "25..25",
                           "sequence": 30,
                           "prefix": "192.0.2.0/24",
                           "action": "permit"
                      },
                 }
            }
       }
    }

    ShowIpv6PrefixList = {
        "prefix_set_name": {
            "test6": {
                 "entries": 4,
                 "protocol": "ipv6",
                 "prefix_set_name": "test6",
                 "prefixes": {
                      "2001:db8:3::/64 64..128 permit": {
                           "masklength_range": "64..128",
                           "sequence": 15,
                           "prefix": "2001:db8:3::/64",
                           "action": "permit"
                      },
                      "2001:db8:2::/64 65..128 permit": {
                           "masklength_range": "65..128",
                           "sequence": 10,
                           "prefix": "2001:db8:2::/64",
                           "action": "permit"
                      },
                      "2001:db8:1::/64 64..64 permit": {
                           "masklength_range": "64..64",
                           "sequence": 5,
                           "prefix": "2001:db8:1::/64",
                           "action": "permit"
                      },
                      "2001:db8:4::/64 65..98 permit": {
                           "masklength_range": "65..98",
                           "sequence": 20,
                           "prefix": "2001:db8:4::/64",
                           "action": "permit"
                      }
                 }
            }
        }
    }

    PrefixList_info = {
        "prefix_set_name": {
            "test": {
                 "protocol": "ipv4",
                 "prefix_set_name": "test",
                 "prefixes": {
                      "10.169.0.0/8 16..24 permit": {
                           "masklength_range": "16..24",
                           "prefix": "10.169.0.0/8",
                           "action": "permit"
                      },
                      "10.205.0.0/8 8..16 permit": {
                           "masklength_range": "8..16",
                           "prefix": "10.205.0.0/8",
                           "action": "permit"
                      },
                      "10.21.0.0/8 8..16 permit": {
                           "masklength_range": "8..16",
                           "prefix": "10.21.0.0/8",
                           "action": "permit"
                      },
                      "10.205.0.0/8 8..8 deny": {
                           "masklength_range": "8..8",
                           "prefix": "10.205.0.0/8",
                           "action": "deny"
                      },
                      "10.94.0.0/8 24..32 permit": {
                           "masklength_range": "24..32",
                           "prefix": "10.94.0.0/8",
                           "action": "permit"
                      },
                      "192.0.2.0/24 25..25 permit": {
                           "masklength_range": "25..25",
                           "prefix": "192.0.2.0/24",
                           "action": "permit"
                      }
                 }
            },
            "test6": {
                 "protocol": "ipv6",
                 "prefix_set_name": "test6",
                 "prefixes": {
                      "2001:db8:3::/64 64..128 permit": {
                           "masklength_range": "64..128",
                           "prefix": "2001:db8:3::/64",
                           "action": "permit"
                      },
                      "2001:db8:2::/64 65..128 permit": {
                           "masklength_range": "65..128",
                           "prefix": "2001:db8:2::/64",
                           "action": "permit"
                      },
                      "2001:db8:1::/64 64..64 permit": {
                           "masklength_range": "64..64",
                           "prefix": "2001:db8:1::/64",
                           "action": "permit"
                      },
                      "2001:db8:4::/64 65..98 permit": {
                           "masklength_range": "65..98",
                           "prefix": "2001:db8:4::/64",
                           "action": "permit"
                      }
                 }
            }
       }

    }
