from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server


class TestConfigureRadiusServer(TestCase):

    def test_configure_radius_server(self):
        device = Mock()

        result = configure_radius_server(
            device=device,
            server_config={
                'acct_port': '1813',
                'auth_port': '1812',
                'ipv4': '20.20.20.2',
                'key': 'Cisco',
                'server_name': 'ISE2.7',
            },
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'radius server ISE2.7',
            'address ipv4 20.20.20.2 auth-port 1812 '
            'acct-port 1813',
            'key Cisco',
        ])

    def test_configure_radius_server_1(self):
        device = Mock()

        result = configure_radius_server(
            device=device,
            server_config={
                'acct_port': '1813',
                'auth_port': '1812',
                'dscp_acct': '10',
                'dscp_auth': '20',
                'ipv4': '20.20.20.2',
                'key': 'Cisco',
                'server_name': 'ISE2.7',
            },
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'radius server ISE2.7',
            'address ipv4 20.20.20.2 auth-port 1812 '
            'acct-port 1813',
            'key Cisco',
            'dscp auth 20',
            'dscp acct 10',
        ])
