import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    configure_queue_sub_interface
)


class TestConfigureQueueSubInterface(unittest.TestCase):

    def test_configure_queue_sub_interface(self):
        device = Mock()

        result = configure_queue_sub_interface(
            device,
            'hundredGigE 1/0/1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface hundredGigE 1/0/1',
              'no switchport',
              'queuing mode sub-interface priority-propagation'],)
        )