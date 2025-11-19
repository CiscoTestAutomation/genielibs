from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_proposal
from unittest.mock import Mock


class TestConfigureIkev2Proposal(TestCase):

    def test_configure_ikev2_proposal(self):
        self.device = Mock()
        result = configure_ikev2_proposal(self.device, 'ikev2proposal', 'aes-cbc-256', 21, 'sha512', None, 'mlkem1024', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 proposal ikev2proposal', 'encryption aes-cbc-256', 'integrity sha512', 'group 21', 'ake mlkem1024 required'],)
        )
