import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_redistribute_eigrp_under_ospf,
)


class TestUnconfigureRedistributeEigrpUnderOspf(TestCase):

    def test_unconfigure_redistribute_eigrp_under_ospf(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_redistribute_eigrp_under_ospf(device, 1, 1, None)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "router ospf 1",
                "no redistribute eigrp 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
