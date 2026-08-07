import unittest
from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.aaa.configure import (
    configure_aaa_authentication_login,
)


class TestConfigureAaaAuthenticationLogin(TestCase):

    def test_configure_aaa_authentication_login(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_aaa_authentication_login(
            device,
            "CONSOLE",
            "none",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "aaa authentication login CONSOLE none"
        )

    def test_configure_aaa_authentication_login_with_group(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_aaa_authentication_login(
            device,
            "CONSOLE",
            "group",
            "RADIUS",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "aaa authentication login CONSOLE group RADIUS"
        )

    def test_configure_aaa_authentication_login_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            configure_aaa_authentication_login(device, "CONSOLE", "none")


if __name__ == "__main__":
    unittest.main()
