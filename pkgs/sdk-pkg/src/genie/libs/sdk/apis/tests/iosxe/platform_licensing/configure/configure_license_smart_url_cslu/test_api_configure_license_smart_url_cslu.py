import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_smart_url_cslu


class TestConfigureLicenseSmartUrlCslu(unittest.TestCase):

    def test_configure_license_smart_url_cslu(self):
        device = Mock()

        result = configure_license_smart_url_cslu(
            device,
            'http://192.168.0.1:8182/cslu/v1/pi'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart url cslu http://192.168.0.1:8182/cslu/v1/pi',)
        )