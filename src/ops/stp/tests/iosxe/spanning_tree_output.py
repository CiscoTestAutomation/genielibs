'''STP Genie Ops Object Outputs for IOSXE.'''


class StpMstOutput(object):

    ShowSpanningTreeDetail = {
        "mstp": {
              "mst_instances": {
                   0: {
                        "hello_timer": 0,
                        "notification_timer": 0,
                        "bridge_sysid": 0,
                        "forwarding_delay": 30,
                        "hello_time": 10,
                        "topology_change_timer": 0,
                        "time_since_topology_change": "03:09:48",
                        "notification_times": 10,
                        "mst_id": 0,
                        "topology_change_flag": False,
                        "root_of_spanning_tree": True,
                        "hold_time": 1,
                        "topology_changes": 3,
                        "bridge_address": "d8b1.9009.bf80",
                        "interfaces": {
                             "Port-channel24": {
                                  "number_of_forward_transitions": 1,
                                  "designated_port_id": "128.2400",
                                  "status": "designated forwarding",
                                  "designated_bridge_priority": 32768,
                                  "forward_delay": 0,
                                  "designated_bridge_address": "d8b1.9009.bf80",
                                  "designated_path_cost": 0,
                                  "designated_root_priority": 32768,
                                  "port_identifier": "128.2400.",
                                  "cost": 6660,
                                  "counters": {
                                       "bpdu_sent": 1099019,
                                       "bpdu_received": 2191582
                                  },
                                  "designated_root_address": "d8b1.9009.bf80",
                                  "boundary": "PVST",
                                  "port_num": 2400,
                                  "port_priority": 128,
                                  "name": "Port-channel24",
                                  "hold": 0,
                                  "message_age": 0,
                                  "link_type": "point-to-point",
                                  "loop_guard": True
                             },
                             "Port-channel14": {
                                  "number_of_forward_transitions": 0,
                                  "designated_port_id": "128.2390",
                                  "status": "broken  (PVST Sim. Inconsistent)",
                                  "designated_bridge_priority": 32768,
                                  "forward_delay": 0,
                                  "designated_bridge_address": "d8b1.9009.bf80",
                                  "designated_path_cost": 0,
                                  "designated_root_priority": 32768,
                                  "port_identifier": "128.2390.",
                                  "cost": 6660,
                                  "counters": {
                                       "bpdu_sent": 138231,
                                       "bpdu_received": 167393
                                  },
                                  "designated_root_address": "d8b1.9009.bf80",
                                  "boundary": "PVST",
                                  "port_num": 2390,
                                  "port_priority": 128,
                                  "name": "Port-channel14",
                                  "hold": 0,
                                  "message_age": 0,
                                  "link_type": "point-to-point",
                                  "loop_guard": True
                             }
                        },
                        "topology_change_times": 70,
                        "topology_from_port": "Port-channel24",
                        "bridge_priority": 32768,
                        "topology_detected_flag": False,
                        "max_age": 40
                   },
                   10: {
                        "hello_timer": 0,
                        "notification_timer": 0,
                        "bridge_sysid": 0,
                        "forwarding_delay": 30,
                        "hello_time": 10,
                        "topology_change_timer": 0,
                        "time_since_topology_change": "03:09:48",
                        "notification_times": 10,
                        "mst_id": 0,
                        "topology_change_flag": False,
                        "root_of_spanning_tree": False,
                        "hold_time": 1,
                        "topology_changes": 3,
                        "bridge_address": "d8b1.9009.bf80",
                        "interfaces": {
                             "GigabitEthernet1/0/5": {
                                  "number_of_forward_transitions": 1,
                                  "designated_port_id": "128.2400",
                                  "status": "designated forwarding",
                                  "designated_bridge_priority": 32768,
                                  "forward_delay": 0,
                                  "designated_bridge_address": "d8b1.9009.bf80",
                                  "designated_path_cost": 0,
                                  "designated_root_priority": 32768,
                                  "port_identifier": "128.2400.",
                                  "cost": 6660,
                                  "counters": {
                                       "bpdu_sent": 1099019,
                                       "bpdu_received": 2191582
                                  },
                                  "designated_root_address": "d8b1.9009.bf80",
                                  "boundary": "PVST",
                                  "port_num": 2400,
                                  "port_priority": 128,
                                  "name": "Port-channel24",
                                  "hold": 0,
                                  "message_age": 0,
                                  "link_type": "point-to-point",
                                  "loop_guard": True
                             },
                             "Port-channel14": {
                                  "number_of_forward_transitions": 0,
                                  "designated_port_id": "128.2390",
                                  "status": "broken  (PVST Sim. Inconsistent)",
                                  "designated_bridge_priority": 32768,
                                  "forward_delay": 0,
                                  "designated_bridge_address": "d8b1.9009.bf80",
                                  "designated_path_cost": 0,
                                  "designated_root_priority": 32768,
                                  "port_identifier": "128.2390.",
                                  "cost": 6660,
                                  "counters": {
                                       "bpdu_sent": 138231,
                                       "bpdu_received": 167393
                                  },
                                  "designated_root_address": "d8b1.9009.bf80",
                                  "boundary": "PVST",
                                  "port_num": 2390,
                                  "port_priority": 128,
                                  "name": "Port-channel14",
                                  "hold": 0,
                                  "message_age": 0,
                                  "link_type": "point-to-point",
                                  "loop_guard": True
                             }
                        },
                        "topology_change_times": 70,
                        "topology_from_port": "Port-channel24",
                        "bridge_priority": 32768,
                        "topology_detected_flag": False,
                        "max_age": 40
                   }
              },
              "forwarding_delay": 30,
              "hello_time": 10,
              "max_age": 40,
              "hold_count": 20
        }
    }

    ShowSpanningTreeMstDetail = {
      "mst_instances": {
            0: {
               "bridge_priority": 32768,
               "interfaces": {
                    "GigabitEthernet1/0/23": {
                         "designated_regional_root_cost": 0,
                         "port_priority": 128,
                         "designated_root_priority": 32768,
                         "designated_bridge_port_id": "128.23",
                         "designated_bridge_priority": 32768,
                         "forward_delay": 0,
                         "port_id": "128.23",
                         "name": "GigabitEthernet1/0/23",
                         "designated_regional_root_priority": 32768,
                         "forward_transitions": 1,
                         "counters": {
                              "bpdu_sent": 493,
                              "bpdu_received": 0
                         },
                         "designated_regional_root_address": "3820.565b.8600",
                         "status": "designated forwarding",
                         "designated_root_cost": 0,
                         "designated_bridge_address": "3820.565b.8600",
                         "designated_root_address": "3820.565b.8600",
                         "cost": 20000,
                         "message_expires": 0
                    }
               },
               "operational": {
                    "max_age": 35,
                    "tx_hold_count": 20,
                    "hello_time": 10,
                    "forward_delay": 30
               },
               "sysid": 0,
               "root": "CIST",
               "bridge_address": "3820.565b.8600",
               "configured": {
                    "max_age": 35,
                    "forward_delay": 30,
                    "hello_time": 10,
                    "max_hops": 10
               },
               "mst_id": 0,
               "vlan": "1-99,201-4094"
            },
            10: {
               "bridge_priority": 61450,
               "interfaces": {
                    "GigabitEthernet1/0/23": {
                         "port_priority": 128,
                         "designated_root_priority": 61450,
                         "designated_bridge_port_id": "128.23",
                         "designated_bridge_priority": 61450,
                         "forward_delay": 0,
                         "port_id": "128.23",
                         "name": "GigabitEthernet1/0/23",
                         "forward_transitions": 1,
                         "counters": {
                              "bpdu_sent": 493,
                              "bpdu_received": 0
                         },
                         "message_expires": 0,
                         "status": "designated forwarding",
                         "designated_root_cost": 0,
                         "designated_bridge_address": "3820.565b.8600",
                         "designated_root_address": "3820.565b.8600",
                         "cost": 20000
                    }
               },
               "sysid": 10,
               "root": "MST10",
               "bridge_address": "3820.565b.8600",
               "mst_id": 10,
               "vlan": "100-200"
            }
        }
    }

    ShowSpanningTreeSummary = {
        "bpdu_filter": False,
        "extended_system_id": True,
        "etherchannel_misconfig_guard": False,
        "total_statistics": {
          "forwardings": 10,
          "listenings": 0,
          "root_bridges": 2,
          "stp_actives": 16,
          "learnings": 0,
          "blockings": 6
        },
        "root_bridge_for": "MST0, MST100",
        "bpdu_guard": False,
        "mode": {
          "mst": {
               "MST100": {
                    "blocking": 3,
                    "forwarding": 1,
                    "listening": 0,
                    "stp_active": 4,
                    "learning": 0
               },
               "MST0": {
                    "blocking": 3,
                    "forwarding": 9,
                    "listening": 0,
                    "stp_active": 12,
                    "learning": 0
               }
          }
        },
        "uplink_fast": False,
        "backbone_fast": False,
        "portfast_default": False,
        "loop_guard": False

    }

    ShowErrdisableRecovery = {
        "bpduguard_timeout_recovery": 333,
        "timer_status": {
          "gbic-invalid": False,
          "oam-remote-failure": False,
          "arp-inspection": False,
          "dtp-flap": False,
          "port-mode-failure": False,
          "loopback": False,
          "mac-limit": False,
          "psp": False,
          "channel-misconfig (STP)": False,
          "l2ptguard": False,
          "Recovery command: \"clear": False,
          "link-monitor-failure": False,
          "vmps": False,
          "bpduguard": False,
          "sfp-config-mismatch": False,
          "dual-active-recovery": False,
          "pagp-flap": False,
          "security-violation": False,
          "storm-control": False,
          "psecure-violation": False,
          "udld": False,
          "inline-power": False,
          "link-flap": False,
          "evc-lite input mapping fa": False,
          "pppoe-ia-rate-limit": False,
          "dhcp-rate-limit": False
        }
    }

    ShowSpanningTree = {
        "mstp": {
          "mst_instances": {
               0: {
                    "bridge": {
                         "hello_time": 7,
                         "priority": 32768,
                         "forward_delay": 15,
                         "address": "ecbd.1d09.5680",
                         "max_age": 12,
                         "configured_bridge_priority": 32768,
                         "sys_id_ext": 0,
                    },
                    "interfaces": {
                         "GigabitEthernet1/0/5": {
                              "port_state": "forwarding",
                              "bound": "RSTP",
                              "port_num": 5,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 20000,
                              "role": "root"
                         },
                         "Port-channel14": {
                              "port_state": "broken",
                              "bound": "PVST",
                              "port_num": 2390,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 6660,
                              "role": "designated"
                         },
                         "Port-channel24": {
                              "port_state": "forwarding",
                              "bound": "PVST",
                              "port_num": 2400,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 6660,
                              "role": "designated"
                         }
                    },
                    "root": {
                         "hello_time": 10,
                         "priority": 32768,
                         "forward_delay": 30,
                         "max_age": 35,
                         "cost": 20000,
                         "address": "3820.565b.8600",
                         "interface": "GigabitEthernet1/0/5",
                         "port": 5
                    }
               },
               10: {
                    "bridge": {
                         "hello_time": 7,
                         "priority": 61450,
                         "forward_delay": 15,
                         "address": "ecbd.1d09.5680",
                         "max_age": 12,
                         "configured_bridge_priority": 61440,
                         "sys_id_ext": 10,
                    },
                    "interfaces": {
                         "GigabitEthernet1/0/5": {
                              "port_state": "forwarding",
                              "bound": "RSTP",
                              "port_num": 5,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 20000,
                              "role": "master "
                         },
                         "Port-channel14": {
                              "port_state": "broken",
                              "bound": "PVST",
                              "port_num": 2390,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 6660,
                              "role": "designated"
                         }
                    },
                    "root": {
                         "hello_time": 10,
                         "priority": 61450,
                         "forward_delay": 30,
                         "address": "ecbd.1d09.5680",
                         "max_age": 35
                    }
               }
            }
        }
    }

    ShowSpanningTreeMstConfiguration = {
        "mstp": {
            "revision": 111,
            "name": "mst",
            "instances_configured": 2,
            "mst_instances": {
               10: {
                    "vlan_mapped": "100-200"
               },
               0: {
                    "vlan_mapped": "1-99,201-4094"
               }
            }
        }
    }

    Stp_info = {
        "global": {
          "etherchannel_misconfig_guard": False,
          "bpdu_filter": False,
          "bpdu_guard": False,
          "bpduguard_timeout_recovery": 333,
          "loop_guard": False
        },
        "mstp": {
            "default": {
                 "max_age": 40,
                 "domain": "default",
                 "revision": 111,
                 "forwarding_delay": 30,
                 "name": "mst",
                 "hello_time": 10,
                 "max_hop": 10,
                 "mst_instances": {
                      0: {
                           "bridge_address": "d8b1.9009.bf80",
                           "time_since_topology_change": "03:09:48",
                           "designated_root_address": "3820.565b.8600",
                           "designated_root_priority": 32768,
                           "configured_bridge_priority": 32768,
                           "sys_id_ext": 0,
                           "bridge_priority": 32768,
                           "root_port": 5,
                           "topology_changes": 3,
                           "hold_time": 1,
                           "vlan": "1-99,201-4094",
                           "interfaces": {
                                "GigabitEthernet1/0/5": {
                                     "designated_port_num": 5,
                                     "role": "root",
                                     "port_state": "forwarding",
                                     "designated_port_priority": 128
                                },
                                "Port-channel14": {
                                     "designated_root_priority": 32768,
                                     "port_num": 2390,
                                     "counters": {
                                          "bpdu_received": 167393,
                                          "bpdu_sent": 138231
                                     },
                                     "designated_port_num": 2390,
                                     "name": "Port-channel14",
                                     "cost": 6660,
                                     "designated_bridge_address": "d8b1.9009.bf80",
                                     "role": "designated",
                                     "port_priority": 128,
                                     "port_state": "broken",
                                     "forward_transitions": 0,
                                     "designated_bridge_priority": 32768,
                                     "designated_root_address": "d8b1.9009.bf80",
                                     "designated_cost": 0,
                                     "designated_port_priority": 128
                                },
                                "Port-channel24": {
                                     "designated_root_priority": 32768,
                                     "port_num": 2400,
                                     "counters": {
                                          "bpdu_received": 2191582,
                                          "bpdu_sent": 1099019
                                     },
                                     "designated_port_num": 2400,
                                     "name": "Port-channel24",
                                     "cost": 6660,
                                     "designated_bridge_address": "d8b1.9009.bf80",
                                     "role": "designated",
                                     "port_priority": 128,
                                     "port_state": "forwarding",
                                     "forward_transitions": 1,
                                     "designated_bridge_priority": 32768,
                                     "designated_root_address": "d8b1.9009.bf80",
                                     "designated_cost": 0,
                                     "designated_port_priority": 128
                                }
                           },
                           "mst_id": 0,
                           "root_cost": 20000
                      },
                      10: {
                           "time_since_topology_change": "03:09:48",
                           "designated_root_priority": 61450,
                           "bridge_priority": 32768,
                           "configured_bridge_priority": 61440,
                           "sys_id_ext": 10,
                           "bridge_address": "d8b1.9009.bf80",
                           "topology_changes": 3,
                           "hold_time": 1,
                           "vlan": "100-200",
                           "interfaces": {
                                "GigabitEthernet1/0/5": {
                                     "designated_root_priority": 32768,
                                     "port_num": 2400,
                                     "counters": {
                                          "bpdu_received": 2191582,
                                          "bpdu_sent": 1099019
                                     },
                                     "designated_port_num": 5,
                                     "name": "Port-channel24",
                                     "cost": 6660,
                                     "designated_bridge_address": "d8b1.9009.bf80",
                                     "role": "master ",
                                     "port_priority": 128,
                                     "port_state": "forwarding",
                                     "forward_transitions": 1,
                                     "designated_bridge_priority": 32768,
                                     "designated_root_address": "d8b1.9009.bf80",
                                     "designated_cost": 0,
                                     "designated_port_priority": 128
                                },
                                "Port-channel14": {
                                     "designated_root_priority": 32768,
                                     "port_num": 2390,
                                     "counters": {
                                          "bpdu_received": 167393,
                                          "bpdu_sent": 138231
                                     },
                                     "designated_port_num": 2390,
                                     "name": "Port-channel14",
                                     "cost": 6660,
                                     "designated_bridge_address": "d8b1.9009.bf80",
                                     "role": "designated",
                                     "port_priority": 128,
                                     "port_state": "broken",
                                     "forward_transitions": 0,
                                     "designated_bridge_priority": 32768,
                                     "designated_root_address": "d8b1.9009.bf80",
                                     "designated_cost": 0,
                                     "designated_port_priority": 128
                                }
                           },
                           "mst_id": 0,
                           "designated_root_address": "ecbd.1d09.5680"
                      }
                 },
                 "hold_count": 20
            }
        }
    }


