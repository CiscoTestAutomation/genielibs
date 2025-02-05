from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_exec_default_start_stop
from unittest.mock import Mock


class TestConfigureAaaAccountingExecDefaultStartStop(TestCase):

    def test_configure_aaa_accounting_exec_default_start_stop(self):
        self.device = Mock()
        result = configure_aaa_accounting_exec_default_start_stop(self.device, 'ISE')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa accounting exec default start-stop group ISE',)
        )
