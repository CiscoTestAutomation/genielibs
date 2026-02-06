from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_switchport_output
from unittest.mock import Mock


class TestGetInterfaceSwitchportOutput(TestCase):

    def test_get_interface_switchport_output(self):
        self.device = Mock()
        results_map = {
            'show interfaces GigabitEthernet0/1/5 switchport': 
            '''Name: Gi0/1/5
            Switchport: Enabled
            Administrative Mode: dynamic auto
            Operational Mode: down
            Administrative Trunking Encapsulation: dot1q
            Negotiation of Trunking: On
            Access Mode VLAN: 1 (default)
            Trunking Native Mode VLAN: 1 (default)
            Administrative Native VLAN tagging: disabled
            Voice VLAN: none
            Administrative private-vlan host-association: none 
            Administrative private-vlan mapping: none 
            Administrative private-vlan trunk native VLAN: none
            Administrative private-vlan trunk Native VLAN tagging: enabled
            Administrative private-vlan trunk encapsulation: dot1q
            Administrative private-vlan trunk normal VLANs: none
            Administrative private-vlan trunk associations: none
            Administrative private-vlan trunk mappings: none
            Operational private-vlan: none
            Trunking VLANs Enabled: ALL
            Pruning VLANs Enabled: 2-1001
            Capture Mode Disabled
            Capture VLANs Allowed: ALL

            Protected: false
            Unknown unicast blocked: disabled
            Unknown multicast blocked: disabled
            Priority for untagged frame: 0
            Override vlan tag priority: FALSE
            Appliance trust: none''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = get_interface_switchport_output(self.device, 'GigabitEthernet0/1/5')
        self.assertIn(
            'show interfaces GigabitEthernet0/1/5 switchport',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show interfaces GigabitEthernet0/1/5 switchport']
        self.assertEqual(result, expected_output)
