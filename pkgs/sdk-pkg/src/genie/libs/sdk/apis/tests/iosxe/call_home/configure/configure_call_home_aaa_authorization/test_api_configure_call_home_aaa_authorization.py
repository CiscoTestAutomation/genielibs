from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_aaa_authorization

class TestConfigureCallHomeAaaAuthorization(TestCase):

    def test_configure_call_home_aaa_authorization(self):
        device = Mock()
        result = configure_call_home_aaa_authorization(device, 'test')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'aaa-authorization username test'],)
        )