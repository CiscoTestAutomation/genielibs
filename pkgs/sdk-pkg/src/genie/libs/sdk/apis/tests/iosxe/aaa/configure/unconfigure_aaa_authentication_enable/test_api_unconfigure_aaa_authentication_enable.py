import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_authentication_enable


class TestUnconfigureAaaAuthenticationEnable(unittest.TestCase):

    def test_unconfigure_aaa_authentication_enable(self):
        self.device = Mock()
        unconfigure_aaa_authentication_enable(self.device)
        self.device.configure.assert_called_with(
            'no aaa authentication enable default'
        )
