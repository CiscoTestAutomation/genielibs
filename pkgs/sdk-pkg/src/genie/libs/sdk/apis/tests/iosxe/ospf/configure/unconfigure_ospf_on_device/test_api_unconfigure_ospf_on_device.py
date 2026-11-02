import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ospf_on_device,
)


class TestUnconfigureOspfOnDevice(TestCase):

    def test_unconfigure_ospf_on_device(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ospf_on_device(device, 200, "UNDERLAY")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "no router ospf 200 vrf UNDERLAY")


if __name__ == "__main__":
    unittest.main()
