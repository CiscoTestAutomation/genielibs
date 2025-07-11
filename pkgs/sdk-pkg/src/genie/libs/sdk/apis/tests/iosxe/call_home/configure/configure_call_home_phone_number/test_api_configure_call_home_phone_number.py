from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_phone_number


class TestConfigureCallHomePhoneNumber(TestCase):

    def test_configure_call_home_phone_number(self):
        self.device = Mock()
        result = configure_call_home_phone_number(self.device, '+123456789012')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'phone-number +123456789012'],)
        )
