import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.lldp.verify import verify_show_lldp


class TestVerifyShowLldp(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_verify_show_lldp_match(self):
        self.device.api.get_lldp_info.return_value = {
            'hello_timer': 30,
            'hold_timer': 120,
            'reinit_timer': 2,
            'status': 'active',
        }
        self.assertTrue(verify_show_lldp(
            self.device, hello_timer=30, hold_timer=120,
            reinit_timer=2, status='active'))

    def test_verify_show_lldp_mismatch(self):
        self.device.api.get_lldp_info.return_value = {
            'hello_timer': 30,
            'hold_timer': 120,
            'reinit_timer': 2,
            'status': 'active',
        }
        self.assertFalse(verify_show_lldp(self.device, hello_timer=99))

    def test_verify_show_lldp_inactive_when_no_data(self):
        self.device.api.get_lldp_info.return_value = None
        self.assertTrue(verify_show_lldp(self.device, status='inactive'))

    def test_verify_show_lldp_active_but_no_data(self):
        self.device.api.get_lldp_info.return_value = None
        self.assertFalse(verify_show_lldp(self.device, status='active'))


if __name__ == '__main__':
    unittest.main()
