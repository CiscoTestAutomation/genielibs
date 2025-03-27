from unittest import TestCase
from genie.libs.sdk.apis.iosxe.policy_map.configure import unconfigure_policy_map_priority_express
from unittest.mock import Mock


class TestUnconfigurePolicyMapPriorityExpress(TestCase):

    def test_unconfigure_policy_map_priority_express(self):
        self.device = Mock()
        result = unconfigure_policy_map_priority_express(self.device, 'pol_test', 'classa')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['policy-map pol_test', 'class classa', 'no priority level 1 express'],)
        )
