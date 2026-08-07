import unittest
from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.aaa.configure import (
    unconfigure_aaa_authentication_login,
)


class TestUnconfigureAaaAuthenticationLogin(TestCase):

    def test_unconfigure_aaa_authentication_login(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_aaa_authentication_login(
            device,
            "CONSOLE",
            "none",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no aaa authentication login CONSOLE none"
        )

    def test_unconfigure_aaa_authentication_login_with_group(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_aaa_authentication_login(
            device,
            "CONSOLE",
            "group",
            "RADIUS",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no aaa authentication login CONSOLE group RADIUS"
        )

    def test_unconfigure_aaa_authentication_login_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            unconfigure_aaa_authentication_login(device, "CONSOLE", "none")


if __name__ == "__main__":
    unittest.main()
