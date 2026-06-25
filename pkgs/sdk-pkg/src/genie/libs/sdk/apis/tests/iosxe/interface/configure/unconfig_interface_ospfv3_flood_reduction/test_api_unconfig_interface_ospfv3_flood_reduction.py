import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_interface_ospfv3_flood_reduction


class TestUnconfigInterfaceOspfv3FloodReduction(TestCase):

    def test_unconfig_interface_ospfv3_flood_reduction(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_flood_reduction(
            device,
            "vmi1",
            "1",
            "ipv6",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface vmi1\nno ospfv3 1 ipv6 flood-reduction",
        )


if __name__ == "__main__":
    unittest.main()