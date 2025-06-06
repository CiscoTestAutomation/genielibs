from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_role_based_monitor
from unittest.mock import Mock


class TestUnconfigureCtsRoleBasedMonitor(TestCase):

    def test_unconfigure_cts_role_based_monitor(self):
        self.device = Mock()
        result = unconfigure_cts_role_based_monitor(self.device, None, 'ipv6', '2900', '3300')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts role-based monitor permissions from 2900 to 3300 ipv6',)
        )
