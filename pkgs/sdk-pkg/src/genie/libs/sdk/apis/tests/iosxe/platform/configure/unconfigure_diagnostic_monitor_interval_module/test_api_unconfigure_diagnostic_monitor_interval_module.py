import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagnostic_monitor_interval_module


class TestUnconfigureDiagnosticMonitorIntervalModule(unittest.TestCase):

    def test_unconfigure_diagnostic_monitor_interval_module(self):
        device = Mock()

        result = unconfigure_diagnostic_monitor_interval_module(
            device, 1, 'TestUnusedPortLoopback', '00:01:00', 0, 0
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no diagnostic monitor interval module 1 test TestUnusedPortLoopback 00:01:00 0 0',)
        )