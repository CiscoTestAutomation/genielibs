import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_mld_vlan_immediate_leave,
)


class TestConfigureIpv6MldVlanImmediateLeave(TestCase):

    def test_configure_ipv6_mld_vlan_immediate_leave(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_mld_vlan_immediate_leave(device, " 1")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "ipv6 mld snooping vlan  1 immediate-leave",
            ],
        )


if __name__ == "__main__":
    unittest.main()
