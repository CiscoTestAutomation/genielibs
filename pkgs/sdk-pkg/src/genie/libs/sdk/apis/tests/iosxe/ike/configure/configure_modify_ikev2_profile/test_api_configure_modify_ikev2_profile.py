from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import configure_modify_ikev2_profile
from unittest.mock import Mock


class TestConfigureModifyIkev2Profile(TestCase):

    def test_configure_modify_ikev2_profile(self):
        self.device = Mock()
        result = configure_modify_ikev2_profile(self.device, 'IKEV2_PROFILE', None, None, None, None, None, None, None, True, 'Mgmt-intf', 1, 'group cert list local-group flex')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 profile IKEV2_PROFILE', 'crypto ikev2 profile IKEV2_PROFILE', 'nat force-encap', 'match fvrf Mgmt-intf', 'virtual-template 1', 'aaa authorization group cert list local-group flex'],)
        )
