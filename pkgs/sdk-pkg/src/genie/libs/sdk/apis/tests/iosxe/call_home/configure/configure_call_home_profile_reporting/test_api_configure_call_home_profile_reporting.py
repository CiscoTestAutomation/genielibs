from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile_reporting


class TestConfigureCallHomeProfileReporting(TestCase):

    def test_configure_call_home_profile_reporting(self):
        device = Mock()
        result = configure_call_home_profile_reporting(device, 'test', 'all')
        expected_output = None
        self.assertEqual(result, expected_output)
        device.configure.assert_called_with([
            'call-home',
            'profile test',
            'reporting all'
        ])
