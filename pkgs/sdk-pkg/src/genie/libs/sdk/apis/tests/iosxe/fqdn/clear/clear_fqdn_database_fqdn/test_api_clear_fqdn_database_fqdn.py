from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fqdn.clear import clear_fqdn_database_fqdn
from unittest.mock import Mock


class TestClearFqdnDatabaseFqdn(TestCase):

    def test_clear_fqdn_database_fqdn(self):
        self.device = Mock()
        results_map = {
            'clear fqdn database fqdn test': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_fqdn_database_fqdn(self.device, 'test')
        self.assertIn(
            'clear fqdn database fqdn test',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)