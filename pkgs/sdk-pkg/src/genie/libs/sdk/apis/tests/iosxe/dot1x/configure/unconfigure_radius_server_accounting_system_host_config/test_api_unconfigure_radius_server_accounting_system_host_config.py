from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import unconfigure_radius_server_accounting_system_host_config
from unittest.mock import Mock


class TestUnconfigureRadiusServerAccountingSystemHostConfig(TestCase):

    def test_unconfigure_radius_server_accounting_system_host_config(self):
        self.device = Mock()
        result = unconfigure_radius_server_accounting_system_host_config(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no radius-server accounting system host-config',)
        )
