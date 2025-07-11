from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_interface_tunnel_spoke
from unittest.mock import Mock

class TestConfigureInterfaceTunnelSpoke(TestCase):

    def test_configure_interface_tunnel_spoke(self):
        self.device = Mock()
        configure_interface_tunnel_spoke(self.device, 'Tunnel0', '172.16.123.1', '255.255.255.0', 'Loopback101', 'OVERLAY', 'UNDERLAY', 'vpnprof', 'DMVPN', 1, 180, 100, '111.0.0.100', '111.1.1.1', False, True, '', True, '1.1.1.1', True, True)
        self.device.configure.assert_called_with((['interface Tunnel0', 'vrf forwarding OVERLAY', 'tunnel vrf UNDERLAY', 'ip address 172.16.123.1 255.255.255.0', 'tunnel source Loopback101', 'tunnel protection ipsec profile vpnprof', 'no ip redirects', 'ip nhrp authentication DMVPN', 'ip nhrp network-id 1', 'ip nhrp holdtime 180', 'tunnel key 100', 'ip nhrp nhs 111.0.0.100 nbma 111.1.1.1 multicast', 'tunnel mode ipsec dual-overlay', 'tunnel destination 1.1.1.1', 'ipv6 enable']))
