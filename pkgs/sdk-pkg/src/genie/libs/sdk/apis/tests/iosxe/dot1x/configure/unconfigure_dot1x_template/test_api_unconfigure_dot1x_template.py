import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    unconfigure_dot1x_template
)


class TestUnconfigureDot1xTemplate(TestCase):

    def test_unconfigure_dot1x_template(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_dot1x_template(
            device,
            'Identity'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'no template Identity',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()