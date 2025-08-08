from unittest import TestCase
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_priority_express
from unittest.mock import Mock


class TestConfigurePolicyMapPriorityExpress(TestCase):


    def test_configure_policy_map_priority_express(self):
        self.device = Mock()
        result = configure_policy_map_priority_express(self.device, 'pol', 'class-default', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['policy-map pol', 'class class-default', 'priority level 1 express'],)
        )


    def test_configure_policy_map_priority_express_bandwidth(self):
        self.device = Mock()
        result = configure_policy_map_priority_express(self.device, 'pol', 'class-default', '1000', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['policy-map pol', 'class class-default', 'priority level 1 express 1000'],)
        )
    def test_configure_policy_map_priority_express_percent(self):
        self.device = Mock()
        result = configure_policy_map_priority_express(self.device, 'pol', 'class-default', None, '50')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['policy-map pol', 'class class-default', 'priority level 1 express percent 50'],)
        )
