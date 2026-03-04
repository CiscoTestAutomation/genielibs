from unittest import TestCase
from genie.libs.sdk.apis.linux.execute import switch_proxmox_vm_power
from unittest.mock import Mock

class TestSwitchProxmoxVmPower(TestCase):

    def test_switch_proxmox_vm_power_off(self):
        self.device = Mock()
        results_map = {
            'qm stop 100': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = switch_proxmox_vm_power(self.device, '100', 'stop')
        self.assertIn(
            'qm stop 100',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
    
    def test_switch_proxmox_vm_power_start(self):
        self.device = Mock()
        results_map = {
            'qm start 100': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = switch_proxmox_vm_power(self.device, '100', 'start')
        self.assertIn(
            'qm start 100',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
    
    def test_switch_proxmox_vm_power_start_nonexistent_raises(self):
        self.device = Mock()

        self.device.execute.return_value = (
            "Configuration file 'nodes/cisco/qemu-server/102.conf' does not exist"
        )
        with self.assertRaises(ValueError) as cm:
            switch_proxmox_vm_power(self.device, '102', 'start')

        self.assertIn('does not exist', str(cm.exception))

        self.device.execute.assert_called_once_with("qm start 102")

