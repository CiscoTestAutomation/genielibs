import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagonistics_monitor_switch


class TestUnconfigureDiagonisticsMonitorSwitch(unittest.TestCase):

    def test_unconfigure_diagonistics_monitor_switch(self):
        device = Mock()

        result = unconfigure_diagonistics_monitor_switch(
            device, 1, 'DiagThermalTest', '00:03:00', 20, 1
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no diagnostic monitor interval switch 1 test DiagThermalTest 00:03:00 20 1',)
        )