import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.verify import verify_alarm_settings
from unittest.mock import Mock

class TestVerifyAlarmSettings(TestCase):
    
    def test_verify_alarm_settings(self):
        self.device = Mock()
        self.device.reload = Mock()
        result = verify_alarm_settings(self.device, 'Positive', 'Disabled', {'hsr': {'alarm': 'Disabled',
         'notifies': 'Disabled',
         'relay': '',
         'syslog': 'Disabled'},
 'input_alarm_1': {'alarm': 'Enabled',
                   'notifies': 'Disabled',
                   'relay': '',
                   'syslog': 'Enabled'},
 'input_alarm_2': {'alarm': 'Enabled',
                   'notifies': 'Disabled',
                   'relay': '',
                   'syslog': 'Enabled'},
 'input_alarm_3': {'alarm': 'Enabled',
                   'notifies': 'Disabled',
                   'relay': '',
                   'syslog': 'Enabled'},
 'input_alarm_4': {'alarm': 'Enabled',
                   'notifies': 'Disabled',
                   'relay': '',
                   'syslog': 'Enabled'},
 'power_supply': {'alarm': 'Enabled',
                  'notifies': 'Disabled',
                  'relay': '',
                  'syslog': 'Enabled'},
 'ptp': {'alarm': 'Disabled',
         'notifies': 'Disabled',
         'relay': '',
         'syslog': 'Disabled'},
 'sd_card': {'alarm': 'Disabled',
             'notifies': 'Disabled',
             'relay': '',
             'syslog': 'Disabled'},
 'temperature_primary': {'alarm': 'Enabled',
                         'notifies': 'Enabled',
                         'relay': 'MAJ',
                         'syslog': 'Enabled',
                         'thresholds': {'max_temp': '80C', 'min_temp': '0C'}},
 'temperature_secondary': {'alarm': 'Disabled',
                           'notifies': 'Disabled',
                           'relay': '',
                           'syslog': 'Disabled'}}, 15, 5)
        expected_output = False
        self.assertEqual(result, expected_output)
