import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_pvlan_host_assoc


class TestUnconfigureInterfacePvlanHostAssoc(TestCase):

    def test_unconfigure_interface_pvlan_host_assoc(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_pvlan_host_assoc(
            device,
            "TwentyFiveGigE1/0/31",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE1/0/31",
                "no switchport private-vlan host-association",
            ],
        )


if __name__ == "__main__":
    unittest.main()