from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_alert_group


class TestConfigureCallHomeAlertGroup(TestCase):

    def test_configure_call_home_alert_group(self):
        self.device = Mock()
        result = configure_call_home_alert_group(self.device, 'inventory')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'alert-group inventory'],)
        )
