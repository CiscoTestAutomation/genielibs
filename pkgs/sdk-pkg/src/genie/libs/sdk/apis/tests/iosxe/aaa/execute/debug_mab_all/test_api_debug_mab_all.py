import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.execute import debug_mab_all


class TestDebugMabAll(unittest.TestCase):

    def test_debug_mab_all_enable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_mab_all(device)
        device.execute.assert_called_once_with("debug mab all")

    def test_debug_mab_all_disable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_mab_all(device, enable=False)
        device.execute.assert_called_once_with("no debug mab all")


if __name__ == "__main__":
    unittest.main()
