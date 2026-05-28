import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_license_smart_transport_off


class TestConfigureLicenseSmartTransportOff(unittest.TestCase):

    def test_configure_license_smart_transport_off(self):
        device = Mock()

        result = configure_license_smart_transport_off(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart transport off',)
        )