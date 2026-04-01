import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    configure_active_timer_under_et_analytics
)


class TestConfigureActiveTimerUnderEtAnalytics(TestCase):

    def test_configure_active_timer_under_et_analytics(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_active_timer_under_et_analytics(device, '60')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('et-analytics', sent_commands)
        self.assertIn('active-timeout 60', sent_commands)


if __name__ == '__main__':
    unittest.main()