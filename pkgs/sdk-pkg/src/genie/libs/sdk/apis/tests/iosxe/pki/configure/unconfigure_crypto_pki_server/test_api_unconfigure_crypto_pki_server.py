from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_crypto_pki_server


class TestUnconfigureCryptoPkiServer(TestCase):

    def test_unconfigure_crypto_pki_server(self):
        device = Mock()
        result = unconfigure_crypto_pki_server(
            device,
            'root'
        )
        self.assertEqual(result, True)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no crypto pki server root',)
        )