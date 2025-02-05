from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_exec_default_start_stop
from unittest.mock import Mock


class TestUnconfigureAaaAccountingExecDefaultStartStop(TestCase):

    def test_unconfigure_aaa_accounting_exec_default_start_stop(self):
        self.device = Mock()
        result = unconfigure_aaa_accounting_exec_default_start_stop(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no aaa accounting exec default start-stop group',)
        )
