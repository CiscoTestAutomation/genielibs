import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_router_id_interface


class TestConfigureBgpRouterIdInterface(unittest.TestCase):

    def test_configure_bgp_router_id_interface(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_router_id_interface(device, 1, "Loopback0")
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1",
                "bgp router-id interface Loopback0",
            ],)
        )