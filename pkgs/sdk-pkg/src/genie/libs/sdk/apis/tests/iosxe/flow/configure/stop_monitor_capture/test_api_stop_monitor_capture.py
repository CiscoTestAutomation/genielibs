import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import start_monitor_capture


class TestStartMonitorCapture(TestCase):

    def test_start_monitor_capture(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = start_monitor_capture(device, 'test')

        expected_output = None
        self.assertEqual(result, expected_output)

        # This API uses device.execute() (not device.configure())
        device.execute.assert_called_once()

        exec_arg = device.execute.mock_calls[0].args[0]
        self.assertEqual(exec_arg, 'monitor capture test start')


if __name__ == '__main__':
    unittest.main()