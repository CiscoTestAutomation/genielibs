import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.l2qos.verify import (
    verify_wrr_queue_cos_map)


class TestVerifyWrrQueueCosMap(unittest.TestCase):

    # parsed output of 'show wrr-queue cos-map':
    #    wrr-queue cos map for Etherswitch NGWIC is
    #    CoS Value      :  0  1  2  3  4  5  6  7
    #    Priority Queue :  1  5  3  4  5  6  7  8
    cos_map = {
        'interface_type': 'Etherswitch NGWIC',
        'cos_map': {
            0: {'priority_queue': 1},
            1: {'priority_queue': 5},
            2: {'priority_queue': 3},
            3: {'priority_queue': 4},
            4: {'priority_queue': 5},
            5: {'priority_queue': 6},
            6: {'priority_queue': 7},
            7: {'priority_queue': 8},
        },
    }

    def setUp(self):
        self.device = Mock()

    def test_verify_wrr_queue_cos_map(self):
        self.device.api.get_show_wrr_queue_cos_map.return_value = \
            self.cos_map
        self.assertTrue(
            verify_wrr_queue_cos_map(self.device, 1, 5))

    def test_verify_wrr_queue_cos_map_mismatch(self):
        self.device.api.get_show_wrr_queue_cos_map.return_value = \
            self.cos_map
        self.assertFalse(
            verify_wrr_queue_cos_map(self.device, 1, 8))

    def test_verify_wrr_queue_cos_map_none(self):
        self.device.api.get_show_wrr_queue_cos_map.return_value = None
        self.assertFalse(
            verify_wrr_queue_cos_map(self.device, 1, 5))


if __name__ == '__main__':
    unittest.main()
