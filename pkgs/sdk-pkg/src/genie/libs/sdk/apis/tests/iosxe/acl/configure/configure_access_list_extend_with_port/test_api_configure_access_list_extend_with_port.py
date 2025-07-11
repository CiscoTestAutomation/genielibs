from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_list_extend_with_port
from unittest.mock import Mock

class TestConfigureAccessListExtendWithPort(TestCase):

    def test_configure_access_list_extend_with_port(self):
        self.device = Mock()
        configure_access_list_extend_with_port(self.device, 'ACL_1', 50, 'permit', 'udp', 14000, 14449, 8000, 8999)
        self.device.configure.assert_called_with(['ip access-list extended ACL_1', '50 permit udp any range 14000 14449 any range 8000 8999'])
