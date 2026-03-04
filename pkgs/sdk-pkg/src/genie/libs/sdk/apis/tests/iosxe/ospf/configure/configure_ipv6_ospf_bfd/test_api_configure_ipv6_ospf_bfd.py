from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ipv6_ospf_bfd
from unittest.mock import Mock


class TestConfigureIpv6OspfBfd(TestCase):

    def test_configure_ipv6_ospf_bfd(self):
        self.device = Mock()
        result = configure_ipv6_ospf_bfd(self.device, 'Vlan40', 'True')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Vlan40', 'ipv6 ospf bfd disable'],)
        )
