from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_ip_ssh_pubkey_chain
from unittest.mock import Mock


class TestConfigureIpSshPubkeyChain(TestCase):

    def test_configure_ip_ssh_pubkey_chain_username_key_string(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data
        username = 'cisco'
        key_string = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7S3inyJfhVGDjIyMPF5Ce2HtinlVjVmmm8fZa9VaUMl2LG'
        
        # Call the function
        result = configure_ip_ssh_pubkey_chain(self.device, username=username, key_string=key_string)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'username cisco',
            'key-string'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_configure_ip_ssh_pubkey_chain_username_key_hash(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data
        username = 'cisco'
        key_hash = '1234567890abcdef'
        
        # Call the function
        result = configure_ip_ssh_pubkey_chain(self.device, username=username, key_hash=key_hash)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'username cisco',
            'key-hash 1234567890abcdef',
            'exit',
            'exit'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_configure_ip_ssh_pubkey_chain_server_key_string(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data
        server = '192.168.1.100'
        key_string = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7S3inyJfhVGDjIyMPF5Ce2HtinlVjVmmm8fZa9VaUMl2LG'
        
        # Call the function
        result = configure_ip_ssh_pubkey_chain(self.device, server=server, key_string=key_string)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'server 192.168.1.100',
            'key-string'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_configure_ip_ssh_pubkey_chain_server_key_hash(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data
        server = '192.168.1.100'
        key_hash = '1234567890abcdef'
        
        # Call the function
        result = configure_ip_ssh_pubkey_chain(self.device, server=server, key_hash=key_hash)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'server 192.168.1.100',
            'key-hash 1234567890abcdef',
            'exit',
            'exit'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_configure_ip_ssh_pubkey_chain_multiline_key_string(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data with multi-line key
        username = 'admin'
        key_string = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7S3inyJfhVGDjIyMPF5Ce2HtinlVjVmmm8f\nZa9VaUMl2LGcYyO3BQyK+Q1j7P8Pj+qQEiNYz5kPgH7fGhN0M4q8J9JmVjZx5wV2R\nadmin@example.com'
        
        # Call the function
        result = configure_ip_ssh_pubkey_chain(self.device, username=username, key_string=key_string)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'username admin',
            'key-string'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)
