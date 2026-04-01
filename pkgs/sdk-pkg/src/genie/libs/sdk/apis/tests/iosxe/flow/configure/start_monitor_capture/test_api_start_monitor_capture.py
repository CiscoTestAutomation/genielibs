import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.flow.configure import start_monitor_capture


class TestStartMonitorCapture(unittest.TestCase):

    def test_start_monitor_capture(self):
        # Create mock device
        device = Mock()

        # start_monitor_capture typically uses EXEC (device.execute) for this command
        device.execute.return_value = "Started capture point : test"

        # Call the API
        result = start_monitor_capture(device, 'test')

        # Assertions
        self.assertIsNone(result)

        # Verify execute was called and sent the expected CLI
        device.execute.assert_called_once()
        sent_cmd = device.execute.call_args[0][0]
        self.assertIn('monitor capture test start', str(sent_cmd))


if __name__ == '__main__':
    unittest.main()