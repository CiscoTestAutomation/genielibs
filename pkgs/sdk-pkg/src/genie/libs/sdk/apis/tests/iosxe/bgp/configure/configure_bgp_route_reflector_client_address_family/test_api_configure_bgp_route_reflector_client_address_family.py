from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_route_reflector_client_address_family
from unittest.mock import Mock


class TestConfigureBgpRouteReflectorClientAddressFamily(TestCase):

    def test_configure_bgp_route_reflector_client_address_family(self):
        self.device = Mock()
        result = configure_bgp_route_reflector_client_address_family(self.device, '50', '1::1', 'ipv6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 50', 'address-family ipv6', 'neighbor 1::1 route-reflector-client', 'exit-address-family'],)
        )
