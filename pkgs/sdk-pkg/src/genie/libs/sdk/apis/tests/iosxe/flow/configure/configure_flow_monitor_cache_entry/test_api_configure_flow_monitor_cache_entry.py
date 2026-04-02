import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    configure_flow_monitor_cache_entry
)


class TestConfigureFlowMonitorCacheEntry(TestCase):

    def test_configure_flow_monitor_cache_entry(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_flow_monitor_cache_entry(
            device,
            'dnacmonitor',
            'dnacrecord',
            10,
            None,
            'dnacexporter'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('flow monitor dnacmonitor', sent_commands)
        self.assertIn('record dnacrecord', sent_commands)
        self.assertIn('exporter dnacexporter', sent_commands)
        self.assertIn('cache timeout active 10', sent_commands)
        self.assertIn('cache timeout inactive 10', sent_commands)


if __name__ == '__main__':
    unittest.main()