import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import tunnel_range_shut_unshut


class TestTunnelRangeShutUnshut(TestCase):

    def test_tunnel_range_shut_unshut(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = tunnel_range_shut_unshut(
            device,
            1,
            1000,
            "shut",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface range Tunnel 1-1000",
                "shut",
            ],
        )


if __name__ == "__main__":
    unittest.main()