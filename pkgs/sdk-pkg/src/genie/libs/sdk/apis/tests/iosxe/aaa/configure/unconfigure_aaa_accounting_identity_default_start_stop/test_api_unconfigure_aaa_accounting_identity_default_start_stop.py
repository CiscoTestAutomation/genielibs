import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_identity_default_start_stop


class TestUnconfigureAaaAccountingIdentityDefaultStartStop(unittest.TestCase):

    def test_unconfigure_aaa_accounting_identity_default_start_stop(self):
        self.device = Mock()
        unconfigure_aaa_accounting_identity_default_start_stop(self.device, 'group', 'My-Radius')
        self.device.configure.assert_called_with(
            'no aaa accounting identity default start-stop group My-Radius'
        )
