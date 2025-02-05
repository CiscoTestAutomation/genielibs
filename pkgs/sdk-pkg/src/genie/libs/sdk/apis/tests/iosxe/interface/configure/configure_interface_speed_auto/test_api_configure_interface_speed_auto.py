from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_speed_auto
from unittest.mock import Mock


class TestConfigureInterfaceSpeedAuto(TestCase):

    def test_configure_interface_speed_auto(self):
        self.device = Mock()
        result = configure_interface_speed_auto(self.device, 'TenGigabitEthernet1/0/6', '10 100 1000 2500 5000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet1/0/6', 'speed auto 10 100 1000 2500 5000'],)
        )
