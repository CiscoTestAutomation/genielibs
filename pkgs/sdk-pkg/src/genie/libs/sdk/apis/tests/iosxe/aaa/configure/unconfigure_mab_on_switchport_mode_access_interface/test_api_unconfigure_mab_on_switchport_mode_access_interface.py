from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import (
    unconfigure_mab_on_switchport_mode_access_interface,
)


class TestUnconfigureMabOnSwitchportModeAccessInterface(TestCase):

    def test_unconfigure_mab_on_switchport_mode_access_interface(self):
        device = Mock()
        device.configure.return_value = ""

        result = unconfigure_mab_on_switchport_mode_access_interface(
            device, "TenGigabitEthernet1/2/0/2"
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "interface TenGigabitEthernet1/2/0/2",
                "no mab",
            ],)
        )