import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_router_bgp


class TestUnconfigureRouterBgp(unittest.TestCase):

    def test_unconfigure_router_bgp(self):
        device = Mock()

        result = unconfigure_router_bgp(
            device,
            '1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no router bgp 1',)
        )