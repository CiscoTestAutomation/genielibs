from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_network_default_start_stop_group


class TestConfigureAaaAccountingNetworkDefaultStartStopGroup(TestCase):

    def test_configure_aaa_accounting_network_default_start_stop_group(self):
        self.device = Mock()
        configure_aaa_accounting_network_default_start_stop_group(self.device, 'RADIUS_SERVER')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa accounting network default start-stop group RADIUS_SERVER',)
        )