import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.get import get_alarm_contact_relay_mode
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure


class TestGetAlarmContactRelayMode(TestCase):

    def test_get_alarm_contact_relay_mode(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
            'alarm_relay_mode': 'Positive'
        })

        result = get_alarm_contact_relay_mode(self.device)
        self.assertEqual(result, 'Positive')

    def test_get_alarm_contact_relay_mode_not_found(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={})

        with self.assertRaises(SubCommandFailure) as context:
            get_alarm_contact_relay_mode(self.device)

        self.assertIn("Could not find contact relay mode", str(context.exception))
