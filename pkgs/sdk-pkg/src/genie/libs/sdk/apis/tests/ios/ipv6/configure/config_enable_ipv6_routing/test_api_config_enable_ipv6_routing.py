from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.ipv6.configure import config_enable_ipv6_routing


class TestConfigEnableIpv6Routing(TestCase):

    def test_config_enable_ipv6_routing(self):
        self.device = Mock()
        config_enable_ipv6_routing(self.device)
        self.device.configure.assert_called_once_with(
            "ipv6 unicast-routing"
        )

    def test_config_enable_ipv6_routing_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            config_enable_ipv6_routing(self.device)
