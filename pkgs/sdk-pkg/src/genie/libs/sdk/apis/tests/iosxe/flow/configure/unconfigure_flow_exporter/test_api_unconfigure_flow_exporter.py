import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_flow_exporter


class TestUnconfigureFlowExporter(TestCase):

    def test_unconfigure_flow_exporter(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_flow_exporter(
            device,
            'test',
            '1.1.1.1',
            '2',
            '23',
            '3',
            '1200',
            None,
            'ipfix'
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

        self.assertIn('flow exporter test', cfg_lines)
        self.assertIn('no destination 1.1.1.1', cfg_lines)
        self.assertIn('no transport udp 2', cfg_lines)
        self.assertIn('no dscp 23', cfg_lines)
        self.assertIn('no ttl 3', cfg_lines)
        self.assertIn('no template data timeout 1200', cfg_lines)
        self.assertIn('no export-protocol ipfix', cfg_lines)


if __name__ == '__main__':
    unittest.main()