import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_dscp_global


class TestConfigureDscpGlobal(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_dscp_global(self):
        result = configure_dscp_global(self.device, '50', '40')
        self.device.configure.assert_called_once_with([
            'radius-server dscp auth 50',
            'radius-server dscp acct 40'
        ])
