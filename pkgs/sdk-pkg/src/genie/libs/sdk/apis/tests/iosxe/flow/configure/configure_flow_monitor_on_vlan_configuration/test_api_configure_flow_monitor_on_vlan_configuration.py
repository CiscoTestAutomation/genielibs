import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    configure_flow_monitor_on_vlan_configuration
)


class TestConfigureFlowMonitorOnVlanConfiguration(TestCase):

    def test_configure_flow_monitor_on_vlan_configuration(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_flow_monitor_on_vlan_configuration(
            device,
            '10',
            'data-mon',
            'input',
            'samper1',
            'datalink'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('vlan configuration 10', sent_commands)
        self.assertIn(
            'datalink flow monitor data-mon sampler samper1 input',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()