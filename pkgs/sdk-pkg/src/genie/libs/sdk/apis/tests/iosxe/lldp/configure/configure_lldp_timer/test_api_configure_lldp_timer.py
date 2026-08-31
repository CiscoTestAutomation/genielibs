import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lldp.configure import (
    configure_lldp_timer,
)


class TestConfigureLldpTimer(TestCase):

    def test_configure_lldp_timer(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lldp_timer(
            device,
            18,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "lldp timer 18",
        )


if __name__ == "__main__":
    unittest.main()
