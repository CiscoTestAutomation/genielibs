from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.ipv6.configure import unconfig_disable_ipv6_routing


class TestUnconfigDisableIpv6Routing(TestCase):

    def test_unconfig_disable_ipv6_routing(self):
        self.device = Mock()
        unconfig_disable_ipv6_routing(self.device)
        self.device.configure.assert_called_once_with(
            "no ipv6 unicast-routing"
        )

    def test_unconfig_disable_ipv6_routing_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfig_disable_ipv6_routing(self.device)
