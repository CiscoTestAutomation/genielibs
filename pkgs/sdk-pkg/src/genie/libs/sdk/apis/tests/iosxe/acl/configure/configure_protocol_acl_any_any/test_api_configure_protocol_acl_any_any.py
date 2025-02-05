from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_protocol_acl_any_any
from unittest.mock import Mock


class TestConfigureProtocolAclAnyAny(TestCase):

    def test_configure_protocol_acl_any_any(self):
        self.device = Mock()
        result = configure_protocol_acl_any_any(self.device, 'ACL_1', 'permit', 'icmp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended ACL_1', 'permit icmp any any'],)
        )
