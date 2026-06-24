import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ipv6_mld_static_group,
)


class TestConfigureIpv6MldStaticGroup(TestCase):

    def test_configure_ipv6_mld_static_group(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_mld_static_group(
            device,
            "vlan100",
            "FF33:1::3",
            "2000::21",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface vlan100", sent_commands)
        self.assertIn(
            "ipv6 mld static-group FF33:1::3 2000::21",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()