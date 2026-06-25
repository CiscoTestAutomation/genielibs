import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_nonegotiate


class TestConfigureSwitchportNonegotiate(TestCase):

    def test_configure_switchport_nonegotiate(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_switchport_nonegotiate(
            device,
            "Gi1/0/3",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Gi1/0/3",
                "switchport nonegotiate",
            ],
        )


if __name__ == "__main__":
    unittest.main()