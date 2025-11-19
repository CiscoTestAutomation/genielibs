from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_modify_ikev2_profile
from unittest.mock import Mock


class TestUnconfigureModifyIkev2Profile(TestCase):

    def test_unconfigure_modify_ikev2_profile(self):
        self.device = Mock()
        result = unconfigure_modify_ikev2_profile(self.device, 'IKEV2_PROFILE', None, None, None, None, None, None, None, True, 'Mgmt-intf', 1, 'group cert list local-group flex', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 profile IKEV2_PROFILE', 'no match fvrf Mgmt-intf', 'no virtual-template 1', 'no aaa authorization group cert list local-group flex'],)
        )