from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagnostic_schedule_module_test_all_daily
from unittest.mock import Mock


class TestUnconfigureDiagnosticScheduleModuleTestAllDaily(TestCase):

    def test_unconfigure_diagnostic_schedule_module_test_all_daily(self):
        self.device = Mock()
        result = unconfigure_diagnostic_schedule_module_test_all_daily(self.device, 1, '10:00', 4348, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no diagnostic schedule module 1 test all daily 10:00 cardindex 4348 jobindex 1',)
        )
