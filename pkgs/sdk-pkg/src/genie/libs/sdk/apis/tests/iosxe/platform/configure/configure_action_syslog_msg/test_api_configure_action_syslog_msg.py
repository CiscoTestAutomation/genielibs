from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_action_syslog_msg


class TestConfigureActionSyslogMsg(TestCase):

    def test_configure_action_syslog_msg(self):
        device = Mock()
        result = configure_action_syslog_msg(
            device,
            'testapplet',
            '5.1',
            '---message---'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['event manager applet testapplet', 'action 5.1 syslog msg ---message---'],)
        )