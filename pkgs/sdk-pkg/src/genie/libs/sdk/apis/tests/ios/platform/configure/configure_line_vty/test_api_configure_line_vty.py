from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.ios.platform.configure import (
    configure_line_vty,
)


class TestConfigureLineVty(TestCase):

    def test_configure_line_vty_all_options(self):
        self.device = Mock()
        configure_line_vty(
            self.device,
            0,
            4,
            password='cisco',
            login_authentication='CONSOLE',
            transport_input='all',
        )
        self.device.configure.assert_called_once_with(
            [
                "line vty 0 4",
                " password cisco",
                " login authentication CONSOLE",
                " transport input all",
            ]
        )

    def test_configure_line_vty_minimal(self):
        self.device = Mock()
        configure_line_vty(self.device, 0, 4)
        self.device.configure.assert_called_once_with(
            ["line vty 0 4"]
        )

    def test_configure_line_vty_with_exec_timeout(self):
        self.device = Mock()
        configure_line_vty(
            self.device,
            0,
            4,
            exec_timeout_minutes=5,
            exec_timeout_seconds=0,
            login_authentication='CONSOLE',
        )
        self.device.configure.assert_called_once_with(
            [
                "line vty 0 4",
                " exec-timeout 5 0",
                " login authentication CONSOLE",
            ]
        )
