import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_exec_default_start_stop_group

class TestConfigureAaaAccountingExecDefaultStartStopGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_accounting_exec_default_start_stop_group(self):
        configure_aaa_accounting_exec_default_start_stop_group(self.device, 'ISEGRP')
        self.device.configure.assert_called_once_with(
            'aaa accounting exec default start-stop group ISEGRP'
        )
