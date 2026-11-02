import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_mld_snooping_vlan_static_interface,
)


class TestConfigureIpv6MldSnoopingVlanStaticInterface(TestCase):

    def test_configure_ipv6_mld_snooping_vlan_static_interface(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_mld_snooping_vlan_static_interface(
            device,
            "1",
            "FF08::10",
            " gi0/0",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ipv6 mld snooping vlan 1 static FF08::10 interface  gi0/0",
        )


if __name__ == "__main__":
    unittest.main()
