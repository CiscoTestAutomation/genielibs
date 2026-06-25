import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_platform


class TestConfigurePlatform(unittest.TestCase):

    def test_configure_platform(self):
        device = Mock()

        result = configure_platform(
            device,
            'hsec-license-release'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('platform hsec-license-release',)
        )