import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import unconfigure_cdp


class TestUnconfigureCdp(unittest.TestCase):

    def test_unconfigure_cdp(self):
        # Create mock device
        device = Mock()
        
        # Mock the parse method to return interface data with proper structure
        device.parse.return_value = {
            'TenGigabitEthernet1/0/1': {
                'type': 'TenGigabitEthernet',
                'oper_status': 'up',
                'enabled': True,
                'port_channel': {
                    'port_channel_member': False
                }
            },
            'TenGigabitEthernet1/0/2': {
                'type': 'TenGigabitEthernet',
                'oper_status': 'up',
                'enabled': True,
                'port_channel': {
                    'port_channel_member': False
                }
            },
            'GigabitEthernet0/0': {
                'type': 'GigabitEthernet',
                'oper_status': 'up',
                'enabled': True,
                'port_channel': {
                    'port_channel_member': False
                }
            },
            'Vlan1': {
                'type': 'Vlan',
                'oper_status': 'up',
                'enabled': True
            }
        }
        
        # Mock the configure method
        device.configure.return_value = None
        
        # Call the function with None for interface_list and timer=300
        result = unconfigure_cdp(device, None, 300)
        
        # Assertions
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify parse was called with timeout parameter
        device.parse.assert_called_once_with('show interfaces', timeout=300)
        
        # Verify configure was called
        self.assertTrue(device.configure.called, "device.configure was not called")


if __name__ == '__main__':
    unittest.main()