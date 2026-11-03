import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ospf_cost,
)


class TestUnconfigureOspfCost(TestCase):

    def test_unconfigure_ospf_cost(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ospf_cost(device, "Te3/0/5", "10")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface Te3/0/5",
                "no ip ospf cost 10",
            ],
        )


if __name__ == "__main__":
    unittest.main()
