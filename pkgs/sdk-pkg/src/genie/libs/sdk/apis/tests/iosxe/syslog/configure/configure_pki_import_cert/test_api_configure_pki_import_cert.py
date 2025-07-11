from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import configure_pki_import_cert
from unittest.mock import Mock


class TestConfigurePkiImportCert(TestCase):

    def test_configure_pki_import_cert(self):
        self.device = Mock()
        result = configure_pki_import_cert(self.device, 'tp1', 'aaa')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('crypto pki import tp1 certificate',)
        )
