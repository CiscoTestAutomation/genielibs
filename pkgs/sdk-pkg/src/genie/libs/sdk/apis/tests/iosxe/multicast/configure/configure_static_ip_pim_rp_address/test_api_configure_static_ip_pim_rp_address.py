import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_static_ip_pim_rp_address,
)


class TestConfigureStaticIpPimRpAddress(TestCase):

    def test_configure_static_ip_pim_rp_address(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_static_ip_pim_rp_address(device, "5.5.5.5", "None")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ip pim vrf None rp-address 5.5.5.5")


if __name__ == "__main__":
    unittest.main()
