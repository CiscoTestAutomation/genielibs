import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_update_periodic_interval


class TestUnconfigureAaaAccountingUpdatePeriodicInterval(unittest.TestCase):

    def test_unconfigure_aaa_accounting_update_periodic_interval(self):
        self.device = Mock()
        unconfigure_aaa_accounting_update_periodic_interval(self.device, 10)
        self.device.configure.assert_called_with(
            'no aaa accounting update periodic 10'
        )
