import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile_destination_transport_method


class TestConfigureCallHomeProfileDestinationTransportMethod(TestCase):

    def test_configure_call_home_profile_destination_transport_method(self):
        device = Mock()
        result = configure_call_home_profile_destination_transport_method(device, 'test', 'email')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        device.configure.assert_called_once_with([
            "call-home",
            "profile test",
            "destination transport-method email",
        ])


if __name__ == '__main__':
    unittest.main()