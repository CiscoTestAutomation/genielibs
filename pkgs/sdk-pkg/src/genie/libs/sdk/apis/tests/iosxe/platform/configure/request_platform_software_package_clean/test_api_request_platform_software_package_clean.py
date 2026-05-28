import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import request_platform_software_package_clean


class TestRequestPlatformSoftwarePackageClean(unittest.TestCase):

    def test_request_platform_software_package_clean(self):
        device = Mock()

        result = request_platform_software_package_clean(device, 'all', 'file', 'flash:')

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('request platform software package clean switch all file flash:',)
        )