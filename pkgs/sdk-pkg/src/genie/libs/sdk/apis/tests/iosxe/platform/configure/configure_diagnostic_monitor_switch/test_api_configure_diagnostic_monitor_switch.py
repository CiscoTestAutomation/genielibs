from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_diagnostic_monitor_switch


class TestConfigureDiagnosticMonitorSwitch(TestCase):

    def test_configure_diagnostic_monitor_switch(self):
        device = Mock()
        result = configure_diagnostic_monitor_switch(
            device,
            '2',
            'basic',
            '2'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('diagnostic monitor threshold switch 2 test basic failure count 2',)
        )