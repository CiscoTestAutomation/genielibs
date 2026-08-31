import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    unconfigure_mtc_parameters,
)


class TestUnconfigureMtcParameters(TestCase):

    def test_unconfigure_mtc_parameters(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mtc_parameters(
            device,
            "ipv4",
            "HundredGigE1/0/4",
            ["http", "snmp"],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "mgmt-traffic control ipv4",
                "no interface HundredGigE1/0/4",
                "no protocol http",
                "no protocol snmp",
            ],
        )


if __name__ == "__main__":
    unittest.main()
