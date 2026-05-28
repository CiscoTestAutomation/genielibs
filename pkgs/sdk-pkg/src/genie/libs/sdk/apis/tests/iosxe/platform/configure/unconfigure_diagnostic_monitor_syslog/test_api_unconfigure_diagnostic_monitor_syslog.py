import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagnostic_monitor_syslog


class TestUnconfigureDiagnosticMonitorSyslog(unittest.TestCase):

    def test_unconfigure_diagnostic_monitor_syslog(self):
        device = Mock()

        result = unconfigure_diagnostic_monitor_syslog(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no diagnostic monitor syslog',)
        )