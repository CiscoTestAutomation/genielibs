import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_route_reflector_client


class TestConfigureBgpRouteReflectorClient(unittest.TestCase):

    def test_configure_bgp_route_reflector_client(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_route_reflector_client(device, 1, "pg-ibgp-rc")
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1",
                "neighbor pg-ibgp-rc route-reflector-client",
            ],)
        )