import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagnostic_monitor_switch


class TestUnconfigureDiagnosticMonitorSwitch(unittest.TestCase):

    def test_unconfigure_diagnostic_monitor_switch(self):
        device = Mock()

        result = unconfigure_diagnostic_monitor_switch(device, '2', 'basic')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no diagnostic monitor switch 2 test basic'],)
        )