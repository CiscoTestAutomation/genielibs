import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_switchport_nonegotiate,
)


class TestUnconfigureSwitchportNonegotiate(TestCase):

    def test_unconfigure_switchport_nonegotiate(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_switchport_nonegotiate(
            device,
            "Gi1/0/3",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["interface Gi1/0/3", "no switchport nonegotiate"]
        )


if __name__ == "__main__":
    unittest.main()