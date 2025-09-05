from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import clear_crypto_pki
from unittest.mock import Mock


class TestClearCryptoPki(TestCase):

    def test_clear_crypto_pki(self):
        self.device = Mock()
        results_map = {
            'clear crypto pki benchmarks': '',
            'clear crypto pki counters': '',
            'clear crypto pki crl': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_crypto_pki(self.device, True, True, True)
        self.assertIn(
            'clear crypto pki benchmarks',
            self.device.execute.call_args_list[0][0]
        )
        self.assertIn(
            'clear crypto pki counters',
            self.device.execute.call_args_list[1][0]
        )
        self.assertIn(
            'clear crypto pki crl',
            self.device.execute.call_args_list[2][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
