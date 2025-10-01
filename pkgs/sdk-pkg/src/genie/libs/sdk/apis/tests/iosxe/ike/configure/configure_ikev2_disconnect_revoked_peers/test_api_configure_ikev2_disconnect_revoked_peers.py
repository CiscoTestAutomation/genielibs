from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_disconnect_revoked_peers
from unittest.mock import Mock


class TestConfigureIkev2DisconnectRevokedPeers(TestCase):

    def test_configure_ikev2_disconnect_revoked_peers(self):
        self.device = Mock()
        result = configure_ikev2_disconnect_revoked_peers(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 disconnect-revoked-peers'],)
        )
