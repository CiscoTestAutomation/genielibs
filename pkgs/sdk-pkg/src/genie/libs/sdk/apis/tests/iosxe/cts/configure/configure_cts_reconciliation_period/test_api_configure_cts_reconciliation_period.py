from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_reconciliation_period
from unittest.mock import Mock


class TestConfigureCtsReconciliationPeriod(TestCase):

    def test_configure_cts_reconciliation_period(self):
        self.device = Mock()
        result = configure_cts_reconciliation_period(self.device, '30')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp reconciliation period 30'],)
        )
