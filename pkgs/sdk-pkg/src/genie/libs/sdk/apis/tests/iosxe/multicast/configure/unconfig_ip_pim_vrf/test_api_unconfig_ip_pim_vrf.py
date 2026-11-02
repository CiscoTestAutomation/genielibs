import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    unconfig_ip_pim_vrf,
)


class TestUnconfigIpPimVrf(TestCase):

    def test_unconfig_ip_pim_vrf(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfig_ip_pim_vrf(device, "2", "autorp listener")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "no ip pim vrf 2 autorp listener")


if __name__ == "__main__":
    unittest.main()
