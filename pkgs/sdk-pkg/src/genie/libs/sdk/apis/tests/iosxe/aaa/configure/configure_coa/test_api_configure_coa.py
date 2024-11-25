import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_coa


class TestConfigureCoa(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_coa(self):
        configure_coa(self.device, {'hostname': '100.8.12.110', 'server_key': 'cisco123', 'vrf': 'cwa'})
        self.device.configure.assert_called_once_with([
            'aaa server radius dynamic-author',
            'client 100.8.12.110 vrf cwa server-key cisco123'
        ])
