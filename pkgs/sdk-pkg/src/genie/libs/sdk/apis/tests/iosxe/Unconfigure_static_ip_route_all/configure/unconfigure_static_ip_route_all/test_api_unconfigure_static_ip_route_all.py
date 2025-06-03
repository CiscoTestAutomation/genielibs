from unittest import TestCase
from genie.libs.sdk.apis.iosxe.Unconfigure_static_ip_route_all.configure import unconfigure_static_ip_route_all
from unittest.mock import Mock


class TestUnconfigureStaticIpRouteAll(TestCase):

    def test_unconfigure_static_ip_route_all(self):
        self.device = Mock()
        unconfigure_static_ip_route_all(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip route *',)
        )
 
