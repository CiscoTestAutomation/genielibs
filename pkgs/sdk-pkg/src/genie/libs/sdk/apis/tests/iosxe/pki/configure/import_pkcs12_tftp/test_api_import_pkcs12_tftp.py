from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import import_pkcs12_tftp
from unittest.mock import Mock


class TestImportPkcs12Tftp(TestCase):

    def test_import_pkcs12_tftp(self):
        self.device = Mock()
        result = import_pkcs12_tftp(self.device, '192.168.1.100', 'cert_bundle.p12', 'TP-CA', 'pkcs12', 'cisco123')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki import TP-CA pkcs12 tftp://192.168.1.100/cert_bundle.p12 password cisco123'],)
        )
