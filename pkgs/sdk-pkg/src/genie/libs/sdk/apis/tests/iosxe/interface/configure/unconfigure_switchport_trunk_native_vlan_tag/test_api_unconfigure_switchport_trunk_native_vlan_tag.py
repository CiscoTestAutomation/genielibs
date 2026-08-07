import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_switchport_trunk_native_vlan_tag,
)


class TestUnconfigureSwitchportTrunkNativeVlanTag(TestCase):

    def test_unconfigure_switchport_trunk_native_vlan_tag(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_switchport_trunk_native_vlan_tag(
            device,
            "GigabitEthernet1/0/10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["interface GigabitEthernet1/0/10", "no switchport trunk native vlan tag"]
        )


if __name__ == "__main__":
    unittest.main()