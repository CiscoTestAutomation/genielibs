import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile_destination_message_size_limit


class TestConfigureCallHomeProfileDestinationMessageSizeLimit(TestCase):

    def test_configure_call_home_profile_destination_message_size_limit(self):
        device = Mock()
        result = configure_call_home_profile_destination_message_size_limit(device, 'test', '1000')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        device.configure.assert_called_once_with([
            "call-home",
            "profile test",
            "destination message-size-limit 1000",
        ])


if __name__ == '__main__':
    unittest.main()