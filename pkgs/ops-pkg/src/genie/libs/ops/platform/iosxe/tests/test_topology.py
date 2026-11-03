import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from genie.libs.ops.platform.iosxe.cat9k.c9500.rev1.platform import (
    Platform as C9500Platform,
)
from genie.libs.ops.platform.iosxe.topology import populate_topology


class TestIosXeTopology(unittest.TestCase):

    def test_svl_and_member_inventory(self):
        platform = SimpleNamespace(device=Mock(), members={})
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
            "show switch": {"switch": {"stack": {
                1: {"state": "Ready"}, 2: {"state": "Ready"},
            }}},
        }.get(command, {})
        inventory = {
            "1": {"inventory": {
                "Switch 1 Chassis": {
                    "pid": "C9610R", "vid": "V01", "sn": "ONE",
                },
                "Switch 1 Slot 2 Linecard": {
                    "pid": "C9600-LC-48YL", "vid": "V02", "sn": "LC1",
                },
            }},
            "2": {"inventory": {
                "Switch 2 Chassis": {
                    "pid": "C9610R", "vid": "V01", "sn": "TWO",
                },
            }},
        }

        populate_topology(platform, inventory)

        self.assertEqual(platform.chassis_type, "stackwise_virtual")
        self.assertTrue(platform.chassis_type_confident)
        self.assertEqual(platform.chassis_member_count, 2)
        self.assertTrue(platform.is_modular)
        self.assertEqual(platform.members["2"]["serial"], "TWO")
        self.assertEqual(
            platform.slot["lc"]["1/2"],
            {
                "name": "Switch 1 Slot 2 Linecard",
                "pid": "C9600-LC-48YL",
                "sn": "LC1",
                "hw_revision": "V02",
                "full_slot": "1/2",
                "subslot": {},
            },
        )

    def test_member_inventory_publishes_modular_descendants(self):
        platform = SimpleNamespace(
            device=Mock(),
            members={
                "1": {"pid": "C9610R"},
                "2": {"pid": "C9610R"},
            },
        )
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
        }.get(command, {})
        inventory = {
            "1": {"inventory": {
                "Switch 1 Slot 5 Linecard": {
                    "pid": "C9600-LC-48YL", "vid": "V02", "sn": "LC1",
                },
                "Switch 1 Slot 5 Linecard 0": {
                    "pid": "C9600-LC-48YL", "vid": "V01", "sn": "MPA1",
                },
                "Switch 1 Slot 5 Linecard 0 Transceiver 1": {
                    "pid": "SFP-10G-SR", "vid": "V03", "sn": "OPTIC1",
                },
                "Switch 1 Slot 4 Supervisor": {
                    "pid": "C9600-SUP-1", "vid": "V01", "sn": "SUP1",
                },
            }},
        }

        populate_topology(platform, inventory)

        linecard = platform.slot["lc"]["1/5"]
        self.assertEqual(linecard["full_slot"], "1/5")
        self.assertEqual(linecard["subslot"]["0"]["sn"], "MPA1")
        self.assertEqual(
            linecard["subslot"]["0 transceiver 1"]["sn"], "OPTIC1"
        )
        self.assertEqual(platform.slot["rp"]["1/4"]["sn"], "SUP1")

    def test_fixed_svl_does_not_publish_synthetic_member_cards(self):
        platform = SimpleNamespace(
            device=Mock(),
            members={
                "1": {"pid": "C9500-32C"},
                "2": {"pid": "C9500-32C"},
            },
        )
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
        }.get(command, {})
        inventory = {
            "1": {"inventory": {
                "Switch 1 Slot 1 Supervisor": {
                    "pid": "C9500-32C", "vid": "V01", "sn": "ONE",
                },
            }},
        }

        populate_topology(platform, inventory)

        self.assertFalse(platform.is_modular)
        self.assertFalse(hasattr(platform, "slot"))

    def test_inventory_enriches_existing_role_only_members(self):
        platform = SimpleNamespace(
            device=Mock(),
            members={"1": {"role": "active"}, "2": {"role": "standby"}},
        )
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
        }.get(command, {})
        inventory = {
            "1": {"inventory": {
                "Switch 1 Chassis": {
                    "pid": "C9500-32C", "vid": "V01", "sn": "ONE",
                },
            }},
            "2": {"inventory": {
                "Switch 2 Chassis": {
                    "pid": "C9500-32C", "vid": "V02", "sn": "TWO",
                },
            }},
        }

        populate_topology(platform, inventory)

        self.assertEqual(platform.members["1"], {
            "role": "active", "serial": "ONE", "pid": "C9500-32C",
            "hw_revision": "V01",
        })
        self.assertEqual(platform.members["2"], {
            "role": "standby", "serial": "TWO", "pid": "C9500-32C",
            "hw_revision": "V02",
        })
        self.assertFalse(platform.is_modular)
        self.assertTrue(platform.modularity_confident)

    def test_fixed_member_pids_override_generic_learned_linecard_tree(self):
        platform = SimpleNamespace(
            device=Mock(),
            members={
                "1": {"pid": "C9500X-28C8D"},
                "2": {"pid": "C9500X-28C8D"},
            },
            slot={"lc": {"1": {"name": "Switch 1 Slot 1 Supervisor"}}},
        )
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
        }.get(command, {})

        populate_topology(platform)

        self.assertFalse(platform.is_modular)
        self.assertTrue(platform.modularity_confident)

    def test_fixed_platform_pid_overrides_generic_learned_linecard_tree(self):
        platform = SimpleNamespace(
            device=Mock(),
            chassis="C9500-48Y4C",
            members={},
            slot={"lc": {"1": {"name": "C9500-48Y4C"}}},
        )
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
        }.get(command, {})

        populate_topology(platform)

        self.assertFalse(platform.is_modular)
        self.assertTrue(platform.modularity_confident)

    def test_member_inventory_is_cleared_when_current_input_is_missing(self):
        platform = SimpleNamespace(device=Mock(), members={})
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
        }.get(command, {})
        inventory = {
            "1": {"inventory": {
                "Switch 1 Chassis": {
                    "pid": "C9500-32C", "vid": "V01", "sn": "ONE",
                },
            }},
        }

        populate_topology(platform, inventory)
        self.assertEqual(platform.member_inventory, inventory)

        populate_topology(platform)

        self.assertEqual(platform.member_inventory, {})
        self.assertEqual(platform.members, {})

    def test_inventory_overlay_is_removed_without_erasing_parser_owned_data(self):
        platform = SimpleNamespace(
            device=Mock(),
            members={"1": {"role": "active"}},
            slot={"lc": {"0/1": {"sn": "PARSER"}}},
        )
        platform.device.parse.return_value = {}
        inventory = {"1": {"inventory": {
            "Switch 1 Chassis": {
                "pid": "C9610R", "vid": "V01", "sn": "ONE",
            },
            "Switch 1 Slot 5 Linecard": {
                "pid": "C9600-LC-48YL", "vid": "V02", "sn": "LC1",
            },
            "Switch 1 Slot 5 Linecard 0": {
                "pid": "C9600-MPA", "vid": "V01", "sn": "MPA1",
            },
        }}}

        populate_topology(platform, inventory)
        self.assertIn("1/5", platform.slot["lc"])
        self.assertEqual(platform.members["1"]["serial"], "ONE")

        populate_topology(platform)

        self.assertEqual(platform.member_inventory, {})
        self.assertEqual(platform.members, {"1": {"role": "active"}})
        self.assertEqual(platform.slot, {"lc": {"0/1": {"sn": "PARSER"}}})
        self.assertTrue(platform.is_modular)

    def test_inventory_overlay_replaces_only_its_own_fields(self):
        platform = SimpleNamespace(device=Mock(), members={"1": {"role": "active"}})
        platform.device.parse.return_value = {}
        first = {"1": {"inventory": {
            "Switch 1 Chassis": {"pid": "C9500-32C", "sn": "ONE"},
        }}}
        second = {"1": {"inventory": {
            "Switch 1 Chassis": {"pid": "C9500-32C", "sn": "TWO"},
        }}}

        populate_topology(platform, first)
        platform.members["1"]["serial"] = "PARSER"
        populate_topology(platform, second)

        self.assertEqual(platform.members["1"]["serial"], "PARSER")
        self.assertEqual(platform.members["1"]["role"], "active")

    def test_inventory_enrichment_leaves_existing_card_intact_on_new_learn(self):
        platform = SimpleNamespace(
            device=Mock(), members={"1": {"pid": "C9610R"}},
            slot={"lc": {"1/5": {"name": "PARSER"}}},
        )
        platform.device.parse.return_value = {}
        inventory = {"1": {"inventory": {
            "Switch 1 Slot 5 Linecard": {
                "pid": "C9600-LC", "sn": "LC1",
            },
            "Switch 1 Slot 5 Linecard 0": {
                "pid": "C9600-MPA", "sn": "MPA1",
            },
        }}}

        populate_topology(platform, inventory)
        self.assertEqual(platform.slot["lc"]["1/5"]["sn"], "LC1")
        self.assertIn("0", platform.slot["lc"]["1/5"]["subslot"])
        populate_topology(platform)

        self.assertEqual(platform.slot["lc"]["1/5"], {"name": "PARSER"})

    def test_inventory_only_modularity_does_not_survive_new_learn(self):
        platform = SimpleNamespace(device=Mock(), members={})
        platform.device.parse.return_value = {}
        inventory = {"1": {"inventory": {
            "Switch 1 Chassis": {"pid": "C9610R", "sn": "ONE"},
            "Switch 1 Slot 5 Linecard": {"pid": "C9600-LC", "sn": "LC1"},
        }}}

        populate_topology(platform, inventory)
        self.assertTrue(platform.is_modular)
        self.assertIn("1/5", platform.slot["lc"])
        populate_topology(platform)

        self.assertIsNone(platform.is_modular)
        self.assertFalse(platform.modularity_confident)
        self.assertFalse(hasattr(platform, "slot"))
        self.assertEqual(platform.members, {})

    def test_svl_requires_current_member_state(self):
        for switch_output in ({}, {"switch": {}}, {"switch": {"stack": {}}}):
            with self.subTest(switch_output=switch_output):
                platform = SimpleNamespace(device=Mock(), members={})
                platform.device.parse.side_effect = lambda command: {
                    "show stackwise-virtual": {"enabled": True},
                    "show switch": switch_output,
                }.get(command, {})

                populate_topology(platform)

                self.assertIsNone(platform.chassis_type)
                self.assertFalse(platform.chassis_type_confident)
                self.assertIsNone(platform.chassis_member_count)
                self.assertIn("no member state", platform.topology_incomplete_reason)

    @patch(
        "genie.libs.ops.platform.iosxe.cat9k.c9500.rev1.platform."
        "populate_topology"
    )
    def test_c9500_specific_rev1_publishes_normalized_topology(self, normalizer):
        platform = SimpleNamespace(
            add_leaf=Mock(),
            make=Mock(),
            device=Mock(),
            _member_inventory={"1": {"inventory": {}}},
        )

        C9500Platform.learn(platform)

        normalizer.assert_called_once_with(
            platform, {"1": {"inventory": {}}}
        )
        self.assertFalse(hasattr(platform, "_member_inventory"))

    def test_degraded_stack_is_inconclusive(self):
        platform = SimpleNamespace(device=Mock(), members={})
        platform.device.parse.side_effect = lambda command: {
            "show switch": {"switch": {"stack": {
                1: {"state": "Ready"},
                2: {"state": "Provisioned"},
            }}},
            "show redundancy states": {
                "mode": "Simplex", "peer_state": "Disabled",
            },
        }.get(command, {})

        populate_topology(platform)

        self.assertIsNone(platform.chassis_type)
        self.assertFalse(platform.chassis_type_confident)
        self.assertIn("member 2=Provisioned", platform.topology_incomplete_reason)

        platform.device.parse.side_effect = lambda command: {
            "show switch": {"switch": {"stack": {
                1: {"state": "Ready"},
                2: {"state": "Ready"},
            }}},
        }.get(command, {})

        populate_topology(platform)

        self.assertEqual(platform.chassis_type, "stack")
        self.assertTrue(platform.chassis_type_confident)
        self.assertEqual(platform.chassis_member_count, 2)
        self.assertIsNone(platform.topology_incomplete_reason)

    def test_degraded_svl_is_inconclusive(self):
        platform = SimpleNamespace(device=Mock(), members={})
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
            "show switch": {"switch": {"stack": {
                1: {"state": "Ready"},
                2: {"state": "Provisioned"},
            }}},
        }.get(command, {})

        populate_topology(platform)

        self.assertIsNone(platform.chassis_type)
        self.assertFalse(platform.chassis_type_confident)
        self.assertIsNone(platform.chassis_member_count)
        self.assertIn("member 2=Provisioned", platform.topology_incomplete_reason)

    def test_non_ready_member_states_are_inconclusive(self):
        for stackwise_enabled in (False, True):
            for state in ("V-Mismatch", "Initializing", "Unprovisioned", None):
                with self.subTest(stackwise=stackwise_enabled, state=state):
                    platform = SimpleNamespace(device=Mock(), members={})
                    platform.device.parse.side_effect = lambda command: {
                        "show stackwise-virtual": {"enabled": stackwise_enabled},
                        "show switch": {"switch": {"stack": {
                            1: {"state": "Ready"},
                            2: {"state": state},
                        }}},
                        "show redundancy states": {"mode": "Simplex"},
                    }.get(command, {})

                    populate_topology(platform)

                    self.assertIsNone(platform.chassis_type)
                    self.assertFalse(platform.chassis_type_confident)
                    self.assertIsNone(platform.chassis_member_count)
                    self.assertIn(
                        "member 2={}".format(state or ""),
                        platform.topology_incomplete_reason,
                    )

    def test_healthy_svl_remains_confident(self):
        platform = SimpleNamespace(device=Mock(), members={})
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
            "show switch": {"switch": {"stack": {
                1: {"state": "Ready"},
                2: {"state": "Ready"},
            }}},
        }.get(command, {})

        populate_topology(platform)

        self.assertEqual(platform.chassis_type, "stackwise_virtual")
        self.assertTrue(platform.chassis_type_confident)
        self.assertEqual(platform.chassis_member_count, 2)
        self.assertIsNone(platform.topology_incomplete_reason)

    def test_partial_svl_members_retain_two_chassis_count(self):
        platform = SimpleNamespace(
            device=Mock(),
            members={"1": {"role": "active", "serial": "ONE"}},
        )
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
            "show switch": {"switch": {"stack": {
                1: {"state": "Ready"},
            }}},
        }.get(command, {})

        populate_topology(platform)

        self.assertEqual(platform.chassis_type, "stackwise_virtual")
        self.assertTrue(platform.chassis_type_confident)
        self.assertEqual(platform.chassis_member_count, 2)
        self.assertIsNone(platform.topology_incomplete_reason)

    def test_svl_prefers_complete_parsed_stack_count(self):
        platform = SimpleNamespace(
            device=Mock(),
            members={"1": {"role": "active", "serial": "ONE"}},
        )
        platform.device.parse.side_effect = lambda command: {
            "show stackwise-virtual": {"enabled": True},
            "show switch": {"switch": {"stack": {
                1: {"state": "Ready"},
                2: {"state": "Ready"},
            }}},
        }.get(command, {})

        populate_topology(platform)

        self.assertEqual(platform.chassis_type, "stackwise_virtual")
        self.assertTrue(platform.chassis_type_confident)
        self.assertEqual(platform.chassis_member_count, 2)
        self.assertIsNone(platform.topology_incomplete_reason)

    def test_dual_rp(self):
        platform = SimpleNamespace(device=Mock(), members={})
        platform.device.parse.side_effect = lambda command: {
            "show redundancy states": {
                "mode": "Duplex",
                "peer_state": "STANDBY HOT",
                "communications": "Up",
            },
        }.get(command, {})

        populate_topology(platform)

        self.assertEqual(platform.chassis_type, "dual_rp")
        self.assertTrue(platform.chassis_type_confident)
        self.assertEqual(platform.chassis_member_count, 2)


if __name__ == '__main__':
    unittest.main()
