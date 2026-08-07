import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ip_route_cache


class TestUnconfigureIpRouteCache(TestCase):

    def test_unconfigure_ip_route_cache(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_route_cache(
            device,
            "GigabitEthernet2/0/17",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface GigabitEthernet2/0/17",
            sent_commands,
        )
        self.assertIn(
            "no ip route-cache",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()