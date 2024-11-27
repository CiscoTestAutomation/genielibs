import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_update_periodic

class TestConfigureAaaAccountingUpdatePeriodic(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_accounting_update_periodic(self):
        configure_aaa_accounting_update_periodic(self.device, '2880')
        self.device.configure.assert_called_with(
            'aaa accounting update newinfo periodic 2880'
        )
