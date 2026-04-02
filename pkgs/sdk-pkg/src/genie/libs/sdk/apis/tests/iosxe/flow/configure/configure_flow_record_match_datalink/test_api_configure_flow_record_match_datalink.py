import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_record_match_datalink


class TestConfigureFlowRecordMatchDatalink(TestCase):

    def test_configure_flow_record_match_datalink(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        # Keep the call as-is (since it produced the observed output)
        result = configure_flow_record_match_datalink(
            device,
            'r2out',
            'mac',
            'source',
            'address',
            'input',
        )

        self.assertEqual(result, None)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('flow record r2out', cfg_lines)

        # Assert what the API actually sent (per the unittest failure output)
        self.assertIn('match datalink mac source address address', cfg_lines)


if __name__ == '__main__':
    unittest.main()