import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_masked_unmasked_enable_secret_password


class TestConfigureMaskedUnmaskedEnableSecretPassword(TestCase):

    def test_masked_secret_default(self):
        """Verify masked secret command is built correctly with defaults."""
        device = Mock()
        device.name = 'Router1'
        configure_masked_unmasked_enable_secret_password(
            device, password='Cisco123'
        )
        # masked=True by default, so command should contain 'masked-secret'
        call_args = device.configure.call_args
        self.assertIn('masked-secret', call_args[0][0])

    def test_unmasked_secret(self):
        """Verify unmasked secret includes password in command."""
        device = Mock()
        device.name = 'Router1'
        configure_masked_unmasked_enable_secret_password(
            device, password='Cisco123', masked=False, secret=True
        )
        call_args = device.configure.call_args
        self.assertIn('secret', call_args[0][0])
        self.assertIn('Cisco123', call_args[0][0])

    def test_with_privilege_and_algorithm(self):
        """Verify privilege level and algorithm-type in command."""
        device = Mock()
        device.name = 'Router1'
        configure_masked_unmasked_enable_secret_password(
            device, password='Cisco123', privilege=15,
            algorithm_type='scrypt', masked=False
        )
        call_args = device.configure.call_args
        cmd = call_args[0][0]
        self.assertIn('algorithm-type scrypt', cmd)
        self.assertIn('level 15', cmd)

    def test_with_ccp_name(self):
        """Verify common-criteria-policy in command."""
        device = Mock()
        device.name = 'Router1'
        configure_masked_unmasked_enable_secret_password(
            device, password='Cisco123', ccp_name='MY_POLICY', masked=False
        )
        call_args = device.configure.call_args
        self.assertIn('common-criteria-policy MY_POLICY', call_args[0][0])

    def test_invalid_password_empty(self):
        """Verify ValueError for empty password."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_masked_unmasked_enable_secret_password(device, password='')

    def test_invalid_privilege(self):
        """Verify ValueError for privilege out of range."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_masked_unmasked_enable_secret_password(
                device, password='Cisco123', privilege=20
            )

    def test_invalid_algorithm_type(self):
        """Verify ValueError for invalid algorithm_type."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_masked_unmasked_enable_secret_password(
                device, password='Cisco123', algorithm_type='invalid'
            )

    def test_invalid_ccp_name(self):
        """Verify ValueError for ccp_name with special chars."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_masked_unmasked_enable_secret_password(
                device, password='Cisco123', ccp_name='bad;name'
            )

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_masked_unmasked_enable_secret_password(
                device, password='Cisco123'
            )


if __name__ == '__main__':
    unittest.main()
