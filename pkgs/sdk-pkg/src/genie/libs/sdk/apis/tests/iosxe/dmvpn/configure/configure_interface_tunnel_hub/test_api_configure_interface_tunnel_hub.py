from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_interface_tunnel_hub
from unittest.mock import Mock

class TestConfigureInterfaceTunnelHub(TestCase):

    def test_configure_interface_tunnel_hub(self):
        self.device = Mock()
        configure_interface_tunnel_hub(self.device, 'Tunnel0', '172.16.123.1', '255.255.255.0', 'Loopback101', 'OVERLAY', 'UNDERLAY', 180, 100, 'vpnprof', True, 'DMVPN', 1, False, True, True, '', True)
        self.device.configure.assert_called_with((['interface Tunnel0', 'vrf forwarding OVERLAY', 'tunnel vrf UNDERLAY', 'ip address 172.16.123.1 255.255.255.0', 'tunnel source Loopback101', 'ip nhrp map multicast dynamic', 'tunnel protection ipsec profile vpnprof', 'ip nhrp authentication DMVPN', 'ip nhrp network-id 1', 'ip nhrp holdtime 180', 'tunnel key 100', 'no ip redirects', 'tunnel mode ipsec dual-overlay', 'ipv6 enable']))
