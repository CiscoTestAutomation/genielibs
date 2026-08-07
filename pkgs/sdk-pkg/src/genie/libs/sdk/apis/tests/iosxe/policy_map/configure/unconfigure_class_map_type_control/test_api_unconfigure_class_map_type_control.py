import unittest
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_class_map_type_control,
)


class TestUnconfigureClassMapTypeControl(unittest.TestCase):

    def test_unconfigure_class_map_type_control(self):
        device = Mock()

        unconfigure_class_map_type_control(
            device,
            class_name="ISG-IP-UNAUTH",
            match_type="match-all",
        )

        device.configure.assert_called_once_with(
            "no class-map type control match-all ISG-IP-UNAUTH"
        )

    def test_unconfigure_class_map_type_control_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            unconfigure_class_map_type_control(
                device,
                class_name="ISG-IP-UNAUTH",
            )


if __name__ == "__main__":
    unittest.main()
