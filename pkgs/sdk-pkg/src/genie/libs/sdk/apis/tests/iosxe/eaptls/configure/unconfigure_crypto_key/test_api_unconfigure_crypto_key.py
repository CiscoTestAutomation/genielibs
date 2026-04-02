import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eaptls.configure import (
    unconfigure_crypto_key
)


class TestUnconfigureCryptoKey(TestCase):

    def test_unconfigure_crypto_key(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_crypto_key(
            device,
            'SecG-A2-8M9300.cisco.com'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'crypto key zeroize rsa SecG-A2-8M9300.cisco.com',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()