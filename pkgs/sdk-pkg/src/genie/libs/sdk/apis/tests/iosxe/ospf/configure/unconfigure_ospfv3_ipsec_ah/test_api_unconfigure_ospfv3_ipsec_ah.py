import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ospfv3_ipsec_ah,
)


class TestUnconfigureOspfv3IpsecAh(TestCase):

    def test_unconfigure_ospfv3_ipsec_ah(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ospfv3_ipsec_ah(
            device,
            "1",
            "0",
            25605,
            "md5",
            "1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78",
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "router ospfv3 1",
                "no area 0 authentication ipsec spi 25605 md5 "
                "1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78",
            ],
        )


if __name__ == "__main__":
    unittest.main()
