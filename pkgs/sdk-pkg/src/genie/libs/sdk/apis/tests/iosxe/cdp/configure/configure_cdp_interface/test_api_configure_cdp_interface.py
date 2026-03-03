from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp_interface

class TestConfigureCdpInterface(TestCase):

    def test_configure_cdp_interface(self):
        device = Mock()
        result = configure_cdp_interface(device, 'Te0/1/1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['cdp run', 'interface Te0/1/1', 'cdp enable'],)
        )