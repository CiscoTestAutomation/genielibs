import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_update_periodic_interval


class TestConfigureAaaAccountingUpdatePeriodicInterval(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_accounting_update_periodic_interval(self):
        configure_aaa_accounting_update_periodic_interval(self.device, 10)
        self.device.configure.assert_called_once_with(
            'aaa accounting update periodic 10'
        )
