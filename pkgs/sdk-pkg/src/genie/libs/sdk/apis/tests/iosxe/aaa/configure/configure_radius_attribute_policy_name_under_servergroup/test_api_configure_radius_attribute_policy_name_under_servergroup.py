from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_attribute_policy_name_under_servergroup


class TestConfigureRadiusAttributePolicyNameUnderServergroup(TestCase):

    def test_configure_radius_attribute_policy_name_under_servergroup(self):
        device = Mock()

        result = configure_radius_attribute_policy_name_under_servergroup(
            device,
            "ISEGRP",
            "e8eb.340a.c100:ABCD",
            "access",
        )
        expected_output = None
        self.assertEqual(result, expected_output)

        # The API calls device.configure() with a list of commands (not a single string)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "aaa group server radius ISEGRP",
                "attribute policy-name e8eb.340a.c100:ABCD include-in-access-req",
            ],)
        )