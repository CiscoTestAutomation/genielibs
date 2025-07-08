from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_contact_email_addr


class TestConfigureCallHomeContactEmailAddr(TestCase):

    def test_configure_call_home_contact_email_addr(self):
        self.device = Mock()
        result = configure_call_home_contact_email_addr(self.device, 'test@test.com')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'contact-email-addr test@test.com'],)
        )
