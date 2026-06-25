import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_smart_usage_interval


class TestConfigureLicenseSmartUsageInterval(unittest.TestCase):

    def test_configure_license_smart_usage_interval(self):
        device = Mock()

        result = configure_license_smart_usage_interval(
            device,
            '2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart usage interval 2',)
        )