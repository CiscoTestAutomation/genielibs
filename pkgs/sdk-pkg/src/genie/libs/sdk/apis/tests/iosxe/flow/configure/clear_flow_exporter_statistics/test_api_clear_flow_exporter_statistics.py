import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    clear_flow_exporter_statistics
)


class TestClearFlowExporterStatistics(TestCase):

    def test_clear_flow_exporter_statistics(self):
        # Create a mock device
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume exec/enable mode

        # Call the API
        result = clear_flow_exporter_statistics(
            device,
            'cisco123'
        )

        # API returns None on success
        self.assertIsNone(result)

        # Ensure execute() was called once (clear commands run in exec mode)
        device.execute.assert_called_once()

        # Validate command sent to device.execute()
        sent_command = device.execute.mock_calls[0].args[0]

        self.assertEqual(
            sent_command,
            'clear flow exporter cisco123 statistics'
        )


if __name__ == '__main__':
    unittest.main()