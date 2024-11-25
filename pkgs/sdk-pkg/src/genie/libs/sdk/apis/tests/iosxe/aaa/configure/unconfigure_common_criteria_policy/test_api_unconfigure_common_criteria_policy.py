import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_common_criteria_policy


class TestUnconfigureCommonCriteriaPolicy(unittest.TestCase):

    def test_unconfigure_common_criteria_policy(self):
        self.device = Mock()
        self.device.configure.return_value = "no aaa common-criteria policy enable_test"
        unconfigure_common_criteria_policy(device=self.device, policy_name='enable_test')
        self.device.configure.assert_called_with(
            'no aaa common-criteria policy enable_test'
        )
