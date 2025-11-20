from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_server
from unittest.mock import Mock


class TestConfigureCryptoPkiServer(TestCase):

    def test_configure_crypto_pki_server(self):
        self.device = Mock()
        result = configure_crypto_pki_server(self.device, 'ca', 'cisco123', None, None, None, None, 'pkcs12', 'cisco123', None, 'bootflash:', None, 'p12', False, None, 'auto', None, None, None, None, None, None, None, None, None, None, None, None, False, None, None, None, None, None, 80, False, None, None, None, False, None, None, None, False, None, None, None, False, None, None, None, False, None, None, None, False, None, None, None, False, False, False, False, False, False, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip http server', 'crypto pki server ca', 'database archive pkcs12', 'database archive pkcs12 password  cisco123', 'database url p12 bootflash:', 'database url p12', 'grant auto'],)
        )
        self.assertEqual(
            self.device.configure.mock_calls[1].args,
            (['crypto pki server ca', 'no shut'],)
        )
