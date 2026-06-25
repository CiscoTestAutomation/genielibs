import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_license_smart_usage_interval


class TestUnconfigureLicenseSmartUsageInterval(unittest.TestCase):

    def test_unconfigure_license_smart_usage_interval(self):
        device = Mock()

        result = unconfigure_license_smart_usage_interval(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no license smart usage interval',)
        )