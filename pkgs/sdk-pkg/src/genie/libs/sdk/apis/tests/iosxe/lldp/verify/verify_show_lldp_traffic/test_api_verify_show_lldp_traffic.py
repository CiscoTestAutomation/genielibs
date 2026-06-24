import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.lldp.verify import verify_show_lldp_traffic


class TestVerifyShowLldpTraffic(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.api.get_lldp_traffic_info.return_value = {
            'frame_out': 20372,
            'entries_aged_out': 34,
            'frame_in': 13315,
            'frame_error_in': 0,
            'frame_discard': 14,
            'tlv_discard': 0,
            'tlv_unknown': 0,
        }

    def test_verify_show_lldp_traffic_in_range(self):
        self.assertTrue(verify_show_lldp_traffic(
            self.device,
            min_frame_in=10000, max_frame_in=20000,
            min_frame_out=10000, max_frame_out=30000))

    def test_verify_show_lldp_traffic_below_min(self):
        self.assertFalse(verify_show_lldp_traffic(
            self.device, min_frame_in=99999))

    def test_verify_show_lldp_traffic_above_max(self):
        self.assertFalse(verify_show_lldp_traffic(
            self.device, max_frame_out=10))

    def test_verify_show_lldp_traffic_no_data(self):
        self.device.api.get_lldp_traffic_info.return_value = None
        self.assertFalse(verify_show_lldp_traffic(
            self.device, min_frame_in=0))


if __name__ == '__main__':
    unittest.main()
