import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_subinterface


class TestUnconfigureSubinterface(TestCase):

    def test_unconfigure_subinterface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_subinterface(
            device,
            "TenGigabitEthernet1/2/0/19",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["no interface TenGigabitEthernet1/2/0/19.1"]
        )


if __name__ == "__main__":
    unittest.main()