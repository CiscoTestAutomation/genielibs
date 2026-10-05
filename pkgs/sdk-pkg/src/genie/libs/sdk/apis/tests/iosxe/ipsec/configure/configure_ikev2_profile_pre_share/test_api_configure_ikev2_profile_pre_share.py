from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ikev2_profile_pre_share
from unittest.mock import Mock


class TestConfigureIkev2ProfilePreShare(TestCase):

    def test_configure_ikev2_profile_pre_share(self):
        self.device = Mock()
        result = configure_ikev2_profile_pre_share(
                self.device,
                'scale_ikev2_profile_v4_phy',
                'pre-share',
                'pre-share',
                'ikev2_key_v4_phy',
                None,
                '',
                'ipv4',
                None,
                '2',
                'periodic',
                None,
                None,
                'GigabitEthernet0/0/1',
                True,
            )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (
                [
                    'crypto ikev2 profile scale_ikev2_profile_v4_phy',
                    'match identity remote any',
                    'authentication local pre-share',
                    'authentication remote pre-share',
                    'keyring local ikev2_key_v4_phy',
                    'match address local interface GigabitEthernet0/0/1',
                ],
            )
        )