class StpRpstOutput(object):

    ShowSpanningTreeDetail = {
        "rapid_pvst": {
              "forwarding_delay": 15,
              "vlans": {
                   201: {
                        "forwarding_delay": 15,
                        "hello_timer": 0,
                        "bridge_sysid": 201,
                        "hold_time": 1,
                        "time_since_topology_change": "00:00:14",
                        "notification_timer": 0,
                        "topology_change_flag": True,
                        "topology_changes": 1,
                        "topology_change_times": 35,
                        "aging_timer": 300,
                        "topology_from_port": "Port-channel14",
                        "topology_change_timer": 21,
                        "bridge_address": "ecbd.1d09.5680",
                        "notification_times": 2,
                        "bridge_priority": 28672,
                        "topology_detected_flag": False,
                        "hello_time": 2,
                        "interfaces": {
                             "GigabitEthernet1/0/5": {
                                  "designated_bridge_address": "ecbd.1d09.5680",
                                  "number_of_forward_transitions": 1,
                                  "port_identifier": "128.5.",
                                  "counters": {
                                       "bpdu_received": 4,
                                       "bpdu_sent": 20
                                  },
                                  "cost": 4,
                                  "designated_port_id": "128.5",
                                  "designated_root_priority": 24777,
                                  "designated_root_address": "58bf.eab6.2f00",
                                  "port_num": 5,
                                  "status": "designated forwarding",
                                  "port_priority": 128,
                                  "forward_delay": 0,
                                  "hold": 0,
                                  "message_age": 0,
                                  "peer": "STP",
                                  "link_type": "point-to-point",
                                  "designated_bridge_priority": 28873,
                                  "designated_path_cost": 3,
                                  "name": "GigabitEthernet1/0/5"
                             }
                        },
                        "max_age": 20,
                        "hold_count": 6,
                        "vlan_id": 201
                   },
                   100: {
                        "forwarding_delay": 15,
                        "hello_timer": 0,
                        "bridge_sysid": 100,
                        "hold_time": 1,
                        "time_since_topology_change": "00:00:34",
                        "notification_timer": 0,
                        "hello_time": 2,
                        "hold_count": 6,
                        "topology_change_flag": True,
                        "topology_changes": 1,
                        "notification_times": 2,
                        "aging_timer": 300,
                        "topology_from_port": "Port-channel12",
                        "topology_change_timer": 0,
                        "bridge_address": "3820.565b.1b80",
                        "topology_change_times": 35,
                        "bridge_priority": 24576,
                        "topology_detected_flag": False,
                        "root_of_spanning_tree": True,
                        "interfaces": {
                             "Port-channel12": {
                                  "designated_bridge_address": "3820.565b.1b80",
                                  "number_of_forward_transitions": 1,
                                  "port_identifier": "128.2388.",
                                  "counters": {
                                       "bpdu_received": 0,
                                       "bpdu_sent": 34
                                  },
                                  "cost": 3,
                                  "designated_port_id": "128.2388",
                                  "designated_root_priority": 24676,
                                  "designated_root_address": "3820.565b.1b80",
                                  "port_num": 2388,
                                  "status": "designated forwarding",
                                  "port_priority": 128,
                                  "forward_delay": 0,
                                  "hold": 0,
                                  "message_age": 0,
                                  "link_type": "point-to-point",
                                  "designated_bridge_priority": 24676,
                                  "designated_path_cost": 0,
                                  "name": "Port-channel12"
                             }
                        },
                        "max_age": 20,
                        "vlan_id": 100
                   }
              },
              "max_age": 20,
              "hold_count": 6,
              "hello_time": 2
         }
    }

    ShowSpanningTreeSummary = {
     "etherchannel_misconfig_guard": True,
     "loop_guard": False,
     "bpdu_filter": False,
     "backbone_fast": False,
     "uplink_fast": False,
     "root_bridge_for": "none",
     "mode": {
          "rapid_pvst": {
               "VLAN0200": {
                    "forwarding": 2,
                    "learning": 0,
                    "listening": 0,
                    "stp_active": 2,
                    "blocking": 0
               },
               "VLAN0201": {
                    "forwarding": 2,
                    "learning": 0,
                    "listening": 0,
                    "stp_active": 2,
                    "blocking": 0
               },
          }
     },
     "portfast_default": False,
     "extended_system_id": True,
     "total_statistics": {
          "stp_actives": 4,
          "blockings": 0,
          "root_bridges": 2,
          "forwardings": 4,
          "learnings": 0,
          "listenings": 0
     },
     "bpdu_guard": False
    }

    ShowErrdisableRecovery = {
        "bpduguard_timeout_recovery": 333,
        "timer_status": {
          "gbic-invalid": False,
          "oam-remote-failure": False,
          "arp-inspection": False,
          "dtp-flap": False,
          "port-mode-failure": False,
          "loopback": False,
          "mac-limit": False,
          "psp": False,
          "channel-misconfig (STP)": False,
          "l2ptguard": False,
          "Recovery command: \"clear": False,
          "link-monitor-failure": False,
          "vmps": False,
          "bpduguard": False,
          "sfp-config-mismatch": False,
          "dual-active-recovery": False,
          "pagp-flap": False,
          "security-violation": False,
          "storm-control": False,
          "psecure-violation": False,
          "udld": False,
          "inline-power": False,
          "link-flap": False,
          "evc-lite input mapping fa": False,
          "pppoe-ia-rate-limit": False,
          "dhcp-rate-limit": False
        }
    }

    ShowSpanningTree = {
        "rapid_pvst": {
          "vlans": {
               200: {
                    "bridge": {
                         "hello_time": 2,
                         "priority": 28872,
                         "forward_delay": 15,
                         "max_age": 20,
                         "aging_time": 300,
                         "address": "ecbd.1d09.5680",
                         "configured_bridge_priority": 28672,
                         "sys_id_ext": 200,
                    },
                    "interfaces": {
                         "GigabitEthernet1/0/5": {
                              "peer": "STP",
                              "port_state": "forwarding",
                              "port_num": 5,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 4,
                              "role": "designated"
                         },
                         "Port-channel14": {
                              "port_state": "forwarding",
                              "port_num": 2390,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 3,
                              "role": "root"
                         }
                    },
                    "root": {
                         "hello_time": 2,
                         "priority": 24776,
                         "forward_delay": 15,
                         "max_age": 20,
                         "cost": 3,
                         "address": "58bf.eab6.2f00",
                         "interface": "Port-channel14",
                         "port": 2390
                    }
               },
               201: {
                    "bridge": {
                         "hello_time": 2,
                         "priority": 28873,
                         "forward_delay": 15,
                         "max_age": 20,
                         "aging_time": 300,
                         "address": "ecbd.1d09.5680",
                         "configured_bridge_priority": 28672,
                         "sys_id_ext": 201,
                    },
                    "interfaces": {
                         "GigabitEthernet1/0/5": {
                              "peer": "STP",
                              "port_state": "forwarding",
                              "port_num": 5,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 4,
                              "role": "designated"
                         },
                         "Port-channel14": {
                              "port_state": "forwarding",
                              "port_num": 2390,
                              "port_priority": 128,
                              "type": "P2p",
                              "cost": 3,
                              "role": "root"
                         }
                    },
                    "root": {
                         "hello_time": 2,
                         "priority": 24777,
                         "forward_delay": 15,
                         "max_age": 20,
                         "cost": 3,
                         "address": "58bf.eab6.2f00",
                         "interface": "Port-channel14",
                         "port": 2390
                    }
               }
            }
        }
    }

    Stp_info = {
        "global": {
          "bpdu_guard": False,
          "bpduguard_timeout_recovery": 333,
          "etherchannel_misconfig_guard": True,
          "bpdu_filter": False,
          "loop_guard": False
        },
        "rapid_pvst": {
            "default": {
                 "hold_count": 6,
                 "hello_time": 2,
                 "max_age": 20,
                 "forwarding_delay": 15,
                 "pvst_id": "default",
                 "vlans": {
                      200: {
                           "designated_root_priority": 24776,
                           "root_port": 2390,
                           "root_cost": 3,
                           "configured_bridge_priority": 28672,
                           "sys_id_ext": 200,
                           "interfaces": {
                                "Port-channel14": {
                                     "designated_port_priority": 128,
                                     "role": "root",
                                     "designated_port_num": 2390,
                                     "port_state": "forwarding"
                                },
                                "GigabitEthernet1/0/5": {
                                     "designated_port_priority": 128,
                                     "role": "designated",
                                     "designated_port_num": 5,
                                     "port_state": "forwarding"
                                }
                           },
                           "designated_root_address": "58bf.eab6.2f00"
                      },
                      201: {
                           "time_since_topology_change": "00:00:14",
                           "bridge_priority": 28672,
                           "configured_bridge_priority": 28672,
                           "sys_id_ext": 201,
                           "hold_count": 6,
                           "vlan_id": 201,
                           "interfaces": {
                                "Port-channel14": {
                                     "designated_port_priority": 128,
                                     "role": "root",
                                     "designated_port_num": 2390,
                                     "port_state": "forwarding"
                                },
                                "GigabitEthernet1/0/5": {
                                     "port_num": 5,
                                     "counters": {
                                          "bpdu_sent": 20,
                                          "bpdu_received": 4
                                     },
                                     "cost": 4,
                                     "designated_bridge_address": "ecbd.1d09.5680",
                                     "forward_transitions": 1,
                                     "name": "GigabitEthernet1/0/5",
                                     "designated_port_num": 5,
                                     "role": "designated",
                                     "designated_bridge_priority": 28873,
                                     "designated_root_address": "58bf.eab6.2f00",
                                     "port_priority": 128,
                                     "designated_cost": 3,
                                     "designated_root_priority": 24777,
                                     "designated_port_priority": 128,
                                     "port_state": "forwarding"
                                }
                           },
                           "hello_time": 2,
                           "max_age": 20,
                           "forwarding_delay": 15,
                           "hold_time": 1,
                           "topology_changes": 1,
                           "designated_root_priority": 24777,
                           "root_port": 2390,
                           "root_cost": 3,
                           "bridge_address": "ecbd.1d09.5680",
                           "designated_root_address": "58bf.eab6.2f00"
                      },
                      100: {
                           "time_since_topology_change": "00:00:34",
                           "bridge_priority": 24576,
                           "hello_time": 2,
                           "max_age": 20,
                           "vlan_id": 100,
                           "hold_count": 6,
                           "forwarding_delay": 15,
                           "interfaces": {
                                "Port-channel12": {
                                     "designated_bridge_priority": 24676,
                                     "designated_root_address": "3820.565b.1b80",
                                     "port_num": 2388,
                                     "port_priority": 128,
                                     "counters": {
                                          "bpdu_sent": 34,
                                          "bpdu_received": 0
                                     },
                                     "designated_cost": 0,
                                     "cost": 3,
                                     "designated_root_priority": 24676,
                                     "forward_transitions": 1,
                                     "name": "Port-channel12",
                                     "designated_bridge_address": "3820.565b.1b80"
                                }
                           },
                           "hold_time": 1,
                           "topology_changes": 1,
                           "bridge_address": "3820.565b.1b80"
                      }
                 }
            }
        }
    }