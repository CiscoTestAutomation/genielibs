from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.pbr.configure import configure_ip_local_policy_route_map


class TestConfigureIpLocalPolicyRouteMap(TestCase):

    def test_configure_ip_local_policy_route_map(self):
        device = Mock()

        result = configure_ip_local_policy_route_map(
            device, route_map_name="local_pbr", timeout=60
        )
        device.configure.assert_called_with(
            ["ip local policy route-map local_pbr"],
            timeout=60,
        )
        self.assertEqual(result, None)
