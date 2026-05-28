from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.simulator.execute import execute_clear


class TestExecuteClear(TestCase):

    def test_execute_clear_simulator_radius_request(self):
        self.device = Mock()
        execute_clear(self.device, 'simulator radius request all')
        self.device.execute.assert_called_once_with(
            "clear simulator radius request all"
        )

    def test_execute_clear_simulator_radius_subscriber(self):
        self.device = Mock()
        execute_clear(self.device, 'simulator radius subscriber 1')
        self.device.execute.assert_called_once_with(
            "clear simulator radius subscriber 1"
        )

    def test_execute_clear_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            execute_clear(self.device, 'simulator radius request all')
