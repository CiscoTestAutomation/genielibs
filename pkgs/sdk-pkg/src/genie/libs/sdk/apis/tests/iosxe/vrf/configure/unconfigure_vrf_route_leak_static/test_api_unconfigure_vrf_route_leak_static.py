from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import unconfigure_vrf_route_leak_static
from unittest.mock import Mock


class TestUnconfigureVrfRouteLeakStatic(TestCase):

    def test_unconfigure_vrf_route_leak_static(self):
        self.device = Mock()
        result = unconfigure_vrf_route_leak_static(self.device, 'star_1', '22.0.0.2', '255.255.255.255', '102.0.1.2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip route vrf star_1 22.0.0.2 255.255.255.255 102.0.1.2 global'],)
        )
