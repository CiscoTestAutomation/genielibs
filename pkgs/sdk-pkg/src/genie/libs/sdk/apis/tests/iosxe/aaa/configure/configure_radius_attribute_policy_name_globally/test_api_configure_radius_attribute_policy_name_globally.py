from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_attribute_policy_name_globally
from unittest.mock import Mock


class TestConfigureRadiusAttributePolicyNameGlobally(TestCase):

    def test_configure_radius_attribute_policy_name_globally(self):
        self.device = Mock()
        configure_radius_attribute_policy_name_globally(self.device, 'e8eb.340a.c100:ABCD', 'access')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('radius-server attribute policy-name e8eb.340a.c100:ABCD include-in-access-req',)
        )

