from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import configure_isakmp_key_simple
from unittest.mock import Mock


class TestConfigureIsakmpKeySimple(TestCase):

    def test_configure_isakmp_key_simple(self):
        self.device = Mock()
        result = configure_isakmp_key_simple(self.device, 'cisco', '0.0.0.0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto isakmp key cisco address 0.0.0.0'],)
        )
