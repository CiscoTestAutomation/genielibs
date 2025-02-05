from unittest import TestCase
from genie.libs.sdk.apis.iosxe.eem.configure import configure_eem_action_syslog_msg
from unittest.mock import Mock


class TestConfigureEemActionSyslogMsg(TestCase):

    def test_configure_eem_action_syslog_msg(self):
        self.device = Mock()
        result = configure_eem_action_syslog_msg(self.device, 'WRITE_MEM_EEM', 1.1, 'Saving the configuration to the startup')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['event manager applet WRITE_MEM_EEM', 'action 1.1 syslog msg "Saving the configuration to the startup"'],)
        )
