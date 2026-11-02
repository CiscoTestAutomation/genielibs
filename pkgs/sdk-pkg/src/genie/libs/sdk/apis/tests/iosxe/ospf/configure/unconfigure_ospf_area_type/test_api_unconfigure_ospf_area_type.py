import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ospf_area_type,
)


class TestUnconfigureOspfAreaType(TestCase):

    def test_unconfigure_ospf_area_type(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ospf_area_type(device, 1, 5, "nssa")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "router ospf 1",
                "no area 5 nssa",
            ],
        )


if __name__ == "__main__":
    unittest.main()
