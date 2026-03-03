from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_ip_proxy_arp
from unittest.mock import Mock


class TestUnconfigureInterfaceIpProxyArp(TestCase):

    def test_unconfigure_interface_ip_proxy_arp(self):
        self.device = Mock()
        result = unconfigure_interface_ip_proxy_arp(self.device, 'Port-channel1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Port-channel1', 'no ip proxy-arp'],)
        )
