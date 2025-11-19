from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import detach_alarm_profile_from_interface
from unittest.mock import Mock


class TestDetachAlarmProfileFromInterface(TestCase):

    def test_detach_alarm_profile_from_interface(self):
        self.device = Mock()
        result = detach_alarm_profile_from_interface(self.device, 'Gi1/0/2', 'LinkFaultProfile')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/0/2', 'no alarm-profile LinkFaultProfile'],)
        )
