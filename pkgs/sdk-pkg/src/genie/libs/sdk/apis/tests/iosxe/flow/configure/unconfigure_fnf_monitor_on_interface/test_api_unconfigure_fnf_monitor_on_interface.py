import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_fnf_monitor_on_interface


class TestUnconfigureFnfMonitorOnInterface(TestCase):

    def test_unconfigure_fnf_monitor_on_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_fnf_monitor_on_interface(
            device,
            'GigabitEthernet2/0/3',
            'FlowMonitor-1',
            sampler_name=None,
            direction='input'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions (API may pass list or multiline string)
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('interface GigabitEthernet2/0/3', cfg_lines)
        self.assertIn('no ip flow monitor FlowMonitor-1 input', cfg_lines)


if __name__ == '__main__':
    unittest.main()