from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import unconfigure_ip_ssh_pubkey_chain
from unittest.mock import Mock


class TestUnconfigureIpSshPubkeyChain(TestCase):

    def test_unconfigure_ip_ssh_pubkey_chain_username(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data
        username = 'cisco'
        
        # Call the function
        result = unconfigure_ip_ssh_pubkey_chain(self.device, username=username)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'no username cisco',
            'exit'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_unconfigure_ip_ssh_pubkey_chain_server(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data
        server = '192.168.1.100'
        
        # Call the function
        result = unconfigure_ip_ssh_pubkey_chain(self.device, server=server)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'no server 192.168.1.100',
            'exit'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_unconfigure_ip_ssh_pubkey_chain_different_user(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Test data with different username
        username = 'admin'
        
        # Call the function
        result = unconfigure_ip_ssh_pubkey_chain(self.device, username=username)
        
        # Verify the configuration commands were called
        expected_config = [
            'ip ssh pubkey-chain',
            'no username admin',
            'exit'
        ]
        
        # Check that configure was called with the expected commands
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)
