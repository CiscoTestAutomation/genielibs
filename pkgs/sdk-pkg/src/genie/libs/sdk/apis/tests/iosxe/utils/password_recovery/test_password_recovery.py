import unittest
from unittest.mock import MagicMock, patch
from genie.libs.sdk.apis.iosxe.utils import password_recovery

class TestPasswordRecovery(unittest.TestCase):

    def setUp(self):
        # Mock the device object and its methods
        self.device = MagicMock()
        self.device.is_ha = False
        self.device.name = 'TestDevice'
        self.device.api.execute_power_cycle_device = MagicMock()
        self.device.api.send_break_boot = MagicMock()
        self.device.execute = MagicMock()
        self.device.enable = MagicMock()
        self.device.api.configure_management_credentials = MagicMock()
        self.device.configure = MagicMock()
        self.device.api.execute_write_memory = MagicMock()
        self.device.api.configure_ignore_startup_config.return_value = None
        self.device.api.unconfigure_ignore_startup_config.return_value = None
        self.device.api.verify_ignore_startup_config.return_value = True


    def test_password_recovery_success(self):

        # Test the password recovery process with expected behavior
        password_recovery(self.device)
        # Verify that all steps were called
        self.device.api.execute_power_cycle_device.assert_called_once()
        self.device.api.send_break_boot.assert_called_once()
        self.device.enable.assert_called_once()
        self.device.api.configure_management_credentials.assert_called_once()
        self.device.api.execute_write_memory.assert_called_once()
        self.device.api.configure_ignore_startup_config.assert_called_once()
        self.device.api.unconfigure_ignore_startup_config.assert_called_once()
        self.device.api.verify_ignore_startup_config.assert_called_once()


    def test_password_recovery_failure(self):
        # Mock the device API methods to simulate a failure in verify_ignore_startup_config
        self.device.api.verify_ignore_startup_config.return_value = False

        with self.assertRaises(Exception) as context:
            password_recovery(self.device)

        # Verify that all steps were called up to the failure point
        self.device.api.execute_power_cycle_device.assert_called_once()
        self.device.api.send_break_boot.assert_called_once()
        self.device.api.configure_ignore_startup_config.assert_called_once()
        self.device.enable.assert_called_once()
        self.device.api.configure_management_credentials.assert_called_once()
        self.device.api.unconfigure_ignore_startup_config.assert_called_once()
        self.device.api.verify_ignore_startup_config.assert_called_once()
        self.device.api.execute_write_memory.assert_not_called()

    def test_password_recovery_ha(self):

        # Test the password recovery process with expected behavior
        self.device.is_ha = True
        password_recovery(self.device)
        # Verify that all steps were called
        self.device.api.execute_power_cycle_device.assert_called_once()
        self.device.api.send_break_boot.assert_called_once()
        self.device.connection_provider.designate_handles.assert_called_once()
        self.device.api.configure_management_credentials.assert_called_once()
        self.device.api.execute_write_memory.assert_called_once()
        self.device.api.configure_ignore_startup_config.assert_called_once()
        self.device.api.unconfigure_ignore_startup_config.assert_called_once()
        self.device.api.verify_ignore_startup_config.assert_called_once()