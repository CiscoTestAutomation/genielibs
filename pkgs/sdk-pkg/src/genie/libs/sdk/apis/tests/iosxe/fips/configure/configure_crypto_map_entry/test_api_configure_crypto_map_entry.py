import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.fips.configure import (
    configure_crypto_map_entry
)


class TestConfigureCryptoMapEntry(TestCase):

    def test_configure_crypto_map_entry(self):
        # Create a mock device
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume enable mode

        # Call the API
        result = configure_crypto_map_entry(
            device,
            'ikev2-cryptomap',
            '1',
            '172.20.249.12',
            'aes256-sha1',
            'ikev2profile',
            '102',
            'ipsec-isakmp',
            None
        )

        # API returns None on success
        self.assertIsNone(result)

        # Ensure configure() was called once
        device.configure.assert_called_once()

        # Validate commands sent to device.configure()
        sent_commands = device.configure.mock_calls[0].args[0]

        expected_commands = [
            'crypto map ikev2-cryptomap 1 ipsec-isakmp',
            'set peer 172.20.249.12',
            'set transform-set aes256-sha1',
            'set ikev2-profile ikev2profile',
            'match address 102'
        ]

        self.assertEqual(sent_commands, expected_commands)


if __name__ == '__main__':
    unittest.main()