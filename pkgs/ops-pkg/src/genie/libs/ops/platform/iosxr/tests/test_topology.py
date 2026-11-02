import unittest
from types import SimpleNamespace

from genie.libs.ops.platform.iosxr.platform import Platform


class TestIosXrTopology(unittest.TestCase):

    def test_known_fixed_single_rp_is_confident_standalone(self):
        learned = SimpleNamespace(
            slot={"rp": {"0/RP0": {"redundancy_state": "Active"}}},
            chassis="NCS-57C1-48Q6-SYS",
            _FIXED_SINGLE_RP_SYSTEM_TYPES=Platform._FIXED_SINGLE_RP_SYSTEM_TYPES,
        )

        Platform._populate_topology(learned)

        self.assertIsNone(learned.chassis_type)
        self.assertTrue(learned.chassis_type_confident)
        self.assertEqual(learned.chassis_member_count, 1)
        self.assertFalse(learned.is_modular)
        self.assertTrue(learned.modularity_confident)

    def test_unknown_single_rp_remains_inconclusive(self):
        learned = SimpleNamespace(
            slot={"rp": {"0/RP0": {"redundancy_state": "Active"}}},
            chassis="UNKNOWN-MODULAR-SYSTEM",
            _FIXED_SINGLE_RP_SYSTEM_TYPES=Platform._FIXED_SINGLE_RP_SYSTEM_TYPES,
        )

        Platform._populate_topology(learned)

        self.assertIsNone(learned.chassis_type)
        self.assertFalse(learned.chassis_type_confident)
        self.assertIsNone(learned.chassis_member_count)
        self.assertFalse(learned.modularity_confident)


if __name__ == '__main__':
    unittest.main()
