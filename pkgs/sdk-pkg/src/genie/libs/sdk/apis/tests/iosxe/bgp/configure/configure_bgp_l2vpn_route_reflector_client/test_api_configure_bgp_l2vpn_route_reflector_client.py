import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import (
    configure_bgp_l2vpn_route_reflector_client,
)


class TestConfigureBgpL2vpnRouteReflectorClient(unittest.TestCase):

    def test_configure_bgp_l2vpn_route_reflector_client(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_l2vpn_route_reflector_client(
            device,
            "l2vpn",        
            1,              
            "pg-ibgp-rc",   
            "evpn",         
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1",
                "address-family l2vpn evpn",
                "neighbor pg-ibgp-rc route-reflector-client",
            ],)
        )