from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ipsec.configure import clear_crypto_cryptotype


class TestClearCryptoCryptotype(TestCase):

    def test_clear_crypto_cryptotype(self):
        self.device = Mock()
        cryptotype = 'ikev2'
        clear_crypto_cryptotype(self.device, cryptotype=cryptotype)
        self.device.execute.assert_called_once_with(
            'clear crypto ikev2'
        )
