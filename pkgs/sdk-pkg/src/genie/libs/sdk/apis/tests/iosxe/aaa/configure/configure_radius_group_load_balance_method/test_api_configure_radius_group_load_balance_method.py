from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_group_load_balance_method
from unittest.mock import Mock


class TestConfigureRadiusGroupLoadBalanceMethod(TestCase):

    def test_configure_radius_group_load_balance_method(self):
        self.device = Mock()
        result = configure_radius_group_load_balance_method(self.device, 'ISE', 5)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['aaa group server radius ISE', 'load-balance method least-outstanding batch-size 5'],)
        )
