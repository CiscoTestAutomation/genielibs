from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import unconfigure_dot1x_cred_profile
from unittest.mock import Mock


class TestUnconfigureDot1xCredProfile(TestCase):

    def test_unconfigure_dot1x_cred_profile(self):
        self.device = Mock()
        result = unconfigure_dot1x_cred_profile(self.device, 'dot1x_prof')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no dot1x credentials dot1x_prof\n',)
        )
