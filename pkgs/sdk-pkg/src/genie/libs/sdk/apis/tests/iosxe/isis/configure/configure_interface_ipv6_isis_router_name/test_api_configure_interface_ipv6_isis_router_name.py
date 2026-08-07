import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import (
    configure_interface_ipv6_isis_router_name,
)


class TestConfigureInterfaceIpv6IsisRouterName(TestCase):

    def test_configure_interface_ipv6_isis_router_name(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ipv6_isis_router_name(
            device,
            "FiftyGigE1/0/1",
            "10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface FiftyGigE1/0/1",
                "ipv6 router isis 10",
            ],
        )


if __name__ == "__main__":
    unittest.main()
