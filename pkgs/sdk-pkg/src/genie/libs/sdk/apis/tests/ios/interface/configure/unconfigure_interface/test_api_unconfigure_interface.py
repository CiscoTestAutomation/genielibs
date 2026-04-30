from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.interface.configure import unconfigure_interface


class TestUnconfigureInterface(TestCase):

    def test_unconfigure_interface_all_options(self):
        self.device = Mock()
        unconfigure_interface(
            self.device, 'GigabitEthernet0/0',
            ip_address='10.1.1.1', mask='255.255.255.0',
            ipv6_address='2001:db8::1', ipv6_prefix_length='64',
            mac_address='0000.1111.2222', ipv6_enable=True
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " no mac-address 0000.1111.2222",
                " shutdown",
                " no ipv6 enable",
                " no ip address 10.1.1.1 255.255.255.0",
                " no ipv6 address 2001:db8::1/64",
            ]
        )

    def test_unconfigure_interface_ipv4_only(self):
        self.device = Mock()
        unconfigure_interface(
            self.device, 'GigabitEthernet0/0',
            ip_address='10.1.1.1', mask='255.255.255.0'
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " shutdown",
                " no ip address 10.1.1.1 255.255.255.0",
            ]
        )

    def test_unconfigure_interface_dhcp(self):
        self.device = Mock()
        unconfigure_interface(
            self.device, 'GigabitEthernet0/0',
            dhcp='dhcp'
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " shutdown",
                " no ip address dhcp",
            ]
        )

    def test_unconfigure_interface_ipv6_autoconfig(self):
        self.device = Mock()
        unconfigure_interface(
            self.device, 'GigabitEthernet0/0',
            ipv6_autoconfig='autoconfig'
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " shutdown",
                " no ipv6 address autoconfig",
            ]
        )
