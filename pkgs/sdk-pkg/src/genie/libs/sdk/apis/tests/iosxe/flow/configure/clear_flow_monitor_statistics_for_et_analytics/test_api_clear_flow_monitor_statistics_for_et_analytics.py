import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    clear_flow_monitor_statistics_for_et_analytics
)


class TestClearFlowMonitorStatisticsForEtAnalytics(TestCase):

    def test_clear_flow_monitor_statistics_for_et_analytics(self):
        # Create a mock device
        device = Mock()
        device.state_machine.current_state = 'enable'  # Exec/enable mode

        # Call the API
        result = clear_flow_monitor_statistics_for_et_analytics(device)

        # API returns None on success
        self.assertIsNone(result)

        # Ensure execute() was called once
        device.execute.assert_called_once()

        # Extract commands passed to execute()
        sent_commands = device.execute.mock_calls[0].args[0]

        expected_commands = [
            'clear flow monitor eta-mon cache',
            'clear flow monitor eta-mon statistics',
            'show platform software fed active fnf clear-et-analytics-stats'
        ]

        # Validate full command list (order matters)
        self.assertEqual(sent_commands, expected_commands)


if __name__ == '__main__':
    unittest.main()