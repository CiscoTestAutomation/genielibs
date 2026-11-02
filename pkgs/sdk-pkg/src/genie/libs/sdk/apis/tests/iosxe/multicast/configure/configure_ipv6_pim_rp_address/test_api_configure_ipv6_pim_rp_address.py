import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_pim_rp_address,
)


class TestConfigureIpv6PimRpAddress(TestCase):

    def test_configure_ipv6_pim_rp_address(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_pim_rp_address(device, "2012:AA:23::3")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "ipv6 pim rp-address 2012:AA:23::3",
            ],
        )


if __name__ == "__main__":
    unittest.main()
