from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import configure_redirect_server_group


class TestConfigureRedirectServerGroup(TestCase):

    def test_configure_redirect_server_group_with_servers(self):
        self.device = Mock()
        configure_redirect_server_group(
            self.device, 'REDIRECT_V4',
            servers=[{'ip': '10.0.0.1', 'port': 80}]
        )
        self.device.configure.assert_called_once_with(
            [
                "redirect server-group REDIRECT_V4",
                " server ip 10.0.0.1 port 80",
            ]
        )

    def test_configure_redirect_server_group_no_servers(self):
        self.device = Mock()
        configure_redirect_server_group(self.device, 'REDIRECT_V4')
        self.device.configure.assert_called_once_with(
            ["redirect server-group REDIRECT_V4"]
        )

    def test_configure_redirect_server_group_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_redirect_server_group(self.device, 'REDIRECT_V4')
