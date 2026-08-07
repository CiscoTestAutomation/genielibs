from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.hw_module.verify import (
    verify_platform_hardware_subslot_module_interface_status_mac_learning,
)


class TestVerifyMacLearning(TestCase):

    def test_verify_mac_learning(self):
        self.device = Mock()
        parsed = {
            'l2_network': {
                'link': 'down',
                'link_config': 'disabled',
                'speed': 'unknown',
                'speed_config': 'unknown',
                'duplex': 'unknown',
                'duplex_config': 'unknown',
                'nego_config': 'unknown',
                'mtu': 1522,
                'rx_pause': 'off',
                'rx_pause_config': 'off',
                'tx_pause': 'off',
                'tx_pause_config': 'off',
            },
            'vlan_mode': 'access',
            'native_vlan': 1,
            'mac_learning': {
                'learning_mode': 'auto learning',
            },
        }
        self.device.api.\
            get_platform_hardware_subslot_module_interface_status = Mock(
                return_value=parsed)
        result = \
            verify_platform_hardware_subslot_module_interface_status_mac_learning(
                self.device, '0/1', 'GigabitEthernet0/1/0', 'auto learning')
        self.assertEqual(result, True)
        self.device.api.\
            get_platform_hardware_subslot_module_interface_status.\
            assert_called_with(
                subslot='0/1', interface='GigabitEthernet0/1/0')

    def test_verify_mac_learning_mismatch(self):
        self.device = Mock()
        parsed = {
            'vlan_mode': 'access',
            'native_vlan': 1,
            'mac_learning': {
                'learning_mode': 'auto learning',
            },
        }
        self.device.api.\
            get_platform_hardware_subslot_module_interface_status = Mock(
                return_value=parsed)
        result = \
            verify_platform_hardware_subslot_module_interface_status_mac_learning(
                self.device, '0/1', 'GigabitEthernet0/1/0', 'no learning')
        self.assertEqual(result, False)

    def test_verify_mac_learning_none(self):
        self.device = Mock()
        self.device.api.\
            get_platform_hardware_subslot_module_interface_status = Mock(
                return_value=None)
        result = \
            verify_platform_hardware_subslot_module_interface_status_mac_learning(
                self.device, '0/1', 'GigabitEthernet0/1/0', 'auto learning')
        self.assertEqual(result, False)
