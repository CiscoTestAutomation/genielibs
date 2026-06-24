import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import unconfigure_policy_map_type_control_isg
from unicon.core.errors import SubCommandFailure


class TestUnconfigurePolicyMapTypeControlIsg(unittest.TestCase):

    def test_unconfigure(self):
        device = Mock()
        unconfigure_policy_map_type_control_isg(device, 'IT')
        device.configure.assert_called_once_with(
            'no policy-map type control IT'
        )

    def test_unconfigure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_policy_map_type_control_isg(device, 'IT')


if __name__ == '__main__':
    unittest.main()
