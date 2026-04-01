import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    configure_flow_monitor
)


def _flatten_cmds(cmds):
    flat = []
    for item in cmds:
        if isinstance(item, (list, tuple)):
            flat.extend(_flatten_cmds(item))
        else:
            flat.append(item)
    return flat


class TestConfigureFlowMonitor(TestCase):

    def test_configure_flow_monitor(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_flow_monitor(
            device,
            'm2in1',
            'FNF-EXP',
            'r2in',
            60
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]
        flat_commands = _flatten_cmds(sent_commands)

        self.assertIn('flow monitor m2in1', flat_commands)
        self.assertIn('exporter FNF-EXP', flat_commands)
        self.assertIn('record r2in', flat_commands)
        self.assertIn('cache timeout active 60', flat_commands)
        self.assertIn('cache timeout inactive 60', flat_commands)


if __name__ == '__main__':
    unittest.main()