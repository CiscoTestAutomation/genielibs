import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.logging.configure import (
    configure_login_log,
)


class TestConfigureLoginLog(TestCase):

    def test_configure_login_log(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_login_log(
            device,
            "on-success",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "login on-success log",
        )


if __name__ == "__main__":
    unittest.main()
