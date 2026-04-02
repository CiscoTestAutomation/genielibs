from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.clear import clear_ip_ssh_pubkey_server
from unittest.mock import Mock


class TestClearIpSshPubkeyServer(TestCase):

    def test_clear_ip_ssh_pubkey_server(self):
        self.device = Mock()
        results_map = {
            'clear ip ssh pubkey server all': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_ip_ssh_pubkey_server(self.device)
        self.assertIn(
            'clear ip ssh pubkey server all',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
