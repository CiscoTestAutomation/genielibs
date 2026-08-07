import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    unconfigure_ospfv3_authentication_null,
)


class TestUnconfigureOspfv3AuthenticationNull(TestCase):

    def test_unconfigure_ospfv3_authentication_null(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ospfv3_authentication_null(
            device,
            "TenGigabitEthernet1/0/41",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TenGigabitEthernet1/0/41",
                "no ospfv3 authentication null",
            ],
        )


if __name__ == "__main__":
    unittest.main()
