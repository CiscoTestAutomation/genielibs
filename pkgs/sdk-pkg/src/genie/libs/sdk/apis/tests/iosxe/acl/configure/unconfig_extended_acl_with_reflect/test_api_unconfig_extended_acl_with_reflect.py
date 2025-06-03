from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfig_extended_acl_with_reflect


class TestUnconfigExtendedAclWithReflect(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        unconfig_extended_acl_with_reflect(self.device, 'test2', 'R10000', 'permit', 'tcp', '1.1.1.1', None, None, '3.3.3.3', None, None, None, None, 'host', '10', '120', 'timeout', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test2', 'no 10 permit tcp host 1.1.1.1 host 3.3.3.3 reflect R10000 timeout 120'] ,)
        )
