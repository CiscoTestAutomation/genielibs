from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import remove_pki_certificate_chain
from unittest.mock import Mock


class TestRemovePkiCertificateChain(TestCase):

    def test_remove_pki_certificate_chain(self):
        self.device = Mock()
        result = remove_pki_certificate_chain(self.device, 'root')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no crypto pki certificate chain root',)
        )
