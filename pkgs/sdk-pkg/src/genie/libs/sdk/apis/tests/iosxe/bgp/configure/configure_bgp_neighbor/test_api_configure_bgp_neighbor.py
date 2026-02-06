import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor


class TestConfigureBgpNeighbor(unittest.TestCase):

    def test_configure_bgp_neighbor(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_neighbor(device, "64001", "64002", "192.168.1.2", "Gig8", None, None, None)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 64001",
                "neighbor 192.168.1.2 remote-as 64002",
                "neighbor 192.168.1.2 update-source Gig8",
            ],)
        )

    def test_configure_bgp_neighbor_1(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_neighbor(device, "64001", "64002", "192.168.1.2", "Gig8", None, "ipv4", None)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 64001",
                "address-family ipv4",
                "neighbor 192.168.1.2 remote-as 64002",
                "neighbor 192.168.1.2 update-source Gig8",
            ],)
        )

    def test_configure_bgp_neighbor_2(self):
        device = Mock()
        device.configure.return_value = ""

        # NOTE: API uses the last argument as VRF name (not description)
        result = configure_bgp_neighbor(device, "64001", "64002", "192.168.1.2", "Gig8", None, "ipv4", "test")
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 64001",
                "address-family ipv4 vrf test",
                "neighbor 192.168.1.2 remote-as 64002",
                "neighbor 192.168.1.2 update-source Gig8",
            ],)
        )