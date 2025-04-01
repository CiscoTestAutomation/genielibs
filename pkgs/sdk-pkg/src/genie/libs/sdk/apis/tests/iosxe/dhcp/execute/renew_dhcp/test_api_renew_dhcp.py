from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.execute import renew_dhcp
from unittest.mock import Mock


class TestRenewDhcp(TestCase):

    def test_renew_dhcp(self):
        self.device = Mock()
        results_map = {
            'renew dhcp GigabitEthernet0/0': 'Interface does not have a DHCP originated address',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = renew_dhcp(self.device, 'GigabitEthernet0/0')
        self.assertIn(
            'renew dhcp GigabitEthernet0/0',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
