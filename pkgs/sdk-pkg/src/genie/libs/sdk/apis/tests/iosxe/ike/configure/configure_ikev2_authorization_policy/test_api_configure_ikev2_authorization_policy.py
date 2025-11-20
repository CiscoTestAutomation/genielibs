from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_authorization_policy
from unittest.mock import Mock


class TestConfigureIkev2AuthorizationPolicy(TestCase):

    def test_configure_ikev2_authorization_policy(self):
        self.device = Mock()
        result = configure_ikev2_authorization_policy(self.device, 'flex', False, None, None, None, None, None, None, None, None, None, '197:16:1::', 64, None, None, None, None, None, None, None, None, None, False, None, None, None, None, None, None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 authorization policy flex', 'route set remote ipv6 197:16:1::/64'],)
        )
