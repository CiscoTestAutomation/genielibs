import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_update


class TestUnconfigureAaaAccountingUpdate(unittest.TestCase):

    def test_unconfigure_aaa_accounting_update(self):
        self.device = Mock()
        unconfigure_aaa_accounting_update(self.device, 'periodic', 3)
        self.device.configure.assert_called_with(
            "no aaa accounting update periodic 3"
        )
