import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.configure import unconfigure_service_private_config_encryption


class TestUnconfigureServicePrivateConfigEncryption(TestCase):

    def test_unconfigure_service_private_config_encryption(self):
        device = Mock()
        result = unconfigure_service_private_config_encryption(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no service private-config-encryption'],)
        )


if __name__ == '__main__':
    unittest.main()