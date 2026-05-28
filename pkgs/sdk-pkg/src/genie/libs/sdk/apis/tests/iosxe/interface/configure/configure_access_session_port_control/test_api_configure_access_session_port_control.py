import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_access_session_port_control,
)


class TestConfigureAccessSessionPortControl(TestCase):

    def test_configure_access_session_port_control(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_access_session_port_control(
            device,
            " TenGigabitEthernet1/1/7",
            "auto",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface  TenGigabitEthernet1/1/7", sent_commands)
        self.assertIn("access-session port-control auto", sent_commands)


if __name__ == "__main__":
    unittest.main()