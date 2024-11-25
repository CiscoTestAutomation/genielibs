import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_dscp_global


class TestUnconfigureDscpGlobal(unittest.TestCase):

    def test_unconfigure_dscp_global(self):
        self.device = Mock()
        unconfigure_dscp_global(self.device, '10', '20')
        self.device.configure.assert_called_with([
            'no radius-server dscp auth 10',
            'no radius-server dscp acct 20'
        ])
