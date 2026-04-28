import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.fnf_sampler.configure import (
    configure_flow_monitor_sampler_fnf_sampler,
)


class TestConfigureFlowMonitorSamplerFnfSampler(TestCase):

    def test_configure_flow_monitor_sampler_fnf_sampler(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_flow_monitor_sampler_fnf_sampler(
            device,
            'ip',
            'm4in',
            'input',
            'GigabitEthernet1/0/13',
            None
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

        self.assertIn('interface GigabitEthernet1/0/13', cfg_lines)
        self.assertIn('ip flow monitor m4in sampler fnf_sampler input', cfg_lines)


if __name__ == '__main__':
    unittest.main()