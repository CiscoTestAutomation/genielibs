from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile_active

class TestConfigureCallHomeProfileActive(TestCase):

    def test_configure_call_home_profile_active(self):
        device = Mock()
        result = configure_call_home_profile_active(device, 'test')
        expected_output = None
        self.assertEqual(result, expected_output)
        # If unsure about the command(s), uncomment to inspect:
        # print(device.configure.mock_calls)
        # Update the assertion below to match the actual output.
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'profile test', 'active'],)
        )