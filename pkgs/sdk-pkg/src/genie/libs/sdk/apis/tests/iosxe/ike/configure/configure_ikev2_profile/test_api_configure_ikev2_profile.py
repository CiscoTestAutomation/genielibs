from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_profile
from unittest.mock import Mock


class TestConfigureIkev2Profile(TestCase):

    def test_configure_ikev2_profile(self):
        self.device = Mock()
        result = configure_ikev2_profile(self.device, 'test', '255.255.255.0', 'pre-share', 'pre-share', 'ike', '10', '2', 'on-demand', None, None, '1.1.1.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 profile test', 'match identity remote address 1.1.1.1 255.255.255.0', 'authentication remote pre-share', 'authentication local pre-share', 'keyring local ike', 'dpd 10 2 on-demand'],)
        )
