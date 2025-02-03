from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_speed_auto
from unittest.mock import Mock


class TestUnconfigureInterfaceSpeedAuto(TestCase):

    def test_unconfigure_interface_speed_auto(self):
        self.device = Mock()
        result = unconfigure_interface_speed_auto(self.device, 'TenGigabitEthernet1/0/6', '10 100 1000 2500 5000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet1/0/6', 'no speed auto 10 100 1000 2500 5000'],)
        )
