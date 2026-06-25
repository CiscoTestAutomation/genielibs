import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_ip_dlep


class TestConfigureIpDlep(TestCase):

    def test_configure_ip_dlep(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_dlep(
            device,
            "GigabitEthernet2",
            1,
            None,
            None,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet2", sent_commands)
        self.assertIn("ip dlep vtemplate 1", sent_commands)


if __name__ == "__main__":
    unittest.main()