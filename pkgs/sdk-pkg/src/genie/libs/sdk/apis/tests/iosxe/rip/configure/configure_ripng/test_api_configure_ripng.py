import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rip.configure import (
    configure_ripng
)


class TestConfigureRipng(unittest.TestCase):

    def test_configure_ripng(self):
        device = Mock()

        result = configure_ripng(
            device,
            '64'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ipv6 router rip 64',)
        )