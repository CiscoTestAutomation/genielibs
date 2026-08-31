import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.logging.configure import (
    configure_lineconsole_exectimeout,
)


class TestConfigureLineconsoleExectimeout(TestCase):

    def test_configure_lineconsole_exectimeout(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lineconsole_exectimeout(
            device,
            0,
            0,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "line console 0",
                "exec-timeout 0",
            ],
        )


if __name__ == "__main__":
    unittest.main()
