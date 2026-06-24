from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import unconfigure_policy_map_type_control


class TestUnconfigurePolicyMapTypeControl(TestCase):

    def test_unconfigure_policy_map_type_control(self):
        self.device = Mock()
        unconfigure_policy_map_type_control(self.device, 'IT')
        self.device.configure.assert_called_once_with(
            "no policy-map type control IT"
        )

    def test_unconfigure_policy_map_type_control_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_policy_map_type_control(self.device, 'IT')
