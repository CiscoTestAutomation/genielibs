import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_eui_64_over_ipv6_enabled_interface,
)


class TestConfigureEui64OverIpv6EnabledInterface(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.configure = Mock(return_value='')

    def test_configure_eui_64_over_ipv6_enabled_interface(self):
        result = configure_eui_64_over_ipv6_enabled_interface(
            self.device,
            'TwentyFiveGigE1/0/23',
            '2009::2/64'
        )

        expected_output = None
        expected_config = [
            'interface TwentyFiveGigE1/0/23',
            'ipv6 address 2009::2/64 eui-64'
        ]

        self.device.configure.assert_called_once_with(expected_config)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()