import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ipv6_ospf_mtu_ignore,
)


class TestUnconfigureIpv6OspfMtuIgnore(TestCase):

    def test_unconfigure_ipv6_ospf_mtu_ignore(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ipv6_ospf_mtu_ignore(
            device=device,
            interface="Vlan3000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface Vlan3000",
                "no ipv6 ospf mtu-ignore",
            ],
        )


if __name__ == "__main__":
    unittest.main()
