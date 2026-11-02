import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_interface_ospfv3_ipsec_esp,
)


class TestUnconfigureInterfaceOspfv3IpsecEsp(TestCase):

    def test_unconfigure_interface_ospfv3_ipsec_esp(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_interface_ospfv3_ipsec_esp(
            device,
            "TenGigabitEthernet1/0/41",
            25604,
            "aes-cbc",
            "1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78",
            "md5",
            "1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78",
            128,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface TenGigabitEthernet1/0/41",
                "no ospfv3 encryption ipsec spi 25604 esp aes-cbc 128 "
                "1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78 md5 "
                "1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78",
            ],
        )


if __name__ == "__main__":
    unittest.main()
