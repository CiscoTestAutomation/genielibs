import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.lldp.verify import verify_show_lldp_interface


class TestVerifyShowLldpInterface(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_verify_show_lldp_interface_match(self):
        self.device.api.get_lldp_interface_info.return_value = {
            'interfaces': {
                'GigabitEthernet1/0/15': {
                    'tx': 'enabled',
                    'rx': 'enabled',
                    'tx_state': 'idle',
                    'rx_state': 'wait for frame',
                },
            },
        }
        self.assertTrue(verify_show_lldp_interface(
            self.device, 'GigabitEthernet1/0/15',
            tx='enabled', rx='enabled',
            tx_state='idle', rx_state='wait for frame'))

    def test_verify_show_lldp_interface_mismatch(self):
        self.device.api.get_lldp_interface_info.return_value = {
            'interfaces': {
                'GigabitEthernet1/0/15': {
                    'tx': 'enabled',
                    'rx': 'enabled',
                },
            },
        }
        self.assertFalse(verify_show_lldp_interface(
            self.device, 'GigabitEthernet1/0/15', tx='disabled'))

    def test_verify_show_lldp_interface_no_data(self):
        self.device.api.get_lldp_interface_info.return_value = None
        self.assertFalse(verify_show_lldp_interface(
            self.device, 'GigabitEthernet1/0/15', tx='enabled'))


if __name__ == '__main__':
    unittest.main()
