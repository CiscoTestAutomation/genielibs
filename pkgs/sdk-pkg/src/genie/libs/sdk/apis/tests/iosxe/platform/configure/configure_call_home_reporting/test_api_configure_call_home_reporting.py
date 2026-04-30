from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_call_home_reporting


class TestConfigureCallHomeReporting(TestCase):

    def test_configure_call_home_reporting(self):
        device = Mock()
        result = configure_call_home_reporting(
            device,
            address='contact-email-addr',
            email='test@test.com'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('call-home reporting contact-email-addr test@test.com',)
        )