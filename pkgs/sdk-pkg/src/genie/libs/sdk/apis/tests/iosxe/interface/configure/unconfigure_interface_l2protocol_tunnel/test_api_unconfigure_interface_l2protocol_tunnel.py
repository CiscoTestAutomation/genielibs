import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_l2protocol_tunnel


class TestUnconfigureInterfaceL2protocolTunnel(TestCase):

    def test_unconfigure_interface_l2protocol_tunnel(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_l2protocol_tunnel(
            device,
            "Gi1/0/5",
            "drop-threshold",
            "lacp",
            "point-to-point",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Gi1/0/5",
                "no l2protocol-tunnel drop-threshold point-to-point lacp",
            ],
        )


if __name__ == "__main__":
    unittest.main()