from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_list_extend_with_range_and_eq_port
from unittest.mock import Mock

class TestConfigureAccessListExtendWithRangeAndEqPort(TestCase):

    def test_configure_access_list_extend_with_range_and_eq_port(self):
        self.device = Mock()
        configure_access_list_extend_with_range_and_eq_port(self.device, 'ACL_1', 110, 'permit', 'udp', 50000, 50019, 3479)
        self.device.configure.assert_called_with(['ip access-list extended ACL_1', '110 permit udp any range 50000 50019 any eq 3479'])
