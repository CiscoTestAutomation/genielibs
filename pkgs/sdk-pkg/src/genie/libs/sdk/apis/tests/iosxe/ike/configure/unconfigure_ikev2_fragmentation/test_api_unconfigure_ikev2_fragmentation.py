import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_ikev2_fragmentation


class TestUnconfigureIkev2Fragmentation(TestCase):

    def test_unconfigure_ikev2_fragmentation(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ikev2_fragmentation(device, 1500)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("no crypto ikev2 fragmentation mtu 1500", sent_commands)


if __name__ == "__main__":
    unittest.main()