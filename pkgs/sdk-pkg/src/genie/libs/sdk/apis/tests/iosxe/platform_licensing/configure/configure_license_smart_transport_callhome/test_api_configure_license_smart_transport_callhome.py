import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_smart_transport_callhome


class TestConfigureLicenseSmartTransportCallhome(unittest.TestCase):

    def test_configure_license_smart_transport_callhome(self):
        device = Mock()

        result = configure_license_smart_transport_callhome(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart transport callhome',)
        )