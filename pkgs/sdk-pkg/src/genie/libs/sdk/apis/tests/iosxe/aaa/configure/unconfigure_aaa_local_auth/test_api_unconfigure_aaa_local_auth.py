import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_local_auth


class TestUnconfigureAaaLocalAuth(unittest.TestCase):

    def test_unconfigure_aaa_local_auth(self):
        self.device = Mock()
        unconfigure_aaa_local_auth(self.device)
        self.device.configure.assert_called_with([
            'no aaa authorization network default local',
            'no aaa local authentication default authorization default',
            'no aaa authentication dot1x default local'
        ])
