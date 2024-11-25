import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_exec_default_start_stop_group


class TestUnconfigureAaaAccountingExecDefaultStartStopGroup(unittest.TestCase):

    def test_unconfigure_aaa_accounting_exec_default_start_stop_group(self):
        self.device = Mock()
        unconfigure_aaa_accounting_exec_default_start_stop_group(self.device, 'ISEGRP')
        self.device.configure.assert_called_with(
            'no aaa accounting exec default start-stop group ISEGRP'
        )
