import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.fips.configure import (
    configure_fips_authorization_key
)


class TestConfigureFipsAuthorizationKey(TestCase):

    def test_configure_fips_authorization_key(self):
        # Create a mock device
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume enable mode

        # Call the API
        result = configure_fips_authorization_key(
            device,
            '12345678901234567890123456789012'
        )

        # API returns None on success
        self.assertIsNone(result)

        # Ensure configure() was called once
        device.configure.assert_called_once()

        # Validate commands sent to device.configure()
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'fips authorization-key 12345678901234567890123456789012',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()