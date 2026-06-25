import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_bandwidth


class TestUnconfigureInterfaceBandwidth(TestCase):

    def test_unconfigure_interface_bandwidth(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_bandwidth(
            device,
            "Port-channel10",
            "30000000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Port-channel10",
                "no bandwidth 30000000",
            ],
        )


if __name__ == "__main__":
    unittest.main()