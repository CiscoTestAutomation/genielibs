import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_exec_default


class TestConfigureAaaAuthorizationExecDefault(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_authorization_exec_default(self):
        configure_aaa_authorization_exec_default(self.device, 'local', 'radius')
        self.device.configure.assert_called_once_with(
            'aaa authorization exec default local group radius'
        )
