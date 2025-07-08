from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_trust
from unittest.mock import Mock

class TestConfigureIpv6DhcpRelayTrust(TestCase):

    def test_configure_ipv6_dhcp_relay_trust(self):
        self.device = Mock()
        configure_ipv6_dhcp_relay_trust(self.device, 'Vlan1500')
        self.device.configure.assert_called_with(['interface Vlan1500', 'ipv6 dhcp relay trust'])
