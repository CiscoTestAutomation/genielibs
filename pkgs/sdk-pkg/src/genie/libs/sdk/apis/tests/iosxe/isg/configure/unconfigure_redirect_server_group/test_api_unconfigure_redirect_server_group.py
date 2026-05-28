from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import unconfigure_redirect_server_group


class TestUnconfigureRedirectServerGroup(TestCase):

    def test_unconfigure_redirect_server_group(self):
        self.device = Mock()
        unconfigure_redirect_server_group(self.device, 'REDIRECT_V4')
        self.device.configure.assert_called_once_with(
            "no redirect server-group REDIRECT_V4"
        )

    def test_unconfigure_redirect_server_group_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_redirect_server_group(self.device, 'REDIRECT_V4')
