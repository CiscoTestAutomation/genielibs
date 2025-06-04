from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_attribute_policy_name_under_server
from unittest.mock import Mock


class TestConfigureRadiusAttributePolicyNameUnderServer(TestCase):

    def test_configure_radius_attribute_policy_name_under_server(self):
        self.device = Mock()
        configure_radius_attribute_policy_name_under_server(self.device, 'ISE', 'e8eb.340a.c100:ABCD', 'accounting')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server ISE', 'attribute policy-name e8eb.340a.c100:ABCD include-in-accounting-req'],)
        )

