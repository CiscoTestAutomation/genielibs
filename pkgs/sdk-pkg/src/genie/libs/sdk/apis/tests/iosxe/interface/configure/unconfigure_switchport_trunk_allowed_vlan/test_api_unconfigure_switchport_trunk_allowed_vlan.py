import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_switchport_trunk_allowed_vlan,
)


class TestUnconfigureSwitchportTrunkAllowedVlan(TestCase):

    def test_unconfigure_switchport_trunk_allowed_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_switchport_trunk_allowed_vlan(
            device,
            "TwentyFiveGigE1/0/37",
            "500",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["interface TwentyFiveGigE1/0/37", "no switchport trunk allowed vlan 500"]
        )


if __name__ == "__main__":
    unittest.main()