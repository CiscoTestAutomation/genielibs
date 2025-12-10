from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import change_pki_certificate_hash
from unittest.mock import Mock


class TestChangePkiCertificateHash(TestCase):

    def test_change_pki_certificate_hash(self):
        self.device = Mock()
        result = change_pki_certificate_hash(self.device, 'sha256')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki certificate self-signed hash sha256'],)
        )
