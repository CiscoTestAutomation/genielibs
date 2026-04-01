import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    configure_flow_exporter
)


class TestConfigureFlowExporter(TestCase):

    def test_configure_flow_exporter(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_flow_exporter(
            device,
            'dnacexporter',
            None, None, None, None, None, None, None,
            'GigabitEthernet3/0/15'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('flow exporter dnacexporter', sent_commands)
        self.assertIn('source GigabitEthernet3/0/15', sent_commands)


if __name__ == '__main__':
    unittest.main()