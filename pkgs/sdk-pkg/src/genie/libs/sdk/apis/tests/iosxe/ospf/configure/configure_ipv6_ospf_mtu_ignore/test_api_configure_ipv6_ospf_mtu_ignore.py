from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ipv6_ospf_mtu_ignore


class TestConfigureIpv6OspfMtuIgnore(TestCase):

    def test_configure_ipv6_ospf_mtu_ignore(self):
        device = Mock()
        result = configure_ipv6_ospf_mtu_ignore(
            device=device,
            interface='Vlan3000'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Vlan3000', ' ipv6 ospf mtu-ignore'],)
        )