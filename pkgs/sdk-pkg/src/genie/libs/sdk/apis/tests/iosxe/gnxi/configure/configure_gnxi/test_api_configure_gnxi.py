import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.gnxi.configure import configure_gnxi


class TestConfigureGnxi(TestCase):

    def test_configure_gnxi_enable(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device)

        expected_output = ['gnxi']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi'])

    def test_configure_gnxi_port(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, port=8080)

        expected_output = ['gnxi', 'gnxi port 8080']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi port 8080'])

    def test_configure_gnxi_secure_port(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_port=443)

        expected_output = ['gnxi', 'gnxi secure-port 443']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-port 443'])

    def test_configure_gnxi_secure_allow_self_signed_trustpoint(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_allow_self_signed_trustpoint=True)

        expected_output = ['gnxi', 'gnxi secure-allow-self-signed-trustpoint']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-allow-self-signed-trustpoint'])

    def test_configure_gnxi_secure_client_auth(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_client_auth=True)

        expected_output = ['gnxi', 'gnxi secure-client-auth']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-client-auth'])

    def test_configure_gnxi_secure_password_auth(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_password_auth=True)

        expected_output = ['gnxi', 'gnxi secure-password-auth']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-password-auth'])

    def test_configure_gnxi_secure_peer_verify_trustpoint(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_peer_verify_trustpoint='gnoi_tp')

        expected_output = ['gnxi', 'gnxi secure-peer-verify-trustpoint gnoi_tp']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-peer-verify-trustpoint gnoi_tp'])

    def test_configure_gnxi_secure_trustpoint(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_trustpoint='gnoi_tp')

        expected_output = ['gnxi', 'gnxi secure-trustpoint gnoi_tp']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-trustpoint gnoi_tp'])

    def test_configure_gnxi_secure_init(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_init=True)

        expected_output = ['gnxi', 'gnxi secure-init']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-init'])

    def test_configure_gnxi_server(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, server=True)

        expected_output = ['gnxi', 'gnxi server']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi server'])

    def test_configure_gnxi_secure_server(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_server=True)

        expected_output = ['gnxi', 'gnxi secure-server']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-server'])

    def test_configure_gnxi_secure_server_port(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_port=443, secure_server=True)

        expected_output = ['gnxi', 'gnxi secure-port 443', 'gnxi secure-server']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-port 443', 'gnxi secure-server'])

    def test_configure_gnxi_server_port(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, port=8080, server=True)

        expected_output = ['gnxi', 'gnxi port 8080', 'gnxi server']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi port 8080', 'gnxi server'])

    def test_configure_gnxi_servers(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, server=True, secure_server=True)

        expected_output = ['gnxi', 'gnxi server', 'gnxi secure-server']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi server', 'gnxi secure-server'])

    def test_configure_gnxi_secure_init_password_auth(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, secure_password_auth=True, secure_init=True)

        expected_output = ['gnxi', 'gnxi secure-password-auth', 'gnxi secure-init']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi', 'gnxi secure-password-auth', 'gnxi secure-init'])

    def test_configure_gnxi_secure_peer_verify_trustpoint_and_trustpoint(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(
            device,
            secure_peer_verify_trustpoint='gnoi_tp',
            secure_trustpoint='gnoi_tp',
            server=True,
            port=None
        )

        expected_output = [
            'gnxi',
            'gnxi secure-peer-verify-trustpoint gnoi_tp',
            'gnxi secure-trustpoint gnoi_tp',
            'gnxi server'
        ]
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(expected_output)

    def test_configure_gnxi_disable_server(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, enable=False, server=True)

        expected_output = ['gnxi server']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi server'])

    def test_configure_gnxi_disable_secure_init(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, enable=False, secure_init=True)

        expected_output = ['gnxi secure-init']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi secure-init'])

    def test_configure_gnxi_disable_secure_password_auth(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(device, enable=False, secure_password_auth=True)

        expected_output = ['gnxi secure-password-auth']
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(['gnxi secure-password-auth'])

    def test_configure_gnxi_all_params(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gnxi(
            device,
            enable=True,
            server=True,
            secure_server=True,
            secure_port=443,
            port=8080,
            secure_allow_self_signed_trustpoint=True,
            secure_client_auth=True,
            secure_init=True,
            secure_password_auth=True,
            secure_peer_verify_trustpoint='gnoi_tp',
            secure_trustpoint='gnoi_tp'
        )

        expected_output = [
            'gnxi',
            'gnxi secure-port 443',
            'gnxi port 8080',
            'gnxi secure-allow-self-signed-trustpoint',
            'gnxi secure-client-auth',
            'gnxi secure-password-auth',
            'gnxi secure-peer-verify-trustpoint gnoi_tp',
            'gnxi secure-trustpoint gnoi_tp',
            'gnxi secure-init',
            'gnxi server',
            'gnxi secure-server'
        ]
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(expected_output)


if __name__ == '__main__':
    unittest.main()