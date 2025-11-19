from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import export_pkcs12_tftp
from unittest.mock import Mock


class TestExportPkcs12Tftp(TestCase):

    def test_export_pkcs12_tftp(self):
        self.device = Mock()
        result = export_pkcs12_tftp(self.device, '192.168.1.100', 'backup_cert_bundle.p12', 'TP-CA', 'pkcs12')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki export TP-CA pkcs12 tftp://192.168.1.100/backup_cert_bundle.p12 password cisco123'],)
        )
