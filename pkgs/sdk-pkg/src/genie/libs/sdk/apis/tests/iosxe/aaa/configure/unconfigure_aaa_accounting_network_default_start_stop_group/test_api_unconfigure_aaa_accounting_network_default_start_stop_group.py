from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_network_default_start_stop_group
from unittest.mock import Mock


class TestUnconfigureAaaAccountingNetworkDefaultStartStopGroup(TestCase):

    def test_unconfigure_aaa_accounting_network_default_start_stop_group(self):
        self.device = Mock()
        unconfigure_aaa_accounting_network_default_start_stop_group(self.device, 'RADIUS_SERVER')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no aaa accounting network default start-stop group RADIUS_SERVER',)
        )

