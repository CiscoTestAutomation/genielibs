import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ip_ospf_mtu_ignore,
)


class TestUnconfigureIpOspfMtuIgnore(TestCase):

    def test_unconfigure_ip_ospf_mtu_ignore(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ip_ospf_mtu_ignore(device, "Vlan1001")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface Vlan1001",
                "no ip ospf mtu-ignore",
            ],
        )


if __name__ == "__main__":
    unittest.main()
