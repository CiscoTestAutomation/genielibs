from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import execute_crypto_pki_server_advanced
from unittest.mock import Mock


class TestExecuteCryptoPkiServerAdvanced(TestCase):

    def test_execute_crypto_pki_server_advanced(self):
        self.device = Mock()
        results_map = {
            ("crypto pki server myCA start",): "% Certificate server 'myCA' is not known."
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(tuple(arg))
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_crypto_pki_server_advanced(self.device, 'myCA', False, False, False, False, False, None, None, False, False, False, None, False, False, None, None, None, False, False, False, None, True, False)
        self.assertIn(
            "crypto pki server myCA start",
            self.device.execute.call_args_list[0][0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)