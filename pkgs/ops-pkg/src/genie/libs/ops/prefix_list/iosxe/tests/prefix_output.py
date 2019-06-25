''' 
Prefix-list Genie Ops Object Outputs for IOSXE.
'''


class PrefixListOutput(object):

    ShowIpPrefixListDetail = {    
        
        "prefix_set_name": {
          "test": {
               "sequences": "5 - 25",
               "prefixes": {
                    "10.205.0.0/8 8..16 permit": {
                         "refcount": 0,
                         "prefix": "10.205.0.0/8",
                         "sequence": 10,
                         "hit_count": 0,
                         "masklength_range": "8..16",
                         "action": "permit",
                    },
                    "10.21.0.0/8 8..16 permit": {
                         "refcount": 1,
                         "prefix": "10.21.0.0/8",
                         "sequence": 15,
                         "hit_count": 0,
                         "masklength_range": "8..16",
                         "action": "permit",
                    },
                    "10.169.0.0/8 16..24 permit": {
                         "refcount": 3,
                         "prefix": "10.169.0.0/8",
                         "sequence": 25,
                         "hit_count": 0,
                         "masklength_range": "16..24",
                         "action": "permit",
                    },
                    "10.94.0.0/8 24..32 permit": {
                         "refcount": 2,
                         "prefix": "10.94.0.0/8",
                         "sequence": 20,
                         "hit_count": 0,
                         "masklength_range": "24..32",
                         "action": "permit",
                    },
                    "10.205.0.0/8 8..8 permit": {
                         "refcount": 1,
                         "prefix": "10.205.0.0/8",
                         "sequence": 5,
                         "hit_count": 0,
                         "masklength_range": "8..8",
                         "action": "permit",
                    }
               },
               "protocol": "ipv4",
               "refcount": 2,
               "range_entries": 4,
               "count": 5,
               "prefix_set_name": "test"
          }
       }
    }

    ShowIpv6PrefixListDetail = {
        "prefix_set_name": {
          "test6": {
               "sequences": "5 - 20",
               "prefixes": {
                    "2001:DB8:2::/64 65..128 permit": {
                         "refcount": 1,
                         "prefix": "2001:DB8:2::/64",
                         "sequence": 10,
                         "hit_count": 0,
                         "action": "permit",
                         "masklength_range": "65..128"
                    },
                    "2001:DB8:3::/64 64..128 permit": {
                         "refcount": 3,
                         "prefix": "2001:DB8:3::/64",
                         "sequence": 15,
                         "hit_count": 0,
                         "action": "permit",
                         "masklength_range": "64..128"
                    },
                    "2001:DB8:1::/64 64..64 permit": {
                         "refcount": 1,
                         "prefix": "2001:DB8:1::/64",
                         "sequence": 5,
                         "hit_count": 0,
                         "action": "permit",
                         "masklength_range": "64..64"
                    }
               },
               "protocol": "ipv6",
               "refcount": 2,
               "range_entries": 3,
               "count": 4,
               "prefix_set_name": "test6"
          }
       }
    }

    PrefixList_info = {
        "prefix_set_name": {
          "test": {
               "protocol": "ipv4",
               "prefix_set_name": "test",
               "prefixes": {
                    "10.205.0.0/8 8..16 permit": {
                         "prefix": "10.205.0.0/8",
                         "action": "permit",
                         "masklength_range": "8..16"
                    },
                    "10.94.0.0/8 24..32 permit": {
                         "prefix": "10.94.0.0/8",
                         "action": "permit",
                         "masklength_range": "24..32"
                    },
                    "10.21.0.0/8 8..16 permit": {
                         "prefix": "10.21.0.0/8",
                         "action": "permit",
                         "masklength_range": "8..16"
                    },
                    "10.205.0.0/8 8..8 permit": {
                         "prefix": "10.205.0.0/8",
                         "action": "permit",
                         "masklength_range": "8..8"
                    },
                    "10.169.0.0/8 16..24 permit": {
                         "prefix": "10.169.0.0/8",
                         "action": "permit",
                         "masklength_range": "16..24"
                    }
               }
          },
          "test6": {
               "protocol": "ipv6",
               "prefix_set_name": "test6",
               "prefixes": {
                    "2001:DB8:1::/64 64..64 permit": {
                         "prefix": "2001:DB8:1::/64",
                         "action": "permit",
                         "masklength_range": "64..64"
                    },
                    "2001:DB8:2::/64 65..128 permit": {
                         "prefix": "2001:DB8:2::/64",
                         "action": "permit",
                         "masklength_range": "65..128"
                    },
                    "2001:DB8:3::/64 64..128 permit": {
                         "prefix": "2001:DB8:3::/64",
                         "action": "permit",
                         "masklength_range": "64..128"
                    }
               }
          }
       }

    }
