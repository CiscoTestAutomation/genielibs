from unittest import TestCase
from genie.libs.sdk.apis.linux.execute import get_proxmox_vm_power_state
from unittest.mock import Mock


class TestGetProxmoxVmPowerState(TestCase):

    def test_get_proxmox_vm_power_state_ON(self):
        self.device = Mock()
        self.device.execute.return_value = "status: running"
        result = get_proxmox_vm_power_state(self.device, vm_name="my-vm", vm_id="101")
        self.assertEqual(result, 'ON')
        self.device.execute.assert_called_once_with("qm status 101")
    
    def test_get_proxmox_vm_power_state_OFF(self):
        self.device = Mock()
        self.device.execute.return_value = "status: stopped"
        result = get_proxmox_vm_power_state(self.device, vm_name="my-vm-stby", vm_id="100")
        self.assertEqual(result, 'OFF')
        self.device.execute.assert_called_once_with("qm status 100")