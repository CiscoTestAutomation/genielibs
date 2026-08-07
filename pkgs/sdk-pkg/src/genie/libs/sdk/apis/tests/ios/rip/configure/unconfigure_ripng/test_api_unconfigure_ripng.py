import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.rip.configure import unconfigure_ripng


class TestUnconfigureRipng(TestCase):

    def test_unconfigure_ripng(self):
        device = Mock()
        device.configure.return_value = None
        result = unconfigure_ripng(device, "RIP")
        self.assertIsNone(result)
        device.configure.assert_called_once_with("no ipv6 router rip RIP")

    def test_unconfigure_ripng_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")
        with self.assertRaises(SubCommandFailure):
            unconfigure_ripng(device, "RIP")


if __name__ == "__main__":
    unittest.main()
