from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile_destination_address

class TestConfigureCallHomeProfileDestinationAddress(TestCase):

    def test_configure_call_home_profile_destination_address(self):
        device = Mock()
        result = configure_call_home_profile_destination_address(device, 'test', 'email', '123@cisco.com')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'profile test', 'destination address email 123@cisco.com'],)
        )