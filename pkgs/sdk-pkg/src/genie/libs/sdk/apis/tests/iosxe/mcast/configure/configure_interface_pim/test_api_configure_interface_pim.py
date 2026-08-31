import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import configure_interface_pim


class TestConfigureInterfacePim(TestCase):

    def test_configure_interface_pim(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_pim(
            device=device,
            interface="loopback1",
            pim_mode="sparse-mode",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface loopback1",
                "ip pim sparse-mode",
            ],
        )


if __name__ == "__main__":
    unittest.main()
