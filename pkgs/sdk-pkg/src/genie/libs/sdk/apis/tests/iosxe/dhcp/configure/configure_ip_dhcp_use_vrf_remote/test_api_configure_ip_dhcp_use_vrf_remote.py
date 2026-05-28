import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.dhcp.configure import (
    configure_ip_dhcp_use_vrf_remote,
    unconfigure_ip_dhcp_use_vrf_remote,
)


class TestConfigureIpDhcpUseVrfRemote(TestCase):

    def test_configure_ip_dhcp_use_vrf_remote(self):
        device = Mock()
        result = configure_ip_dhcp_use_vrf_remote(device)
        self.assertIsNone(result)
        device.configure.assert_called_once_with("ip dhcp use vrf remote")

    def test_configure_ip_dhcp_use_vrf_remote_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_ip_dhcp_use_vrf_remote(device)


class TestUnconfigureIpDhcpUseVrfRemote(TestCase):

    def test_unconfigure_ip_dhcp_use_vrf_remote(self):
        device = Mock()
        result = unconfigure_ip_dhcp_use_vrf_remote(device)
        self.assertIsNone(result)
        device.configure.assert_called_once_with("no ip dhcp use vrf remote")

    def test_unconfigure_ip_dhcp_use_vrf_remote_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_ip_dhcp_use_vrf_remote(device)


if __name__ == '__main__':
    unittest.main()
