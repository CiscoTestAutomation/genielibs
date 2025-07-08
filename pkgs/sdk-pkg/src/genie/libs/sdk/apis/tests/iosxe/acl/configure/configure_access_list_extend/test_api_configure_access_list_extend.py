from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_list_extend
from unittest.mock import Mock

class TestConfigureAccessListExtend(TestCase):

    def test_configure_access_list_extend(self):
        self.device = Mock()
        configure_access_list_extend(self.device, 'ACL_1', 120, 'permit', 'icmp')
        self.device.configure.assert_called_with(['ip access-list extended ACL_1', '120 permit icmp any any'])
