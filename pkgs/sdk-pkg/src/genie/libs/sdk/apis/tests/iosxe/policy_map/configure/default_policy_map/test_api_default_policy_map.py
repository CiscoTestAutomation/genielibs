from unittest import TestCase
from genie.libs.sdk.apis.iosxe.policy_map.configure import default_policy_map
from unittest.mock import Mock


class TestDefaultPolicyMap(TestCase):

    def test_default_policy_map(self):
        self.device = Mock()
        result = default_policy_map(self.device, 'system-cpp-policy', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('default policy-map system-cpp-policy',)
        )

    def test_default_policy_map_with_policy_type(self):
        self.device = Mock()
        result = default_policy_map(self.device, 'abc', 'control')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('default policy-map type control subscriber abc',)
        )