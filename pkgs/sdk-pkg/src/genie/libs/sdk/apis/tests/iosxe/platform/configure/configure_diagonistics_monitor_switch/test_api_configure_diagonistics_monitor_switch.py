from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_diagonistics_monitor_switch


class TestConfigureDiagonisticsMonitorSwitch(TestCase):

    def test_configure_diagonistics_monitor_switch(self):
        device = Mock()
        result = configure_diagonistics_monitor_switch(
            device,
            1,
            'DiagThermalTest',
            '00:03:00',
            20,
            1
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('diagnostic monitor interval switch 1 test DiagThermalTest 00:03:00 20 1',)
        )