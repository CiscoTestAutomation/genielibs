from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_gnmi
from unittest.mock import Mock, patch, MagicMock


class TestConfigureManagementGnmi(TestCase):

    @patch('genie.libs.sdk.apis.iosxe.management.configure.loader')
    @patch('genie.libs.sdk.apis.iosxe.management.configure.tempfile.TemporaryDirectory')
    @patch('genie.libs.sdk.apis.iosxe.management.configure.atexit')
    @patch('genie.libs.sdk.apis.iosxe.management.configure.uuid')
    def test_configure_management_gnmi(self, mock_uuid, mock_atexit, mock_tempdir, mock_loader):
        # Mock device
        self.device = Mock()
        self.device.name = 'Switch'
        self.device.connections.gnmi.update = Mock()
        self.device.api.configure_gnxi = Mock()
        self.device.api.copy_to_device = Mock()
        self.device.api.configure_pki_import = Mock()
        self.device.api.configure_trustpoint = Mock()
        
        # Mock linux device for SSL operations
        mock_linux_dev = MagicMock()
        mock_linux_dev.api.generate_rsa_ssl_key = Mock()
        mock_linux_dev.api.generate_ca_certificate = Mock()
        mock_linux_dev.api.generate_ssl_certificate = Mock()
        mock_linux_dev.api.generate_pkcs12 = Mock()
        mock_linux_dev.execute = Mock()
        
        # Mock testbed and loader
        mock_tb = Mock()
        mock_tb.devices.linux = mock_linux_dev
        mock_loader.load.return_value = mock_tb
        
        # Mock temporary directory
        mock_tmpdir_obj = Mock()
        mock_tmpdir_obj.name = '/tmp/test_dir'
        mock_tmpdir_obj.cleanup = Mock()
        mock_tempdir.return_value = mock_tmpdir_obj
        
        # Mock uuid
        mock_uuid.uuid4.return_value = 'test-password-uuid'
        
        # Call the function with secure_server=True
        result = configure_management_gnmi(self.device, secure_server=True)
        
        # Verify Linux device was connected
        mock_linux_dev.connect.assert_called_once_with(log_buffer=True)
        
        # Verify SSL key and certificate generation
        mock_linux_dev.api.generate_rsa_ssl_key.assert_any_call(private_key_name='rootCA.key', aes=True)
        mock_linux_dev.api.generate_ca_certificate.assert_called_once()
        mock_linux_dev.api.generate_rsa_ssl_key.assert_any_call(private_key_name='device.key', password='test-password-uuid', aes=True)
        mock_linux_dev.api.generate_ssl_certificate.assert_called()
        mock_linux_dev.api.generate_pkcs12.assert_called_once()
        
        # Verify device configuration
        self.device.api.copy_to_device.assert_called_once()
        self.device.api.configure_pki_import.assert_called_once_with(
            tp_name='trustpoint1',
            file_password='test-password-uuid',
            pkcs_file='device.p12',
            import_type='pkcs12'
        )
        self.device.api.configure_trustpoint.assert_called_once_with(
            tp_name='trustpoint1',
            revoke_check='none',
            rsa_key_size=2048
        )
        
        # Verify gnmi connection was updated
        self.device.connections.gnmi.update.assert_called_once()
        
        # Verify configure_gnxi was called with expected parameters
        self.device.api.configure_gnxi.assert_called_once_with(
            device=self.device,
            enable=True,
            server=True,
            port=None,
            secure_server=True,
            secure_client_auth=False,
            secure_trustpoint='trustpoint1'
        )
