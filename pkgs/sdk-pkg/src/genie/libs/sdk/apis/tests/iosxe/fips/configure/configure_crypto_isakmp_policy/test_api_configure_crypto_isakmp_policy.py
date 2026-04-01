import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.fips.configure import (
    configure_crypto_isakmp_policy
)


class TestConfigureCryptoIsakmpPolicy(TestCase):

    def test_configure_crypto_isakmp_policy(self):
        # Create a mock device
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        # Call the API
        result = configure_crypto_isakmp_policy(
            device,
            '1',
            'aes',
            'sha',
            'pre-share',
            '14',
            '86400'
        )

        # Validate return value
        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure() was called once
        device.configure.assert_called_once()

        # Extract the commands sent to device.configure()
        sent_commands = device.configure.mock_calls[0].args[0]

        # Validate individual configuration commands
        self.assertIn('crypto isakmp policy 1', sent_commands)
        self.assertIn('encryption aes', sent_commands)
        self.assertIn('hash sha', sent_commands)
        self.assertIn('authentication pre-share', sent_commands)
        self.assertIn('group 14', sent_commands)
        self.assertIn('lifetime 86400', sent_commands)


if __name__ == '__main__':
    unittest.main()