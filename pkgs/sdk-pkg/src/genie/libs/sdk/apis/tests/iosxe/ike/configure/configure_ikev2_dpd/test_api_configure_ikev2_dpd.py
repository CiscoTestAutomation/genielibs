import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_dpd


class TestConfigureIkev2Dpd(TestCase):

    def test_configure_ikev2_dpd(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_dpd(device, 20, 5, "on-demand")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 dpd 20 5 on-demand", sent_commands)


if __name__ == "__main__":
    unittest.main()