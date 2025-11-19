from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import crypto_pki_trustpool_import
from unittest.mock import Mock


class TestCryptoPkiTrustpoolImport(TestCase):

    def test_crypto_pki_trustpool_import(self):
        self.device = Mock()
        result = crypto_pki_trustpool_import(self.device, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki trustpool import ca-bundle'],)
        )
