import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import configure_monitor_capture_export_status


class TestConfigureMonitorCaptureExportStatus(TestCase):

    def test_configure_monitor_capture_export_status(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_monitor_capture_export_status(device, 'mypcap')

        expected_output = None
        self.assertEqual(result, expected_output)

        # This API uses device.execute() (not device.configure())
        device.execute.assert_called_once()

        exec_arg = device.execute.mock_calls[0].args[0]
        self.assertEqual(exec_arg, 'monitor capture mypcap export status')


if __name__ == '__main__':
    unittest.main()