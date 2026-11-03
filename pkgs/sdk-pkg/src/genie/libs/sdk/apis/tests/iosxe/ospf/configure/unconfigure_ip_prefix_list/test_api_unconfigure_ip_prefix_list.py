import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ip_prefix_list,
)


class TestUnconfigureIpPrefixList(TestCase):

    def test_unconfigure_ip_prefix_list(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ip_prefix_list(device, "up", 1, "1.1.1.1", 32)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "no ip prefix-list up seq 1 permit 1.1.1.1/32",
        )


if __name__ == "__main__":
    unittest.main()
