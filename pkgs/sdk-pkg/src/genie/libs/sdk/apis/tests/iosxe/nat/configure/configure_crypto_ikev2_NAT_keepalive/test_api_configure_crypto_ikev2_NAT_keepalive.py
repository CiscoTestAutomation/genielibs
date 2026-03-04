from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_crypto_ikev2_NAT_keepalive

class TestConfigureCryptoIkev2NatKeepalive(TestCase):

    def test_configure_crypto_ikev2_NAT_keepalive(self):
        device = Mock()
        result = configure_crypto_ikev2_NAT_keepalive(device, 30)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['crypto ikev2 nat keepalive 30'],)
        )