import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.interface.configure import configure_crypto


class TestConfigureCrypto(TestCase):

    def test_configure_crypto_default(self):
        """Verify hostname and domain are configured."""
        device = Mock()
        device.name = 'Router1'
        configure_crypto(
            device, hostname='Router1',
            domain='cisco.com', rsa_modulus='2048'
        )
        self.assertEqual(
            device.configure.call_args[0][0],
            [
                'hostname Router1',
                'ip domain name cisco.com',
            ]
        )

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_crypto(
                device, hostname='Router1',
                domain='cisco.com', rsa_modulus='2048'
            )


if __name__ == '__main__':
    unittest.main()
