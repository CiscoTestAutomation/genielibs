import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.install.configure import install_remove_version


class TestInstallRemoveVersion(TestCase):

    def test_install_remove_version(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = """
install_remove: START Wed Jul 13 11:39:04 IST 2022
install_remove: Removing IMG
Preparing packages list to remove ...

Do you want to remove the above files? [y/n]
"""

        result = install_remove_version(device, "17.10.01.0.162943", 60, 10)

        self.assertTrue(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            "install remove version 17.10.01.0.162943",
            sent_command,
        )


if __name__ == "__main__":
    unittest.main()