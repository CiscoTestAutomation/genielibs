import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_router_ospf


class TestUnconfigureRouterOspf(unittest.TestCase):

    def test_unconfigure_router_ospf(self):
        device = Mock()

        result = unconfigure_router_ospf(
            device,
            '1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no router ospf 1',)
        )