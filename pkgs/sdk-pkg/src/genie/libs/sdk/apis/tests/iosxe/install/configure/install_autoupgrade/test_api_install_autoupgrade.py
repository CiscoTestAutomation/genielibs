import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.install.configure import install_autoupgrade


class TestInstallAutoupgrade(TestCase):

    def test_install_autoupgrade(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = install_autoupgrade(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual("install autoupgrade", sent_command)


if __name__ == "__main__":
    unittest.main()