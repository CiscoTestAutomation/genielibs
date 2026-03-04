import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_class_map_type_match_none
)


class TestConfigureClassMapTypeMatchNone(TestCase):

    def test_configure_class_map_type_match_none(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_class_map_type_match_none(
            device,
            'NOT_IN_CRITICAL_AUTH',
            'DefaultCriticalVoice_SRV_TEMPLATE'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'class-map type control subscriber match-none NOT_IN_CRITICAL_AUTH',
            sent_commands
        )
        self.assertIn(
            'match activated-service-template DefaultCriticalVoice_SRV_TEMPLATE',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()