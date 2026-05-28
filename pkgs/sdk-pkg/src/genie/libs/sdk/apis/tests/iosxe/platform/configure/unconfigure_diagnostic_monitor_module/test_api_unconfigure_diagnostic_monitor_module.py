import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagnostic_monitor_module


class TestUnconfigureDiagnosticMonitorModule(unittest.TestCase):

    def test_unconfigure_diagnostic_monitor_module(self):
        device = Mock()

        result = unconfigure_diagnostic_monitor_module(
            device, 2, 'TestUnusedPortLoopback', None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no diagnostic monitor module 2 test TestUnusedPortLoopback',)
        )