import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_smart_proxy


class TestConfigureLicenseSmartProxy(unittest.TestCase):

    def test_configure_license_smart_proxy(self):
        device = Mock()

        result = configure_license_smart_proxy(
            device,
            '1.1.1.1',
            80
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['license smart proxy address 1.1.1.1', 'license smart proxy port 80'],)
        )