import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rip.configure import (
    unconfig_interface_ripng
)


class TestUnconfigInterfaceRipng(unittest.TestCase):

    def test_unconfig_interface_ripng(self):
        device = Mock()

        result = unconfig_interface_ripng(
            device,
            'TwentyFiveGigE1/0/2',
            '64'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/2',
              'no ipv6 rip 64 enable'],)
        )