from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_reconciliation_period
from unittest.mock import Mock


class TestUnconfigureCtsReconciliationPeriod(TestCase):

    def test_unconfigure_cts_reconciliation_period(self):
        self.device = Mock()
        result = unconfigure_cts_reconciliation_period(self.device, '30')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp reconciliation period 30'],)
        )
