import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import configure_fnf_record


class TestConfigureFnfRecord(TestCase):

    def test_configure_fnf_record(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_fnf_record(
            device, 'flow_Po',
            'protocol', None, None,
            'tos',
            'destination-port',
            'source-port',
            True, True,
            None,
            False, False,
            None, None, None, None, None,
            False
        )

        self.assertIsNone(result)

        # API calls configure() twice
        self.assertEqual(device.configure.call_count, 2)

        # Merge config from both calls
        all_lines = []
        for call in device.configure.mock_calls:
            cfg_arg = call.args[0]
            if isinstance(cfg_arg, str):
                all_lines.extend([line.strip() for line in cfg_arg.splitlines() if line.strip()])
            else:
                all_lines.extend(list(cfg_arg))

        # Core record
        self.assertIn('flow record flow_Po', all_lines)

        # Match lines
        self.assertIn('match ipv4 tos', all_lines)
        self.assertIn('match ipv4 destination address', all_lines)
        self.assertIn('match ipv4 protocol', all_lines)
        self.assertIn('match ipv4 source address', all_lines)
        self.assertIn('match routing vrf input', all_lines)
        self.assertIn('match transport destination-port', all_lines)
        self.assertIn('match transport source-port', all_lines)

        # Collect lines
        self.assertIn('collect counter bytes long', all_lines)
        self.assertIn('collect counter packets long', all_lines)
        self.assertIn('collect transport tcp flags', all_lines)


if __name__ == '__main__':
    unittest.main()