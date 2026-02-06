import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import (
    configure_bgp_neighbor_advertisement_interval,
)


class TestConfigureBgpNeighborAdvertisementInterval(unittest.TestCase):

    def test_configure_bgp_neighbor_advertisement_interval(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_neighbor_advertisement_interval(
            device,
            "1002",        # bgp_asn
            "l2vpn evpn",  # address_family
            "4.4.4.4",     # neighbor
            "1",           # interval
            None,          # vrf
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1002",
                "address-family l2vpn evpn",
                "neighbor 4.4.4.4 advertisement-interval 1",
            ],)
        )