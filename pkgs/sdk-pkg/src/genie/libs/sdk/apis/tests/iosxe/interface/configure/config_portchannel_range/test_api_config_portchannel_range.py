import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import config_portchannel_range


class TestConfigPortchannelRange(TestCase):

    def test_config_portchannel_range(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_portchannel_range(
            device=device,
            portchannel_start="10",
            portchannel_end="20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            "interface range port-channel 10 - 20",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()