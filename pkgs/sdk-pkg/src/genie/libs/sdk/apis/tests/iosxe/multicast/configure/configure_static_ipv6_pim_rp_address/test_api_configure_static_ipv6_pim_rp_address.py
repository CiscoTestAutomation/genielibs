import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_static_ipv6_pim_rp_address,
)


class TestConfigureStaticIpv6PimRpAddress(TestCase):

    def test_configure_static_ipv6_pim_rp_address(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_static_ipv6_pim_rp_address(
            device,
            "2001::100",
            "None",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ipv6 pim vrf None rp-address 2001::100")


if __name__ == "__main__":
    unittest.main()
