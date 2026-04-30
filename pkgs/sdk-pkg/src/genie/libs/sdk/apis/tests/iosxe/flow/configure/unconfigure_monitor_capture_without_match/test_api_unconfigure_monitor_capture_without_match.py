import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_monitor_capture_without_match


class TestUnconfigureMonitorCaptureWithoutMatch(TestCase):

    def test_unconfigure_monitor_capture_without_match(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_monitor_capture_without_match(
            device,
            'REL',
            'both',
            'TwentyFiveGigE1/0/5'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # This API uses device.execute() (not device.configure())
        device.execute.assert_called_once()

        exec_arg = device.execute.mock_calls[0].args[0]
        self.assertEqual(exec_arg, 'no monitor capture REL interface TwentyFiveGigE1/0/5 both')


if __name__ == '__main__':
    unittest.main()