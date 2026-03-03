import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_attribute_policy_name_under_servergroup


class TestUnconfigureRadiusAttributePolicyNameUnderServergroup(TestCase):

    def test_unconfigure_radius_attribute_policy_name_under_servergroup(self):
        device = Mock()
        result = unconfigure_radius_attribute_policy_name_under_servergroup(
            device,
            "ISEGRP",
            "e8eb.340a.c100:ABCD",
            "accounting",
        )
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify configure was called with the correct commands
        device.configure.assert_called_once_with([
            "aaa group server radius ISEGRP",
            "no attribute policy-name e8eb.340a.c100:ABCD include-in-accounting-req",
        ])


if __name__ == '__main__':
    unittest.main()
