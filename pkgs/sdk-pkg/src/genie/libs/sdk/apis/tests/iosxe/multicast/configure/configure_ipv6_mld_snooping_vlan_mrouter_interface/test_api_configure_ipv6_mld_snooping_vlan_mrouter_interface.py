import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_mld_snooping_vlan_mrouter_interface,
)


class TestConfigureIpv6MldSnoopingVlanMrouterInterface(TestCase):

    def test_configure_ipv6_mld_snooping_vlan_mrouter_interface(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_mld_snooping_vlan_mrouter_interface(
            device,
            1,
            "Gi1/0/1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ipv6 mld snooping vlan 1 mrouter interface Gi1/0/1",
        )


if __name__ == "__main__":
    unittest.main()
