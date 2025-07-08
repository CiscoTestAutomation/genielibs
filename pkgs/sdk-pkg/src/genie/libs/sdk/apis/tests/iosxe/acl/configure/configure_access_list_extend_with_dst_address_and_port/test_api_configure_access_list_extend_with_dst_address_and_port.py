from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_list_extend_with_dst_address_and_port
from unittest.mock import Mock

class TestConfigureAccessListExtendWithDstAddressAndPort(TestCase):

    def test_configure_access_list_extend_with_dst_address_and_port(self):
        self.device = Mock()
        configure_access_list_extend_with_dst_address_and_port(self.device, 'ACL_1', 10, 'deny', 'udp', '8.33.237.0', '0.0.0.255', 10000, 13000)
        self.device.configure.assert_called_with(['ip access-list extended ACL_1', '10 deny udp any 8.33.237.0 0.0.0.255 range 10000 13000'])
