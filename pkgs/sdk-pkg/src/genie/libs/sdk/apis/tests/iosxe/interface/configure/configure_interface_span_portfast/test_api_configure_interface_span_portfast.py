import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_span_portfast


class TestConfigureInterfaceSpanPortfast(TestCase):

    def test_configure_interface_span_portfast(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_span_portfast(
            device=device,
            interface="ten1/1/0/5",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface ten1/1/0/5", sent_commands)
        self.assertIn("spanning-tree portfast ", sent_commands)


if __name__ == "__main__":
    unittest.main()