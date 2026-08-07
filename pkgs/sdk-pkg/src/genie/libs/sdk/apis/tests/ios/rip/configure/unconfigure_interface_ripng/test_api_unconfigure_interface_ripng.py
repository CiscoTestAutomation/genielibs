import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.rip.configure import unconfigure_interface_ripng


class TestUnconfigureInterfaceRipng(TestCase):

    def test_unconfigure_interface_ripng(self):
        device = Mock()
        device.configure.return_value = None
        result = unconfigure_interface_ripng(device, "Virtual-Template1", "RIP")
        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            "interface Virtual-Template1",
            "no ipv6 rip RIP enable",
        ])

    def test_unconfigure_interface_ripng_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")
        with self.assertRaises(SubCommandFailure):
            unconfigure_interface_ripng(device, "Virtual-Template1", "RIP")


if __name__ == "__main__":
    unittest.main()
