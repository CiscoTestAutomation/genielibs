import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.get import get_alarm_max_min_temp
from unittest.mock import Mock


class TestGetAlarmMaxMinTemp(TestCase):
    
    def test_get_alarm_max_min_temp(self):
        self.device = Mock()
        self.device.parse = Mock(return_value={
            'temperature_primary': {
                'threshold': {
                    'max_temp': 45,
                    'min_temp': 5
                }
            }
        })
        result = get_alarm_max_min_temp(self.device)
        expected_output = [45, 5]
        self.assertEqual(result, expected_output)
        self.device.parse.assert_called_with('show alarm settings')
