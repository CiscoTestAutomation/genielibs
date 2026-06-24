import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_pppoe_enable_interface


class TestConfigurePppoeEnableInterface(TestCase):

    def test_configure_pppoe_enable_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_pppoe_enable_interface(
            device,
            "Ethernet0/2/0",
            "global",
            "100",
            "1590",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Ethernet0/2/0",
                "pppoe enable group global",
                "pppoe-client dial-pool-number 100",
                "pppoe-client ppp-max-payload 1590",
            ],
        )


if __name__ == "__main__":
    unittest.main()