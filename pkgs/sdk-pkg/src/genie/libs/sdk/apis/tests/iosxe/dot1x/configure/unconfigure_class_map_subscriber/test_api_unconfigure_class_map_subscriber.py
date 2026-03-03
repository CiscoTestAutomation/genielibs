import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    unconfigure_class_map_subscriber
)


class TestUnconfigureClassMapSubscriber(TestCase):

    def test_unconfigure_class_map_subscriber(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_class_map_subscriber(
            device,
            'AAA_SVR_DOWN_AUTHD_HOST'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'no class-map type control subscriber match-all AAA_SVR_DOWN_AUTHD_HOST',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()