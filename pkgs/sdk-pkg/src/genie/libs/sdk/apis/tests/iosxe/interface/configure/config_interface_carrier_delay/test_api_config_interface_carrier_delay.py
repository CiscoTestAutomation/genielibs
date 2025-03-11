from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import config_interface_carrier_delay
from unittest.mock import Mock


class TestConfigInterfaceCarrierDelay(TestCase):

    def test_config_interface_carrier_delay(self):
        self.device = Mock()
        result = config_interface_carrier_delay(self.device, 'GigabitEthernet1/5', 0, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/5', 'carrier-delay 0'],)
        )
