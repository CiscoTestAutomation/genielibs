import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_auth_proxy


class TestUnconfigureAaaAuthProxy(unittest.TestCase):

    def test_unconfigure_aaa_auth_proxy(self):
        self.device = Mock()
        unconfigure_aaa_auth_proxy(self.device, 'ISEGRP')
        self.device.configure.assert_called_with([
            'no aaa authorization auth-proxy default group ISEGRP'            
        ])
