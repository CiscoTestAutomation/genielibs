from  unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_attribute_policy_name_globally

class TestUnconfigureRadiusAttributePolicyNameGlobally(TestCase):

    def test_unconfigure_radius_attribute_policy_name_globally(self):
        device = Mock()
        device.configure.return_value = ""

        result = unconfigure_radius_attribute_policy_name_globally(
            device,
            "e8eb.340a.c100:ABCD",
            "accounting",
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ("no radius-server attribute policy-name e8eb.340a.c100:ABCD include-in-accounting-req",)
        )