import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ntp.configure import configure_ntp_server


class TestConfigureNtpServer(TestCase):

    def test_configure_ntp_server_single_ip(self):
        """Verify correct CLI for a single NTP server."""
        device = Mock()
        device.name = 'Router1'
        result = configure_ntp_server(device, ntp_config=['192.168.1.1'])
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ntp server 192.168.1.1'],),
        )

    def test_configure_ntp_server_multiple_ips(self):
        """Verify correct CLI for multiple NTP servers."""
        device = Mock()
        device.name = 'Router1'
        configure_ntp_server(device, ntp_config=['192.168.1.1', '10.0.0.1'])
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ntp server 192.168.1.1', 'ntp server 10.0.0.1'],),
        )

    def test_configure_ntp_server_with_vrf(self):
        """Verify correct CLI when VRF is specified."""
        device = Mock()
        device.name = 'Router1'
        configure_ntp_server(device, ntp_config=['10.1.1.1'], vrf='Mgmt-vrf')
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ntp server vrf Mgmt-vrf 10.1.1.1'],),
        )

    def test_configure_ntp_server_invalid_ip(self):
        """Verify ValueError for invalid characters in NTP server address."""
        device = Mock()
        device.name = 'Router1'
        with self.assertRaises(ValueError):
            configure_ntp_server(device, ntp_config=['192.168.1.1; reboot'])

    def test_configure_ntp_server_invalid_vrf(self):
        """Verify ValueError for invalid characters in VRF."""
        device = Mock()
        device.name = 'Router1'
        with self.assertRaises(ValueError):
            configure_ntp_server(device, ntp_config=['10.1.1.1'], vrf='bad vrf!')

    def test_configure_ntp_server_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_ntp_server(device, ntp_config=['192.168.1.1'])


if __name__ == '__main__':
    unittest.main()
