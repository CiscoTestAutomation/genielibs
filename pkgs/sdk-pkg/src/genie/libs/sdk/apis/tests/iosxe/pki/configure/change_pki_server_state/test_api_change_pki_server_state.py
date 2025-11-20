from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import change_pki_server_state
from unittest.mock import Mock


class TestChangePkiServerState(TestCase):

    def test_change_pki_server_state(self):
        self.device = Mock()
        result = change_pki_server_state(self.device, 'rootca', 'shutdown')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki server rootca', 'shutdown'],)
        )
