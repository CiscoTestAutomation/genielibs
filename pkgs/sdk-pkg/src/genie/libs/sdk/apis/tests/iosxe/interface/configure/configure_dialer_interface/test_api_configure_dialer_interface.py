import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_dialer_interface


class TestConfigureDialerInterface(TestCase):

    def test_configure_dialer_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_dialer_interface(
            device,
            "Dialer10",
            "ppp",
            "chap",
            "negotiated",
            "10",
            None,
            None,
            None,
            None,
            None,
            False,
            True,
            True,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Dialer10", sent_commands)
        self.assertIn("encapsulation ppp", sent_commands)
        self.assertIn("no shutdown", sent_commands)
        self.assertIn("dialer pool 10", sent_commands)
        self.assertIn("ip address negotiated", sent_commands)
        self.assertIn("ppp authentication chap callin", sent_commands)
        self.assertIn("dialer down-with-vInterface", sent_commands)
        self.assertIn("ppp mtu adaptive", sent_commands)
        self.assertIn("ppp ipcp address required", sent_commands)


if __name__ == "__main__":
    unittest.main()