import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.bgp.clear import (
    clear_ip_bgp,
)


class TestClearIpBgp(TestCase):

    def test_clear_ip_bgp(self):
        device = Mock()
        device.execute.return_value = None

        result = clear_ip_bgp(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "clear ip bgp *")
        device.execute.assert_called_once_with(command)


if __name__ == "__main__":
    unittest.main()
