import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_sso_route_refresh_enable


class TestConfigureBgpSsoRouteRefreshEnable(unittest.TestCase):

    def test_configure_bgp_sso_route_refresh_enable(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_sso_route_refresh_enable(device, 5001)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ("router bgp 5001\nbgp sso route-refresh-enable\n",)
        )