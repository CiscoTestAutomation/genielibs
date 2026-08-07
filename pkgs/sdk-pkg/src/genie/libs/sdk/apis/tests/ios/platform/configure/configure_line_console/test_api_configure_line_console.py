from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.ios.platform.configure import (
    configure_line_console,
)


class TestConfigureLineConsole(TestCase):

    def test_configure_line_console_all_options(self):
        self.device = Mock()
        configure_line_console(
            self.device,
            0,
            exec_timeout_minutes=0,
            exec_timeout_seconds=0,
            login_authentication='CONSOLE',
        )
        self.device.configure.assert_called_once_with(
            [
                "line console 0",
                " exec-timeout 0 0",
                " login authentication CONSOLE",
            ]
        )

    def test_configure_line_console_minimal(self):
        self.device = Mock()
        configure_line_console(self.device, 0)
        self.device.configure.assert_called_once_with(
            ["line console 0"]
        )

    def test_configure_line_console_with_password(self):
        self.device = Mock()
        configure_line_console(
            self.device,
            0,
            password='cisco',
            transport_input='all',
        )
        self.device.configure.assert_called_once_with(
            [
                "line console 0",
                " password cisco",
                " transport input all",
            ]
        )
