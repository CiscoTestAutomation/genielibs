import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_isis_redistribution


class TestConfigureBgpIsisRedistribution(unittest.TestCase):

    def test_configure_bgp_isis_redistribution(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_isis_redistribution(
            device,
            "100",
            "ipv4",
            "10",
            "level-1-2",
            True,
            "3.3.3.3",
            None,
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 100",
                "address-family ipv4",
                "redistribute connected",
                "neighbor 3.3.3.3 send-label",
                "redistribute isis 10 level-1-2",
            ],)
        )