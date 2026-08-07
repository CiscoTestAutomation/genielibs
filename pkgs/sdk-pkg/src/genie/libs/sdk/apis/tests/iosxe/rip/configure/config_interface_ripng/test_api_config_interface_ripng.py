import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rip.configure import (
    config_interface_ripng
)


class TestConfigInterfaceRipng(unittest.TestCase):

    def test_config_interface_ripng(self):
        device = Mock()

        result = config_interface_ripng(
            device,
            'TwentyFiveGigE1/0/2',
            '64'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/2',
              'ipv6 rip 64 enable'],)
        )