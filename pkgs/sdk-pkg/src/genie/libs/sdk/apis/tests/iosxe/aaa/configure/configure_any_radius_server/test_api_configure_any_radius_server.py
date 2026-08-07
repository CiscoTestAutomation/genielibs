import unittest
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_any_radius_server


class TestConfigureAnyRadiusServer(unittest.TestCase):

    def test_configure_any_radius_server(self):
        device = Mock()
        configure_any_radius_server(
            device, 'host', 'ipv4', '6.6.6.2', 1645, 1646, 'rad123')
        device.configure.assert_called_once_with(
            [
                "radius server host",
                "address ipv4 6.6.6.2 auth-port 1645 acct-port 1646",
                "key rad123",
            ]
        )

    def test_configure_any_radius_server_non_standard(self):
        device = Mock()
        configure_any_radius_server(
            device, 'host', 'ipv4', '6.6.6.2', 1645, 1646, 'rad123',
            non_standard=True)
        device.configure.assert_called_once_with(
            [
                "radius server host",
                "address ipv4 6.6.6.2 auth-port 1645 acct-port 1646",
                "non-standard",
                "key rad123",
            ]
        )

    def test_configure_any_radius_server_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_any_radius_server(
                device, 'host', 'ipv4', '6.6.6.2', 1645, 1646, 'rad123')
