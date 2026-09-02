import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    configure_interface_default_snmp,
)


class TestConfigureInterfaceDefaultSnmp(TestCase):

    def test_configure_interface_default_snmp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_default_snmp(
            device,
            "Te3/1/5",
            "removed",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Te3/1/5",
                "default snmp trap mac-notification change removed",
            ],
        )


if __name__ == "__main__":
    unittest.main()
