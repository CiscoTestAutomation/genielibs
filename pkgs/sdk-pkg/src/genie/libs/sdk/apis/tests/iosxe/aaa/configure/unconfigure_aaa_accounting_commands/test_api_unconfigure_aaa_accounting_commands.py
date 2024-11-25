import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_commands


class TestUnconfigureAaaAccountingCommands(unittest.TestCase):

    def test_unconfigure_aaa_accounting_commands(self):
        self.device = Mock()
        unconfigure_aaa_accounting_commands(self.device, '15', 'test', 'none', '', None)
        self.device.configure.assert_called_with(
            'no aaa accounting commands 15 test none'
        )

    def test_unconfigure_aaa_accounting_commands_1(self):
        self.device = Mock()
        unconfigure_aaa_accounting_commands(self.device, '1', 'default', 'start-stop', 'broadcast', 'DATANET')
        self.device.configure.assert_called_with(
            'no aaa accounting commands 1 default start-stop broadcast group DATANET'
        )
