from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_attribute_policy_name_under_servergroup



class TestUnconfigureRadiusAttributePolicyNameUnderServergroup(TestCase):

    def test_unconfigure_radius_attribute_policy_name_under_servergroup(self):
        device = Mock()
        device.configure.return_value = ""

        result = unconfigure_radius_attribute_policy_name_under_servergroup(
            device,
            "ISEGRP",
            "e8eb.340a.c100:ABCD",
            "accounting",
        )
        self.assertIsNone(result)

        # API is expected to call device.configure() with a list of commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "aaa group server radius ISEGRP",
                "no attribute policy-name e8eb.340a.c100:ABCD include-in-accounting-req",
            ],)
        )