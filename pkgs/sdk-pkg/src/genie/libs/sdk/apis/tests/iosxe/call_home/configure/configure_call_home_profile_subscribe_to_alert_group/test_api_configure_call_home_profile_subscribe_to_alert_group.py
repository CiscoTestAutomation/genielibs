from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_profile_subscribe_to_alert_group


class TestConfigureCallHomeProfileSubscribeToAlertGroup(TestCase):
    
    def test_configure_call_home_profile_subscribe_to_alert_group(self):
        device = Mock()
        result = configure_call_home_profile_subscribe_to_alert_group(device, 'test', 'crash')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'call-home',
                    'profile test',
                    'subscribe-to-alert-group crash'
                ],
            )
        )
