from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vlan.clear import clear_vlan
from unittest.mock import Mock


class TestClearVlan(TestCase):

    def test_clear_vlan(self):
        self.device = Mock()
        results_map = {
            'clear vlan 100': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_vlan(self.device, 100, None, False)
        self.assertIn(
            'clear vlan 100',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
