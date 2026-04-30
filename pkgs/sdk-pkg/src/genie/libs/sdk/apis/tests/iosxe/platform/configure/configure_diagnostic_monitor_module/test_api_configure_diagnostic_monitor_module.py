from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_diagnostic_monitor_module


class TestConfigureDiagnosticMonitorModule(TestCase):

    def test_configure_diagnostic_monitor_module(self):
        device = Mock()
        result = configure_diagnostic_monitor_module(
            device,
            2,
            'TestUnusedPortLoopback',
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('diagnostic monitor module 2 test TestUnusedPortLoopback',)
        )