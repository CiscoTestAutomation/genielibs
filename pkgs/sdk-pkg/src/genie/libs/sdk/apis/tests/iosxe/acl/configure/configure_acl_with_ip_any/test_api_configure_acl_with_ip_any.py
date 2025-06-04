from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_acl_with_ip_any


class TestConfigureAclWithIpAny(TestCase):

    def test_configure_acl_with_ip_any(self):
        self.device = Mock()
        configure_acl_with_ip_any(self.device, 102, 'permit')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['access-list 102 permit ip any any'],)
        )
