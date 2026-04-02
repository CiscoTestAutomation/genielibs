import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_fnf_monitor_datalink_interface


class TestUnconfigureFnfMonitorDatalinkInterface(TestCase):

    def test_unconfigure_fnf_monitor_datalink_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_fnf_monitor_datalink_interface(
            device,
            'GigabitEthernet1/0/1',
            'fl_mon_Po'
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

        self.assertIn('interface GigabitEthernet1/0/1', cfg_lines)
        self.assertIn('no datalink flow monitor fl_mon_Po', cfg_lines)


if __name__ == '__main__':
    unittest.main()