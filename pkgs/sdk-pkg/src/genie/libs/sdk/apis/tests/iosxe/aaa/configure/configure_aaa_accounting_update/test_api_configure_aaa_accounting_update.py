import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_update


class TestConfigureAaaAccountingUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_accounting_update(self):
        configure_aaa_accounting_update(self.device, 'periodic', 3)
        self.device.configure.assert_called_once_with(
            'aaa accounting update periodic 3'
        )
