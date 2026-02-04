from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_mail_server

class TestConfigureCallHomeMailServer(TestCase):

    def test_configure_call_home_mail_server(self):
        device = Mock()
        result = configure_call_home_mail_server(device, 'test', '3', 'tls')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'mail-server test priority 3 secure tls'],)
        )