import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.execute import debug_epm_all


class TestDebugEpmAll(unittest.TestCase):

    def test_debug_epm_all_enable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_epm_all(device)
        device.execute.assert_called_once_with("debug epm all")

    def test_debug_epm_all_disable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_epm_all(device, enable=False)
        device.execute.assert_called_once_with("no debug epm all")


if __name__ == "__main__":
    unittest.main()
