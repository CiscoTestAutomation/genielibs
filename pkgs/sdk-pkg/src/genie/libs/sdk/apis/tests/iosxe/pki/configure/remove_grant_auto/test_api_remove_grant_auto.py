from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pki.configure import remove_grant_auto

class TestRemoveGrantAuto(TestCase):

    def test_remove_grant_auto(self):
        self.device = Mock()
        self.device.parse.return_value = {
            'server': {
                'myCA': {'status': 'enabled'}
            }
        }
        self.device.api.change_pki_server_state = Mock()
        self.device.configure = Mock(return_value=True)

        result = remove_grant_auto(self.device, wait_time=0)

        called_args = self.device.configure.call_args[0][0]
        self.assertIn("no grant auto", called_args)

        calls = [call[0][1] for call in self.device.api.change_pki_server_state.call_args_list]
        self.assertIn("shutdown", calls)
        self.assertIn("no shutdown", calls)

        self.assertTrue(result)