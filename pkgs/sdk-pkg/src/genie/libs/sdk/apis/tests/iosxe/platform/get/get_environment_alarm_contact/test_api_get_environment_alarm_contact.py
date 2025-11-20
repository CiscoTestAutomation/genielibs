import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_environment_alarm_contact
from unittest.mock import Mock


class TestGetEnvironmentAlarmContact(unittest.TestCase):    

    def test_get_environment_alarm_contact(self):
        self.device = Mock()
        self.device.name = 'Switch'
        self.device.parse = Mock(return_value={
            'ALARM CONTACT 1': {
                'status': 'not asserted',
                'description': 'external alarm contact 1',
                'severity': 'minor',
                'trigger': 'closed'
            },
            'ALARM CONTACT 2': {
                'status': 'not asserted',
                'description': 'external alarm contact 2',
                'severity': 'minor',
                'trigger': 'closed'
            }
        })
        result = get_environment_alarm_contact(self.device, 1)
        expected_output = {
            'status': 'not asserted',
            'trigger': 'closed',
            'severity': 'minor'
        }
        self.assertEqual(result, expected_output)
