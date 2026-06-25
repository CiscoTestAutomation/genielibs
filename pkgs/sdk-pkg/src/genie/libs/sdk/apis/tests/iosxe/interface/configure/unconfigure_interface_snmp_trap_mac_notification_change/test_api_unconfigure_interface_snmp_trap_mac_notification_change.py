import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_snmp_trap_mac_notification_change


class TestUnconfigureInterfaceSnmpTrapMacNotificationChange(TestCase):

    def test_unconfigure_interface_snmp_trap_mac_notification_change(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_snmp_trap_mac_notification_change(
            device,
            "te1/0/7",
            "added",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface te1/0/7",
                "no snmp trap mac-notification change added",
            ],
        )


if __name__ == "__main__":
    unittest.main()