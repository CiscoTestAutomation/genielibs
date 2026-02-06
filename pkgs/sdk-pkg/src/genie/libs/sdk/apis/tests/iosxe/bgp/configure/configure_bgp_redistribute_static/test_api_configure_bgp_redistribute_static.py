import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_redistribute_static


class TestConfigureBgpRedistributeStatic(unittest.TestCase):

    def test_configure_bgp_redistribute_static(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_redistribute_static(device, 65000, "vpnv4", None, "test")
        self.assertIsNone(result)

        # Update these if your API renders the CLI differently (e.g., route-map keyword, order, string vs list)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 65000",
                "address-family vpnv4",
                "redistribute static route-map test",
            ],)
        )