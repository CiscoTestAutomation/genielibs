from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_street_address


class TestConfigureCallHomeStreetAddress(TestCase):
    
    def test_configure_call_home_street_address(self):
        device = Mock()
        result = configure_call_home_street_address(device, '123abcStreet')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'street-address 123abcStreet'],)
        )
