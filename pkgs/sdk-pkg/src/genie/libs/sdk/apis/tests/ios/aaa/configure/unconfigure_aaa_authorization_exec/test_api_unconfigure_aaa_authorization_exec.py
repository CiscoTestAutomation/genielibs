import unittest
from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.aaa.configure import (
    unconfigure_aaa_authorization_exec,
)


class TestUnconfigureAaaAuthorizationExec(TestCase):

    def test_unconfigure_aaa_authorization_exec(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_aaa_authorization_exec(
            device,
            "CONSOLE",
            "none",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no aaa authorization exec CONSOLE none"
        )

    def test_unconfigure_aaa_authorization_exec_with_group(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_aaa_authorization_exec(
            device,
            "CONSOLE",
            "group",
            "RADIUS",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no aaa authorization exec CONSOLE group RADIUS"
        )

    def test_unconfigure_aaa_authorization_exec_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            unconfigure_aaa_authorization_exec(device, "CONSOLE", "none")


if __name__ == "__main__":
    unittest.main()
