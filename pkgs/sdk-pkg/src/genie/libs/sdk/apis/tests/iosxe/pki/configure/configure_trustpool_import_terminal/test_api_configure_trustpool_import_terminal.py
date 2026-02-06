from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_trustpool_import_terminal
from unittest.mock import Mock


class TestConfigureTrustpoolImportTerminal(TestCase):

    def test_configure_trustpool_import_terminal(self):
        self.device = Mock()
        result = configure_trustpool_import_terminal(self.device, ('-----BEGIN CERTIFICATE-----\n'
 'MIIDXTCCAkWgAwIBAgIJAKoK/OvD/XjIMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNV\n'
 'BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX\n'
 'aWRnaXRzIFB0eSBMdGQwHhcNMTMxMjMwMTY1NzUwWhcNMjMxMjI4MTY1NzUwWjBF\n'
 'MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50\n'
 'ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\n'
 'CgKCAQEAwU8/q3W0y9DGF5Z4BPQvNvNnUo4DEk+zM7ZXBh2LZwLSxF8MhAwLmWgn\n'
 '-----END CERTIFICATE-----'))
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('crypto pki trustpool import terminal',)
        )
