import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_switchport_protected,
)


class TestUnconfigureSwitchportProtected(TestCase):

    def test_unconfigure_switchport_protected(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_switchport_protected(
            device,
            "Gi1/0/5",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["interface Gi1/0/5", "no switchport protected"]
        )


if __name__ == "__main__":
    unittest.main()