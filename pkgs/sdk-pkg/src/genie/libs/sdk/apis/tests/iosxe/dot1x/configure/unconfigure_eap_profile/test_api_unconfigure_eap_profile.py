from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import unconfigure_eap_profile
from unittest.mock import Mock


class TestUnconfigureEapProfile(TestCase):

    def test_unconfigure_eap_profile(self):
        self.device = Mock()
        result = unconfigure_eap_profile(self.device, 'DUMMY')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no eap profile DUMMY\n',)
        )
