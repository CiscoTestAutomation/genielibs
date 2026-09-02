import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import (
    configure_ip_multicast_routing,
)


class TestConfigureIpMulticastRouting(TestCase):

    def test_configure_ip_multicast_routing(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_multicast_routing(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "ip multicast-routing",
        )


if __name__ == "__main__":
    unittest.main()
