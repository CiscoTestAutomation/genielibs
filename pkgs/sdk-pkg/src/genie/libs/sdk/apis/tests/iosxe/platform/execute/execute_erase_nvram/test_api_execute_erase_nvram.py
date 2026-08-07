from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.execute import (
    execute_erase_nvram,
    execute_erase_nvram_all,
)
from unicon.core.errors import SubCommandFailure


class TestExecuteEraseNvram(TestCase):

    def test_execute_erase_nvram(self):
        device = Mock()
        device.execute.error_pattern = []
        device.execute.return_value = (
            "Erasing the nvram filesystem will remove all configuration files! "
            "Continue? [confirm]\n[OK]\nErase of nvram: complete"
        )
        result = execute_erase_nvram(device)
        self.assertEqual(device.execute.call_args.args[0], "erase nvram:")
        self.assertIn("[OK]", result)
        self.assertIn("Erase of nvram: complete", result)

    def test_execute_erase_nvram_failure(self):
        device = Mock()
        device.execute.error_pattern = []
        device.execute.return_value = "Unexpected output"
        with self.assertRaises(SubCommandFailure):
            execute_erase_nvram(device)

    def test_execute_erase_nvram_all(self):
        device = Mock()
        device.execute.error_pattern = []
        device.execute.return_value = (
            "Erasing the nvram filesystem will remove all files! "
            "Continue? [confirm]\n[OK]\nErase of nvram: complete"
        )
        result = execute_erase_nvram_all(device)
        self.assertEqual(device.execute.call_args.args[0], "erase /all nvram:")
        self.assertIn("[OK]", result)
        self.assertIn("Erase of nvram: complete", result)

    def test_execute_erase_nvram_all_failure(self):
        device = Mock()
        device.execute.error_pattern = []
        device.execute.return_value = "Unexpected output"
        with self.assertRaises(SubCommandFailure):
            execute_erase_nvram_all(device)
