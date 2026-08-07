import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.l2qos.get import (
    get_l2qos_max_queue_number)


class TestGetL2qosMaxQueueNumber(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_max_queue_number_8(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = {
            'enabled': True,
            'interface_type': 'Etherswitch NGWIC',
            'queues': {
                1: {'bandwidth': 1}, 2: {'bandwidth': 2},
                3: {'bandwidth': 3}, 4: {'bandwidth': 6},
                5: {'bandwidth': 12}, 6: {'bandwidth': 17},
                7: {'bandwidth': 25}, 8: {'bandwidth': 33},
            },
        }
        result = get_l2qos_max_queue_number(self.device)
        self.assertEqual(result, 8)

    def test_max_queue_number_4(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = {
            'enabled': True,
            'interface_type': 'Etherswitch NGWIC',
            'queues': {
                1: {'bandwidth': 1}, 2: {'bandwidth': 2},
                3: {'bandwidth': 3}, 4: {'bandwidth': 6},
            },
        }
        result = get_l2qos_max_queue_number(self.device)
        self.assertEqual(result, 4)

    def test_max_queue_number_disabled(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = {
            'enabled': False,
        }
        result = get_l2qos_max_queue_number(self.device)
        self.assertEqual(result, 0)

    def test_max_queue_number_empty(self):
        self.device.api.get_show_wrr_queue_bandwidth.return_value = None
        result = get_l2qos_max_queue_number(self.device)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
