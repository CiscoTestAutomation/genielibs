from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import execute_trim_crypto_pki_certificate
from unittest.mock import Mock


class TestExecuteTrimCryptoPkiCertificate(TestCase):

    def test_execute_trim_crypto_pki_certificate(self):
        self.device = Mock()
        results_map = {
            ('crypto pki server root trim url example.com',): "% Certificate server 'root' is not known.",
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(tuple(arg))
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_trim_crypto_pki_certificate(self.device, 'root', False, 'example.com', True)
        self.assertIn(
            ['crypto pki server root trim url example.com'],
            self.device.execute.call_args_list[0][0]
        )
        expected_output = "% Certificate server 'root' is not known."
        self.assertEqual(result, expected_output)
