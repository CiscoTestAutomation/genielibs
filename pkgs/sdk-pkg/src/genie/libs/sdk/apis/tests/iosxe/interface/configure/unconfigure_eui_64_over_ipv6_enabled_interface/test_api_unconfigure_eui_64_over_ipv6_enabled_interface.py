import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_eui_64_over_ipv6_enabled_interface


class TestUnconfigureEui64OverIpv6EnabledInterface(TestCase):

    def test_unconfigure_eui_64_over_ipv6_enabled_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_eui_64_over_ipv6_enabled_interface(
            device,
            "TwentyFiveGigE1/0/23",
            "2009::2/64",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE1/0/23",
                "no ipv6 address 2009::2/64 eui-64",
            ],
        )


if __name__ == "__main__":
    unittest.main()