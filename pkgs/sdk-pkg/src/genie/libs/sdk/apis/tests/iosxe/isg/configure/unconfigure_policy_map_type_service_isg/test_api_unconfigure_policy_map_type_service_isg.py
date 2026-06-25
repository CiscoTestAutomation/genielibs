from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import unconfigure_policy_map_type_service_isg


class TestUnconfigurePolicyMapTypeServiceIsg(TestCase):

    def test_unconfigure_policy_map_type_service_isg(self):
        self.device = Mock()
        unconfigure_policy_map_type_service_isg(self.device, 'service3')
        self.device.configure.assert_called_once_with(
            "no policy-map type service service3"
        )

    def test_unconfigure_policy_map_type_service_isg_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_policy_map_type_service_isg(self.device, 'service3')
