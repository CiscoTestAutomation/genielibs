import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_pvlan_mapping


class TestUnconfigureInterfacePvlanMapping(TestCase):

    def test_unconfigure_interface_pvlan_mapping(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_pvlan_mapping(
            device,
            "TwentyFiveGigE1/0/35",
            "500",
            "501",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE1/0/35",
                "no switchport private-vlan mapping 500 501",
            ],
        )


if __name__ == "__main__":
    unittest.main()