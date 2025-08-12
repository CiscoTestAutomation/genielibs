from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_role_based_monitor
from unittest.mock import Mock

class TestConfigureCtsRoleBasedMonitor(TestCase):

    def test_configure_cts_role_based_monitor(self):
        self.device = Mock()
        configure_cts_role_based_monitor(self.device, '', 'ipv6', 2900, 3300)
        self.assertEqual(self.device.configure.mock_calls[0].args,("cts role-based monitor permissions from 2900 to 3300 ipv6",))
