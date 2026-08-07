import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.execute import (
    debug_access_session_all,
)


class TestDebugAccessSessionAll(unittest.TestCase):

    def test_debug_access_session_all_enable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_access_session_all(device)
        device.execute.assert_called_once_with(
            "debug access-session all")

    def test_debug_access_session_all_disable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_access_session_all(device, enable=False)
        device.execute.assert_called_once_with(
            "no debug access-session all")


if __name__ == "__main__":
    unittest.main()
