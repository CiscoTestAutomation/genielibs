from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfig_extended_acl_with_evaluate


class TestUnconfigExtendedAclWithEvaluate(TestCase):

    def test_unconfig_extended_acl_with_evaluate(self):
        self.device = Mock()
        unconfig_extended_acl_with_evaluate(self.device, 'test1', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test1', 'no evaluate None'] ,)
        )
