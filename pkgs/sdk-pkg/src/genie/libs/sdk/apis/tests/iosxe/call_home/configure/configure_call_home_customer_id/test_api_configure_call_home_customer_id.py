from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_customer_id


class TestConfigureCallHomeCustomerId(TestCase):

    def test_configure_call_home_customer_id(self):
        self.device = Mock()
        result = configure_call_home_customer_id(self.device, 'test123')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'customer-id test123'],)
        )
