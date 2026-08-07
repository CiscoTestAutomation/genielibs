import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_nsf_xfsu


class TestConfigureIsisNsfXfsu(TestCase):

    def test_configure_isis_nsf_xfsu(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_nsf_xfsu(
            device,
            "49.1290.0000.0014.00",
            "1",
            "loopback0",
            "wide",
            "ietf",
            "connected",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis 1",
                "net 49.1290.0000.0014.00",
                "router-id loopback0",
                "metric-style wide",
                "nsf ietf",
                "redistribute connected",
            ],
        )


if __name__ == "__main__":
    unittest.main()