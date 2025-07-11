from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_list_extend_with_dst_address_and_gt_port
from unittest.mock import Mock

class TestConfigureAccessListExtendWithDstAddressAndGtPort(TestCase):

    def test_configure_access_list_extend_with_dst_address_and_gt_port(self):
        self.device = Mock()
        configure_access_list_extend_with_dst_address_and_gt_port(self.device, 'ACL_1', 70, 'permit', 'udp', 14000, 14449, '206.203.117.19', 2023)
        self.device.configure.assert_called_with(['ip access-list extended ACL_1', '70 permit udp any range 14000 14449 host 206.203.117.19 gt 2023'])
