from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.simulator.execute import (
    execute_show_simulator_radius_server_all,
)


class TestExecuteShowSimulatorRadiusServerAll(TestCase):

    def test_execute_show_simulator_radius_server_all(self):
        self.device = Mock()
        self.device.execute.return_value = "server output"

        output = execute_show_simulator_radius_server_all(self.device)

        self.assertEqual(output, "server output")
        self.device.execute.assert_called_once_with(
            "show simulator radius server all"
        )

    def test_execute_show_simulator_radius_server_all_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            execute_show_simulator_radius_server_all(self.device)
