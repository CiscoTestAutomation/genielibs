import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hardware.get import get_hardware_led_status
from unittest.mock import Mock


class TestGetHardwareLedStatus(TestCase):
    
    def test_get_hardware_led_status(self):
        self.device = Mock()
        self.device.reload = Mock()
        self.device.parse = Mock(return_value={
            'alarm-in1': 'GREEN',
            'alarm-in2': 'RED',
            'alarm-out': 'GREEN'
        })
        result = get_hardware_led_status(self.device, 1, True)
        expected_output = ('GREEN', 'GREEN')
        self.assertEqual(result, expected_output)
        self.device.parse.assert_called_with('show hardware led')
        