import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import (
    configure_bgp_l2vpn_evpn_rewrite_evpn_rt_asn,
)


class TestConfigureBgpL2vpnEvpnRewriteEvpnRtAsn(unittest.TestCase):

    def test_configure_bgp_l2vpn_evpn_rewrite_evpn_rt_asn(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_l2vpn_evpn_rewrite_evpn_rt_asn(device, "1002")
        self.assertIsNone(result)

        # Update expected CLI if your API renders it differently (string vs list, ordering, etc.)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1002",
                "address-family l2vpn evpn",
                "rewrite-evpn-rt-asn",
            ],)
        )