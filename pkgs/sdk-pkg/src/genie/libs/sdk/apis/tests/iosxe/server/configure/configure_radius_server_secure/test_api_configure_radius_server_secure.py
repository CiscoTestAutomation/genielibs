import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_secure


class TestConfigureRadiusServerSecure(TestCase):

    def test_full_config(self):
        """Verify full config with TLS, send-ma, validate-ma."""
        device = Mock()
        device.name = 'Router1'
        server_config = {
            'server_name': 'ISE_SERVER',
            'ipv4': '10.6.1.200',
            'auth_port': '1812',
            'acct_port': '1813',
            'key': 'cisco123',
            'timeout': '100',
            'retransmit': '5',
            'send_ma': True,
            'validate_ma': True,
            'tls_connectiontimeout': 5,
            'tls_idletimeout': 60,
            'tls_retransmit': 2,
            'tls_trustpoint_client': 'RAD-CLIENT',
            'tls_trustpoint_server': 'RAD-CA',
        }
        configure_radius_server_secure(device, server_config)
        config_list = device.configure.call_args[0][0]
        self.assertIn('radius server ISE_SERVER', config_list)
        self.assertIn('address ipv4 10.6.1.200 auth-port 1812 acct-port 1813', config_list)
        self.assertIn('key cisco123', config_list)
        self.assertIn('timeout 100', config_list)
        self.assertIn('retransmit 5', config_list)
        self.assertIn('send-ma', config_list)
        self.assertIn('validate-ma', config_list)
        self.assertIn('tls connectiontimeout 5', config_list)
        self.assertIn('tls idletimeout 60', config_list)
        self.assertIn('tls retransmit 2', config_list)
        self.assertIn('tls trustpoint client RAD-CLIENT', config_list)
        self.assertIn('tls trustpoint server RAD-CA', config_list)

    def test_minimal_config(self):
        """Verify minimal config with only server name and IP."""
        device = Mock()
        device.name = 'Router1'
        server_config = {
            'server_name': 'RAD1',
            'ipv4': '192.168.1.1',
            'auth_port': '1812',
            'acct_port': '1813',
        }
        configure_radius_server_secure(device, server_config)
        config_list = device.configure.call_args[0][0]
        self.assertIn('radius server RAD1', config_list)
        self.assertIn('address ipv4 192.168.1.1 auth-port 1812 acct-port 1813', config_list)

    def test_with_key_encryption(self):
        """Verify key with encryption type."""
        device = Mock()
        device.name = 'Router1'
        server_config = {
            'server_name': 'RAD1',
            'ipv4': '10.1.1.1',
            'auth_port': '1812',
            'acct_port': '1813',
            'key_encryption': '7',
            'key': 'EncryptedKey',
        }
        configure_radius_server_secure(device, server_config)
        config_list = device.configure.call_args[0][0]
        self.assertIn('key 7 EncryptedKey', config_list)

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        server_config = {
            'server_name': 'RAD1',
            'ipv4': '10.1.1.1',
            'auth_port': '1812',
            'acct_port': '1813',
        }
        with self.assertRaises(SubCommandFailure):
            configure_radius_server_secure(device, server_config)


if __name__ == '__main__':
    unittest.main()
