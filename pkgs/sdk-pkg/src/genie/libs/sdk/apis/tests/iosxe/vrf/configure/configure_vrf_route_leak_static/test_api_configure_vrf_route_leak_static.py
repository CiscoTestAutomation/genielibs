from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vrf_route_leak_static
from unittest.mock import Mock


class TestConfigureVrfRouteLeakStatic(TestCase):

    def test_configure_vrf_route_leak_static(self):
        self.device = Mock()
        result = configure_vrf_route_leak_static(self.device, 'star_1', '22.0.0.2', '255.255.255.255', '102.0.1.2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip route vrf star_1 22.0.0.2 255.255.255.255 102.0.1.2 global'],)
        )
