from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import attach_alarm_profile_to_interface
from unittest.mock import Mock


class TestAttachAlarmProfileToInterface(TestCase):

    def test_attach_alarm_profile_to_interface(self):
        self.device = Mock()
        result = attach_alarm_profile_to_interface(self.device, 'Gi1/0/2', 'LinkFaultProfile')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/0/2', 'alarm-profile LinkFaultProfile'],)
        )
