import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_network


class TestConfigureAaaAuthorizationNetwork(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_authorization_network(self):
        configure_aaa_authorization_network(self.device, 'cts-mlist', 'CTS-group')
        self.device.configure.assert_called_once_with(
            'aaa authorization network cts-mlist group CTS-group'
        )
