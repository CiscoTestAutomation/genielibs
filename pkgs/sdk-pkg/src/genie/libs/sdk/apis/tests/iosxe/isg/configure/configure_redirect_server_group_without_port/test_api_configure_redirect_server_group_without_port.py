from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.isg.configure import (
    configure_redirect_server_group_without_port,
)


class TestConfigureRedirectServerGroupWithoutPort(TestCase):

    def test_configure_redirect_server_group_without_port(self):
        device = Mock()
        configure_redirect_server_group_without_port(
            device, 'SMTP_REDIRECT_GROUP', '10.1.1.1',
        )

        device.configure.assert_called_once_with([
            "redirect server-group SMTP_REDIRECT_GROUP",
            " server ip 10.1.1.1",
        ])

    def test_configure_redirect_server_group_without_port_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_redirect_server_group_without_port(
                device, 'SMTP_REDIRECT_GROUP', '10.1.1.1',
            )
