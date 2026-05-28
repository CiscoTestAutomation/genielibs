import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import config_enable_ip_routing


class TestConfigEnableIpRouting(TestCase):

    def test_config_enable_ip_routing(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_enable_ip_routing(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual("ip routing", sent_commands)


if __name__ == "__main__":
    unittest.main()