from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ip_acl_with_any
from unittest.mock import Mock


class TestConfigureIpAclWithAny(TestCase):

    def test_configure_ip_acl_with_any(self):
        self.device = Mock()
        result = configure_ip_acl_with_any(self.device, 'test', 'permit', 'True')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test', 'permit ip any any log'],)
        )
