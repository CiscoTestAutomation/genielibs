from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_isakmp_key_simple
from unittest.mock import Mock


class TestUnconfigureIsakmpKeySimple(TestCase):

    def test_unconfigure_isakmp_key_simple(self):
        self.device = Mock()
        result = unconfigure_isakmp_key_simple(self.device, 'cisco', '0.0.0.0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto isakmp key cisco address 0.0.0.0'],)
        )
