from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.interface.get import get_interface_ip_address


class TestGetInterfaceIpAddress(TestCase):

    def test_get_interface_ip_address(self):
        self.device = Mock()
        self.device.name = 'router1'
        self.device.parse.return_value = {
            'interface': {
                'GigabitEthernet0/2': {
                    'ip_address': '11.11.11.14',
                    'interface_is_ok': 'YES',
                    'method': 'DHCP',
                    'status': 'up',
                    'protocol': 'up',
                }
            }
        }
        result = get_interface_ip_address(
            self.device, 'GigabitEthernet0/2')
        self.assertEqual(result, '11.11.11.14')
        self.device.parse.assert_called_once_with(
            'show ip interface brief GigabitEthernet0/2')

    def test_get_interface_ip_address_unassigned(self):
        self.device = Mock()
        self.device.name = 'router1'
        self.device.parse.return_value = {
            'interface': {
                'GigabitEthernet0/1': {
                    'ip_address': 'unassigned',
                }
            }
        }
        result = get_interface_ip_address(
            self.device, 'GigabitEthernet0/1')
        self.assertIsNone(result)

    def test_get_interface_ip_address_failure(self):
        self.device = Mock()
        self.device.name = 'router1'
        self.device.parse.side_effect = SubCommandFailure('error')
        result = get_interface_ip_address(
            self.device, 'GigabitEthernet0/2')
        self.assertIsNone(result)
