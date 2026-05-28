import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagnostic_schedule_switch


class TestUnconfigureDiagnosticScheduleSwitch(unittest.TestCase):

    def test_unconfigure_diagnostic_schedule_switch(self):
        device = Mock()

        result = unconfigure_diagnostic_schedule_switch(
            device, '1', '06:00', None, 'jan', '12', '2023'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             ('no diagnostic schedule switch 1 test all on jan 12 2023 06:00',)
        )