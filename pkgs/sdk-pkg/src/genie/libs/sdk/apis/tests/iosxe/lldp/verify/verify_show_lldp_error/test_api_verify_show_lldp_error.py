import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.lldp.verify import verify_show_lldp_error


class TestVerifyShowLldpError(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.api.get_lldp_error_info.return_value = {
            'memory': 0,
            'encapsulation': 0,
            'input_queue': 0,
            'table': 0,
        }

    def test_verify_show_lldp_error_in_range(self):
        self.assertTrue(verify_show_lldp_error(
            self.device, min_memory=0, max_memory=100,
            min_encapsulation=0, max_encapsulation=100))

    def test_verify_show_lldp_error_above_max(self):
        self.device.api.get_lldp_error_info.return_value = {
            'memory': 50,
        }
        self.assertFalse(verify_show_lldp_error(
            self.device, max_memory=10))

    def test_verify_show_lldp_error_below_min(self):
        self.device.api.get_lldp_error_info.return_value = {
            'memory': 0,
        }
        self.assertFalse(verify_show_lldp_error(
            self.device, min_memory=10))

    def test_verify_show_lldp_error_no_data(self):
        self.device.api.get_lldp_error_info.return_value = None
        self.assertFalse(verify_show_lldp_error(
            self.device, min_memory=0))


if __name__ == '__main__':
    unittest.main()
