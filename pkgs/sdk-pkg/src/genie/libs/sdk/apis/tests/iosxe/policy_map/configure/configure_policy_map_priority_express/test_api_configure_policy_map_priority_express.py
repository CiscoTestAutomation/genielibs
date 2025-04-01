from unittest import TestCase
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_priority_express
from unittest.mock import Mock


class TestConfigurePolicyMapPriorityExpress(TestCase):

    def test_configure_policy_map_priority_express(self):
        self.device = Mock()
        result = configure_policy_map_priority_express(self.device, 'pol_test', 'classa')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['policy-map pol_test', 'class classa', 'priority level 1 express'],)
        )
