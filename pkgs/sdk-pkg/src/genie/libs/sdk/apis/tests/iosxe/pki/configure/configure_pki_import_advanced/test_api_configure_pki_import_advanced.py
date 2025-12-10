from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_import_advanced
from unittest.mock import Mock


class TestConfigurePkiImportAdvanced(TestCase):

    def test_configure_pki_import_advanced(self):
        self.device = Mock()
        result = configure_pki_import_advanced(self.device, 'my_trustpoint', 'pkcs12', 'cisco123', 'url', 'bootflash:', '192.168.1.100/certificates/import_cert.pem', 'tftp:', '192.168.1.100/certificates/import_cert.p12')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('crypto pki import my_trustpoint pkcs12 '
 'tftp:192.168.1.100/certificates/import_cert.p12 password cisco123'),)
        )
