from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_dynamic_tunnel
from unittest.mock import Mock


class TestConfigureDynamicTunnel(TestCase):

    def test_configure_dynamic_tunnel(self):
        self.device = Mock()
        result = configure_dynamic_tunnel(self.device, 1, 100, 'myIKEv2Profile', '10.1.1.1', '255.255.255.0', True, None, 'Te0/0/2', 'dmvpn-hub', 'ipv4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Loopback100', 'ip address 10.1.1.1 255.255.255.0', 'interface Virtual-Template1 type tunnel', 'ip unnumbered Loopback100', 'tunnel mode ipsec ipv4', 'tunnel source Te0/0/2', 'tunnel destination dynamic', 'tunnel protection ipsec profile dmvpn-hub', 'crypto ikev2 profile myIKEv2Profile', 'virtual-template 1'],)
        )
