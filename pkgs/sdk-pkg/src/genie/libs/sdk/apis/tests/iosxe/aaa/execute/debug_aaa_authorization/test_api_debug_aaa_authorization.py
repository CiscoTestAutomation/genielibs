import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.execute import (
    debug_aaa_authorization,
)


class TestDebugAaaAuthorization(unittest.TestCase):

    def test_debug_aaa_authorization_enable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_aaa_authorization(device)
        device.execute.assert_called_once_with(
            "debug aaa authorization")

    def test_debug_aaa_authorization_disable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_aaa_authorization(device, enable=False)
        device.execute.assert_called_once_with(
            "no debug aaa authorization")


if __name__ == "__main__":
    unittest.main()
