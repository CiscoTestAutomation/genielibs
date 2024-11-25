from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_commands


class TestConfigureAaaAccountingCommands(TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_accounting_commands(self):
        configure_aaa_accounting_commands(self.device, '15', 'test', 'none', None)
        self.device.configure.assert_called_once_with(
          'aaa accounting commands 15 test none'
        )
