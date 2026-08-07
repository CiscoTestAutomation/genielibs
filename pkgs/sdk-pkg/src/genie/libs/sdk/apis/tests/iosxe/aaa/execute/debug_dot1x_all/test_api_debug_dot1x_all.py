import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.execute import debug_dot1x_all


class TestDebugDot1xAll(unittest.TestCase):

    def test_debug_dot1x_all_enable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_dot1x_all(device)
        device.execute.assert_called_once_with("debug dot1x all")

    def test_debug_dot1x_all_disable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_dot1x_all(device, enable=False)
        device.execute.assert_called_once_with("no debug dot1x all")


if __name__ == "__main__":
    unittest.main()
