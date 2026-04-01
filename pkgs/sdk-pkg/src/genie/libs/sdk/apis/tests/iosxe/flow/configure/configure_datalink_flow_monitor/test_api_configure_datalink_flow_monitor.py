import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    configure_datalink_flow_monitor
)


class TestConfigureDatalinkFlowMonitor(TestCase):

    def test_configure_datalink_flow_monitor(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_datalink_flow_monitor(
            device,
            'Gi3/0/2',
            'm2in1',
            'input'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('interface Gi3/0/2', sent_commands)
        self.assertIn('datalink flow monitor m2in1 input', sent_commands)


if __name__ == '__main__':
    unittest.main()