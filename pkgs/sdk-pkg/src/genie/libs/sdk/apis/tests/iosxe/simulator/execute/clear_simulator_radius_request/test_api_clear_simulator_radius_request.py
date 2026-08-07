from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.simulator.execute import (
    execute_clear_simulator_radius_request,
    execute_clear_simulator_radius_testcase,
)


class TestClearSimulatorRadiusRequest(TestCase):

    def test_execute_clear_simulator_radius_request(self):
        device = Mock()

        result = execute_clear_simulator_radius_request(device)

        self.assertEqual(result, None)
        device.execute.assert_called_once_with(
            "clear simulator radius request all"
        )

    def test_execute_clear_simulator_radius_request_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            execute_clear_simulator_radius_request(device)

    def test_execute_clear_simulator_radius_testcase(self):
        device = Mock()

        result = execute_clear_simulator_radius_testcase(device)

        self.assertEqual(result, None)
        device.execute.assert_called_once_with(
            "clear simulator radius testcase all"
        )

    def test_execute_clear_simulator_radius_testcase_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            execute_clear_simulator_radius_testcase(device)
