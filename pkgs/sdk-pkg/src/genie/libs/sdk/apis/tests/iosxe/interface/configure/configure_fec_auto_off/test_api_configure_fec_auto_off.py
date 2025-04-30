from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_fec_auto_off
from unittest.mock import Mock


class TestConfigureFecAutoOff(TestCase):

    def test_configure_fec_auto_off(self):
        self.device = Mock()
        result = configure_fec_auto_off(self.device, 'TenGigabitEthernet1/2', 'off')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet1/2', 'fec off'],)
        )
