import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import (
    unconfigure_ip_multicast_routing_distributed,
)


class TestUnconfigureIpMulticastRoutingDistributed(TestCase):

    def test_unconfigure_ip_multicast_routing_distributed(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_multicast_routing_distributed(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no ip multicast-routing distributed",
        )


if __name__ == "__main__":
    unittest.main()
