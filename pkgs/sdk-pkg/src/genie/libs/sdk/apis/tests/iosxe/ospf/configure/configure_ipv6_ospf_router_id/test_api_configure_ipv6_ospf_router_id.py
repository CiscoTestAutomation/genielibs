from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ipv6_ospf_router_id


class TestConfigureIpv6OspfRouterId(TestCase):

    def test_configure_ipv6_ospf_router_id(self):
        device = Mock()
        result = configure_ipv6_ospf_router_id(
            device,
            '10',
            '1.1.1.1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ipv6 router ospf 10', 'router-id 1.1.1.1'],)
        )