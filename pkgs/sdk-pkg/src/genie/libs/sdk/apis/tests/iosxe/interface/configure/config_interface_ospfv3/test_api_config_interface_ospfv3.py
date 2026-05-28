import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import config_interface_ospfv3


class TestConfigInterfaceOspfv3(TestCase):

    def test_config_interface_ospfv3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3(
            device,
            "Virtual-Template1",
            1,
            0,
            True,
            True,
            None,
            0,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Virtual-Template1", sent_commands)
        self.assertIn("ospfv3 1 ipv4 area 0", sent_commands)
        self.assertIn("ospfv3 1 ipv6 area 0", sent_commands)


if __name__ == "__main__":
    unittest.main()