from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_export_advanced
from unittest.mock import Mock


class TestConfigurePkiExportAdvanced(TestCase):

    def test_configure_pki_export_advanced(self):
        self.device = Mock()
        result = configure_pki_export_advanced(self.device, 'my_trustpoint', 'pkcs12', 'cisco123', 'tftp:', 'my_cert.p12', '192.168.1.100/certificates/my_cert.p12', 'url', 'bootflash:', 'my_cert.pem', '192.168.1.100/certificates/my_cert.pem', 'rollover')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('crypto pki export my_trustpoint pkcs12 '
 'tftp:192.168.1.100/certificates/my_cert.p12 password cisco123'),)
        )
