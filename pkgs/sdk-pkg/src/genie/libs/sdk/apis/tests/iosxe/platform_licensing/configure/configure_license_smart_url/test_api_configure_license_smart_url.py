import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_smart_url


class TestConfigureLicenseSmartUrl(unittest.TestCase):

    def test_configure_license_smart_url(self):
        device = Mock()

        result = configure_license_smart_url(
            device,
            'test'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart url smart test',)
        )