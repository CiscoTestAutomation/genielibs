import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rip.configure import (
    unconfigure_ripng
)


class TestUnconfigureRipng(unittest.TestCase):

    def test_unconfigure_ripng(self):
        device = Mock()

        result = unconfigure_ripng(
            device,
            '64'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 router rip 64',)
        )