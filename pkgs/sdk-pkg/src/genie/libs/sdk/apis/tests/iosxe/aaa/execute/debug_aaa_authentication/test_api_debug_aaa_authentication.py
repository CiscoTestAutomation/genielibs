import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.execute import (
    debug_aaa_authentication,
)


class TestDebugAaaAuthentication(unittest.TestCase):

    def test_debug_aaa_authentication_enable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_aaa_authentication(device)
        device.execute.assert_called_once_with(
            "debug aaa authentication")

    def test_debug_aaa_authentication_disable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_aaa_authentication(device, enable=False)
        device.execute.assert_called_once_with(
            "no debug aaa authentication")


if __name__ == "__main__":
    unittest.main()
