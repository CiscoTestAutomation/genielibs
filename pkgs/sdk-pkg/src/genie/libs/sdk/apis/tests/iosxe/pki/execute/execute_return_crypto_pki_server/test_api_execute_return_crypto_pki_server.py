from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import execute_return_crypto_pki_server
from unittest.mock import Mock


class TestExecuteReturnCryptoPkiServer(TestCase):

    def test_execute_return_crypto_pki_server(self):
        self.device = Mock()
        results_map = {
            'crypto pki authenticate myCA': "    % Certificate Authority (trustpoint) 'myCA' is unknown",
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_return_crypto_pki_server(self.device, 'authenticate', 'myCA', ('-----BEGIN CERTIFICATE-----\n'
 'MIIDXTCCAkWgAwIBAgIJAKoK/OvD/XjIMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNV\n'
 'BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX\n'
 'aWRnaXRzIFB0eSBMdGQwHhcNMTMxMjMwMTY1NzUwWhcNMjMxMjI4MTY1NzUwWjBF\n'
 'MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50\n'
 'ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\n'
 'CgKCAQEAwU8/q3W0y9DGF5Z4BPQvNvNnUo4DEk+zM7ZXBh2LZwLSxF8MhAwLmWgn\n'
 '-----END CERTIFICATE-----\n'), 5)
        self.assertIn(
            'crypto pki authenticate myCA',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = "    % Certificate Authority (trustpoint) 'myCA' is unknown"
        self.assertEqual(result, expected_output)
