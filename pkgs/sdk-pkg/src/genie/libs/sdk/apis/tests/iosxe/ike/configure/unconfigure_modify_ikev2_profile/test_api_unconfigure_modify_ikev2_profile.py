from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_modify_ikev2_profile
from unittest.mock import Mock


class TestUnconfigureModifyIkev2Profile(TestCase):

    def test_unconfigure_modify_ikev2_profile(self):
        self.device = Mock()
        result = unconfigure_modify_ikev2_profile(self.device, 'test_ikev2_profile', None, None, None, None, None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 profile test_ikev2_profile'],)
        )
