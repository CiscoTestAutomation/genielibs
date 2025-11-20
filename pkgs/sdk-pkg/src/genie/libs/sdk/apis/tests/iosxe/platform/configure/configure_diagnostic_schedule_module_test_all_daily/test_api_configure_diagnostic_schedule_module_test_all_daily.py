from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_diagnostic_schedule_module_test_all_daily
from unittest.mock import Mock


class TestConfigureDiagnosticScheduleModuleTestAllDaily(TestCase):

    def test_configure_diagnostic_schedule_module_test_all_daily(self):
        self.device = Mock()
        result = configure_diagnostic_schedule_module_test_all_daily(self.device, 1, '10:00', 4348, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('diagnostic schedule module 1 test all daily 10:00 cardindex 4348 jobindex 1',)
        )
