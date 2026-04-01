import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_active_timer_under_et_analytics


class TestUnconfigureActiveTimerUnderEtAnalytics(TestCase):

    def test_unconfigure_active_timer_under_et_analytics(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_active_timer_under_et_analytics(
            device,
            '60'
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

        self.assertIn('et-analytics', cfg_lines)
        self.assertIn('no active-timeout 60', cfg_lines)


if __name__ == '__main__':
    unittest.main()