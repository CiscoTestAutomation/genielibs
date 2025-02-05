from unittest import TestCase
from genie.libs.sdk.apis.iosxe.eem.configure import configure_eem_action_info_type_routername
from unittest.mock import Mock


class TestConfigureEemActionInfoTypeRoutername(TestCase):

    def test_configure_eem_action_info_type_routername(self):
        self.device = Mock()
        result = configure_eem_action_info_type_routername(self.device, 'DAILY_HEARTBEAT_SYSLOG', 1.0)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['event manager applet DAILY_HEARTBEAT_SYSLOG', 'action 1.0 info type routername'],)
        )
