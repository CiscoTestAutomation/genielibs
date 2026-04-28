from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_diagnostic_schedule_module


class TestConfigureDiagnosticScheduleModule(TestCase):

    def test_configure_diagnostic_schedule_module(self):
        device = Mock()
        result = configure_diagnostic_schedule_module(
            device,
            2,
            '1:00',
            None,
            None,
            None,
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('diagnostic schedule module 2 test all daily 1:00',)
        )