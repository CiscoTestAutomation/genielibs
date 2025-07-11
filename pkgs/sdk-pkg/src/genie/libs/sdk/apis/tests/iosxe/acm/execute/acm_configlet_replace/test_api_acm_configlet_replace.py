from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_configlet_replace
from unittest.mock import Mock


class TestAcmConfigletReplace(TestCase):

    def test_acm_configlet_replace(self):
        self.device = Mock()
        results_map = {
            'acm configlet modify demo replace 1 vlan 50': ' Successfully replaced cli: vlan 50 at Index : 1',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_configlet_replace(self.device, 'demo', '1', 'vlan 50')
        self.assertIn(
            'acm configlet modify demo replace 1 vlan 50',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
