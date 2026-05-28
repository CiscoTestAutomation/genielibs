import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagnostic_schedule_module


class TestUnconfigureDiagnosticScheduleModule(unittest.TestCase):

    def test_unconfigure_diagnostic_schedule_module(self):
        device = Mock()

        result = unconfigure_diagnostic_schedule_module(
            device, 2, '1:00', None, None, None, None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no diagnostic schedule module 2 test all daily 1:00',)
        )