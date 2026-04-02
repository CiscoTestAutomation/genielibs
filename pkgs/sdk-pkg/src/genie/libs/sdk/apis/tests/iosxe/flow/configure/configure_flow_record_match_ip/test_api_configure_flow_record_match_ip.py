import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_record_match_ip


class TestConfigureFlowRecordMatchIp(TestCase):

    def test_configure_flow_record_match_ip(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_flow_record_match_ip(
            device,
            'r2out',
            'ipv6',
            'source',
            True
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

        self.assertIn('flow record r2out', cfg_lines)
        self.assertIn('match ipv6 source address', cfg_lines)


if __name__ == '__main__':
    unittest.main()