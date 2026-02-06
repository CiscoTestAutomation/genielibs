import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_eigrp_redistribution


class TestConfigureBgpEigrpRedistribution(unittest.TestCase):

    def test_configure_bgp_eigrp_redistribution(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_eigrp_redistribution(device, 3, "ipv4", "green", 10)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 3",
                "address-family ipv4 vrf green",
                "redistribute eigrp 10",
            ],)
        )

    def test_configure_bgp_eigrp_redistribution_1(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_eigrp_redistribution(device, 3, "ipv4", "green", None)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 3",
                "address-family ipv4 vrf green",
            ],)
        )

    def test_configure_bgp_eigrp_redistribution_2(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_eigrp_redistribution(device, 3, "ipv4", None, 10)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 3",
                "address-family ipv4",
                "redistribute eigrp 10",
            ],)
        )