from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_speed_number
from unittest.mock import Mock


class TestUnconfigureInterfaceSpeedNumber(TestCase):

    def test_unconfigure_interface_speed_number(self):
        self.device = Mock()
        result = unconfigure_interface_speed_number(self.device, 'GigabitEthernet2/0/1', '1000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet2/0/1', 'no speed 1000'],)
        )
