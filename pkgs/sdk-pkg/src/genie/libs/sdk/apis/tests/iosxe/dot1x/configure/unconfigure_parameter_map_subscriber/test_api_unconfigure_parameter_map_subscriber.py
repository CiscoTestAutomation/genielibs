import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    unconfigure_parameter_map_subscriber
)


class TestUnconfigureParameterMapSubscriber(TestCase):

    def test_unconfigure_parameter_map_subscriber(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_parameter_map_subscriber(
            device,
            'BUILTIN_DEVICE_TO_TEMPLATE'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'no parameter-map type subscriber attribute-to-service '
            'BUILTIN_DEVICE_TO_TEMPLATE',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()