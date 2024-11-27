import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_identity_default_start_stop

class TestConfigureAaaAccountingIdentityDefaultStartStop(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_accounting_identity_default_start_stop(self):
        configure_aaa_accounting_identity_default_start_stop(self.device, 'group', 'radius')
        self.device.configure.assert_called_once_with(
            'aaa accounting identity default start-stop group radius'
        )
