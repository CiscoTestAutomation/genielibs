from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_scale_ipv6_accesslist_config


class TestConfigureScaleIpv6AccesslistConfig(TestCase):

    def test_configure_scale_ipv6_accesslist_config(self):
        self.device = Mock()
        configure_scale_ipv6_accesslist_config(self.device, 'IPV6_CRITICAL_AUTH_ACL', 'sequence 10 permit ipv6 any any')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 access-list IPV6_CRITICAL_AUTH_ACL', 'sequence 10 permit ipv6 any any'] ,)
        )
