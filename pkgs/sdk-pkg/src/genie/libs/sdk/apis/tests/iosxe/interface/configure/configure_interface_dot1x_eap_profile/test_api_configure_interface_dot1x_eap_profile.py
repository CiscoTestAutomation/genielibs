import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_dot1x_eap_profile,
)


class TestConfigureInterfaceDot1xEapProfile(TestCase):

    def test_configure_interface_dot1x_eap_profile(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_dot1x_eap_profile(
            device,
            "GigabitEthernet1/0/3",
            "md5",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/3", sent_commands)
        self.assertIn("dot1x supplicant eap profile md5", sent_commands)


if __name__ == "__main__":
    unittest.main()