import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.execute import (
    debug_radius_authentication,
)


class TestDebugRadiusAuthentication(unittest.TestCase):

    def test_debug_radius_authentication_enable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_radius_authentication(device)
        device.execute.assert_called_once_with(
            "debug radius authentication")

    def test_debug_radius_authentication_disable(self):
        device = Mock()
        device.execute = Mock(return_value="")
        debug_radius_authentication(device, enable=False)
        device.execute.assert_called_once_with(
            "no debug radius authentication")


if __name__ == "__main__":
    unittest.main()
