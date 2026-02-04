from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_attribute_policy_name_under_server



class TestUnconfigureRadiusAttributePolicyNameUnderServer(TestCase):

    def test_unconfigure_radius_attribute_policy_name_under_server(self):
        device = Mock()
        device.configure.return_value = ""

        result = unconfigure_radius_attribute_policy_name_under_server(
            device,
            "ISE",
            "e8eb.340a.c100:ABCD",
            "access",
        )
        self.assertIsNone(result)

        
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "radius server ISE",
                "no attribute policy-name e8eb.340a.c100:ABCD include-in-access-req",
            ],)
        )