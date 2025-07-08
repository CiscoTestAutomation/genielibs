from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_alert_group_config_snapshot


class TestConfigureCallHomeAlertGroupConfigSnapshot(TestCase):

    def test_configure_call_home_alert_group_config_snapshot(self):
        self.device = Mock()
        result = configure_call_home_alert_group_config_snapshot(self.device, 'no', 'help')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'alert-group-config snapshot', 'no add-command help'],)
        )
