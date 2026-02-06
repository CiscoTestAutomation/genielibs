from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile_anonymous_reporting_only

class TestConfigureCallHomeProfileAnonymousReportingOnly(TestCase):

    def test_configure_call_home_profile_anonymous_reporting_only(self):
        device = Mock()
        result = configure_call_home_profile_anonymous_reporting_only(device, 'test')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'profile test', 'anonymous-reporting-only'],)
        )