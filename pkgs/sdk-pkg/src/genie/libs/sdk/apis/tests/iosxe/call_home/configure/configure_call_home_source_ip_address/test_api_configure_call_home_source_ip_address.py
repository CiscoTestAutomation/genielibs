from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_source_ip_address


class TestConfigureCallHomeSourceIpAddress(TestCase):
    
    def test_configure_call_home_source_ip_address(self):
        device = Mock()
        result = configure_call_home_source_ip_address(device, '1.1.1.1')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'source-ip-address 1.1.1.1'],)
        )