from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_authorization_exec_on_vty
from unittest.mock import Mock


class TestConfigureAuthorizationExecOnVty(TestCase):

    def test_configure_authorization_exec_on_vty(self):
        self.device = Mock()
        result = configure_authorization_exec_on_vty(self.device, 'VTY_author')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 15', 'authorization exec VTY_author'],)
        )
