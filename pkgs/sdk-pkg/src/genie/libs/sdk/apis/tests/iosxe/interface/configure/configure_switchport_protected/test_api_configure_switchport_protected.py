import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_protected


class TestConfigureSwitchportProtected(TestCase):

    def test_configure_switchport_protected(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_switchport_protected(
            device,
            "Gi1/0/5",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Gi1/0/5",
                "switchport protected",
            ],
        )


if __name__ == "__main__":
    unittest.main()