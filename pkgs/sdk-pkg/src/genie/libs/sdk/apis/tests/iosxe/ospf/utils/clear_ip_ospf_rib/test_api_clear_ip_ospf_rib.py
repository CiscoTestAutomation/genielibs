import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.utils import (
    clear_ip_ospf_rib,
)


class TestClearIpOspfRib(TestCase):

    def test_clear_ip_ospf_rib(self):
        device = Mock()
        device.execute.return_value = None

        result = clear_ip_ospf_rib(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "clear ip ospf rib")


if __name__ == "__main__":
    unittest.main()
