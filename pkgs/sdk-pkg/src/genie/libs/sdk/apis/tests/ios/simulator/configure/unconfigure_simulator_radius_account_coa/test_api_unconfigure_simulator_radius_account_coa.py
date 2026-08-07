from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.simulator.configure import (
    unconfigure_simulator_radius_account_coa
)


class TestUnconfigureSimulatorRadiusAccountCoa(TestCase):

    def test_unconfigure_simulator_radius_account_coa(self):
        self.device = Mock()
        unconfigure_simulator_radius_account_coa(self.device)
        self.device.configure.assert_called_once_with(
            "no simulator radius account-coa"
        )

    def test_unconfigure_simulator_radius_account_coa_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_simulator_radius_account_coa(self.device)
