import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_smart


class TestConfigureLicenseSmart(unittest.TestCase):

    def test_configure_license_smart(self):
        device = Mock()

        result = configure_license_smart(
            device,
            'transport smart'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart transport smart',)
        )