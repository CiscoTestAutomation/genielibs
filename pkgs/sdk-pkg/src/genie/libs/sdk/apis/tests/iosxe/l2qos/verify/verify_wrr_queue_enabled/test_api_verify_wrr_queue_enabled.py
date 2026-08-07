import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.l2qos.verify import (
    verify_wrr_queue_enabled)


class TestVerifyWrrQueueEnabled(unittest.TestCase):

    # parsed output of 'show wrr-queue bandwidth':
    #    wrr-queue bandwidth for Etherswitch NGWIC is:
    #    WRR Queue  :   1   2   3   4   5   6   7   8
    #    Bandwidth  :   1   2   3   6  12  17  25  33
    enabled = {
        'enabled': True,
        'interface_type': 'Etherswitch NGWIC',
        'queues': {
            1: {'bandwidth': 1}, 2: {'bandwidth': 2},
            3: {'bandwidth': 3}, 4: {'bandwidth': 6},
            5: {'bandwidth': 12}, 6: {'bandwidth': 17},
            7: {'bandwidth': 25}, 8: {'bandwidth': 33},
        },
    }

    # parsed output of 'show wrr-queue bandwidth':
    #    wrr-queue bandwidth is disabled
    disabled = {'enabled': False}

    def setUp(self):
        self.device = Mock()

    def test_verify_wrr_queue_enabled_true(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = \
            self.enabled
        self.assertTrue(
            verify_wrr_queue_enabled(self.device, wrr_queue_enabled=True))

    def test_verify_wrr_queue_enabled_false(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = \
            self.disabled
        self.assertTrue(
            verify_wrr_queue_enabled(self.device, wrr_queue_enabled=False))

    def test_verify_wrr_queue_enabled_mismatch(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = \
            self.enabled
        self.assertFalse(
            verify_wrr_queue_enabled(self.device, wrr_queue_enabled=False))

    def test_verify_wrr_queue_enabled_none(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = None
        self.assertFalse(
            verify_wrr_queue_enabled(self.device, wrr_queue_enabled=True))


if __name__ == '__main__':
    unittest.main()
