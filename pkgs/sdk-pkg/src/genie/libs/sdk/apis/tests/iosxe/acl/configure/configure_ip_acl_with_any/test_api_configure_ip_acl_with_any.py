from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ip_acl_with_any


class TestConfigureIpAclWithAny(TestCase):

    def test_configure_ip_acl_with_any(self):
        self.device = Mock()
        configure_ip_acl_with_any(self.device, 'racl_ipv41', 'permit')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended racl_ipv41', 'permit ip any any'] ,)
        )
