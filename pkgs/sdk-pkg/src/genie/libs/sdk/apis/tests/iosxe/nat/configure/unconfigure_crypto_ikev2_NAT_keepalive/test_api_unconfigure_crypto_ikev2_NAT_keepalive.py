from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_crypto_ikev2_NAT_keepalive

class TestUnconfigureCryptoIkev2NatKeepalive(TestCase):

    def test_unconfigure_crypto_ikev2_NAT_keepalive(self):
        device = Mock()
        result = unconfigure_crypto_ikev2_NAT_keepalive(device, 30)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no crypto ikev2 nat keepalive 30'],)
        )