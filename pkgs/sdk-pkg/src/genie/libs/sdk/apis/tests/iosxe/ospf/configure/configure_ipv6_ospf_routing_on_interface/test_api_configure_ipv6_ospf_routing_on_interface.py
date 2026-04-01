from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ipv6_ospf_routing_on_interface


class TestConfigureIpv6OspfRoutingOnInterface(TestCase):

    def test_configure_ipv6_ospf_routing_on_interface(self):
        device = Mock()
        result = configure_ipv6_ospf_routing_on_interface(
            device,
            'HundredGigE1/0/21',
            '1',
            0
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface HundredGigE1/0/21', 'ipv6 ospf 1 area 0'],)
        )