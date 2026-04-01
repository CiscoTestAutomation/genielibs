import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    clear_monitor_capture
)


class TestClearMonitorCapture(TestCase):

    def test_clear_monitor_capture(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        # Simulate device response shown in mock data
        device.execute.return_value = 'Capture point does not exist : capture1'

        result = clear_monitor_capture(device, 'capture1')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure execute was called
        device.execute.assert_called_once()

        # Validate command sent to the device
        sent_command = device.execute.mock_calls[0].args[0]
        self.assertEqual(sent_command, 'monitor capture capture1 clear')


if __name__ == '__main__':
    unittest.main()