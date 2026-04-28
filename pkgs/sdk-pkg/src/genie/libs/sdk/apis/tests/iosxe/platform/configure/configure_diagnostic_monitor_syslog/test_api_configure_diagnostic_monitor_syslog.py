from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_diagnostic_monitor_syslog


class TestConfigureDiagnosticMonitorSyslog(TestCase):

    def test_configure_diagnostic_monitor_syslog(self):
        device = Mock()
        result = configure_diagnostic_monitor_syslog(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('diagnostic monitor syslog',)
        )