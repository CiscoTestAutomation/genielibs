import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.nxos.mds.platform.execute import execute_delete_boot_variable


class TestExecuteDeleteBootVariable(unittest.TestCase):

    def test_execute_delete_boot_variable(self):
        device = Mock()
        device.name = 'II23-FCCORE'

        device.configure.return_value = None

        device.api.execute_copy_run_to_start.return_value = None
        device.api.is_current_boot_variable_as_expected.return_value = None

        result = execute_delete_boot_variable(device)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once_with(
            ['no boot system', 'no boot kickstart'], timeout=300
        )

        device.api.execute_copy_run_to_start.assert_called_once_with(
            command_timeout=300
        )
        device.api.is_current_boot_variable_as_expected.assert_called_once_with(
            device=device, system=None, kickstart=None
        )


if __name__ == '__main__':
    unittest.main()