import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_smart_transport_cslu


class TestConfigureLicenseSmartTransportCslu(unittest.TestCase):

    def test_configure_license_smart_transport_cslu(self):
        device = Mock()

        result = configure_license_smart_transport_cslu(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart transport cslu',)
        )