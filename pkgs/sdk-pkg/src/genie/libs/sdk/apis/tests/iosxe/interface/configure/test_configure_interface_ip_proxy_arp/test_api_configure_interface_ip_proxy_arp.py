from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_ip_proxy_arp
from unicon.core.errors import SubCommandFailure


class TestConfigureInterfaceIpProxyArp(TestCase):

    def test_configure_interface_ip_proxy_arp(self):
        self.device = Mock()
        interface = 'g0/0/1'
        configure_interface_ip_proxy_arp(self.device, interface=interface)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                f"interface {interface}",
                "ip proxy-arp",
            ],)
        )

    def test_configure_interface_ip_proxy_arp_failure(self):
        self.device = Mock()
        self.device.name = 'router1'
        interface = 'g0/0/1'
        self.device.configure.side_effect = SubCommandFailure('configure failed')
        with self.assertRaises(SubCommandFailure):
            configure_interface_ip_proxy_arp(self.device, interface=interface)
