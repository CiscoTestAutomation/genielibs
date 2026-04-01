import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import disable_et_analytics


class TestDisableEtAnalytics(TestCase):

    def test_disable_et_analytics(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = disable_et_analytics(
            device,
            'GigabitEthernet1/0/35'
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

        self.assertIn('interface GigabitEthernet1/0/35', cfg_lines)
        self.assertIn('no et-analytics enable', cfg_lines)


if __name__ == '__main__':
    unittest.main()