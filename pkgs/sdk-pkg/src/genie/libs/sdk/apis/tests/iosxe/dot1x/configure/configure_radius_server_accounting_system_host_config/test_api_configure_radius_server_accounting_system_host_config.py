from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_radius_server_accounting_system_host_config
from unittest.mock import Mock


class TestConfigureRadiusServerAccountingSystemHostConfig(TestCase):

    def test_configure_radius_server_accounting_system_host_config(self):
        self.device = Mock()
        result = configure_radius_server_accounting_system_host_config(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('radius-server accounting system host-config',)
        )
