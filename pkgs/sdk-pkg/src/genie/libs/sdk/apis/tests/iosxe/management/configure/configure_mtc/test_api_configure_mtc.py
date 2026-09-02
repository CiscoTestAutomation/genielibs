import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_mtc,
)


class TestConfigureMtc(TestCase):

    def test_configure_mtc(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_mtc(
            device,
            "ipv4",
            "HundredGigE1/0/4",
            ["http", "ssh", "snmp"],
            "4.4.4.4",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "mgmt-traffic control ipv4",
                "interface HundredGigE1/0/4",
                "protocol http",
                "protocol ssh",
                "protocol snmp",
                "address 4.4.4.4",
            ],
        )


if __name__ == "__main__":
    unittest.main()
