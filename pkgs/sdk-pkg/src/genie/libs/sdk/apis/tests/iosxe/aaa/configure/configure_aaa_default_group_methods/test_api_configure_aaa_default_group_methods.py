import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_default_group_methods


class TestConfigureAaaDefaultGroupMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_default_group_methods(self):
        configure_aaa_default_group_methods(self.device, 'group', 'ISEGRP')
        self.device.configure.assert_called_once_with([
            'aaa authentication dot1x default group ISEGRP',
            'aaa authorization network default group ISEGRP',
            'aaa authorization network MLIST group ISEGRP',
            'aaa authorization auth-proxy default group ISEGRP',
            'aaa accounting network default start-stop group ISEGRP'
        ])
