from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile


class TestConfigureCallHomeProfile(TestCase):
  
    def test_configure_call_home_profile(self):
        device = Mock()
        result = configure_call_home_profile(device, 'http://www.test1.com', 'CiscoTAC-1')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'call-home',
                'no http secure server-identity-check',
                'profile CiscoTAC-1',
                'active',
                'destination transport-method http',
                'destination address http http://www.test1.com',
                'reporting smart-licensing-data'
            ],)
        )

