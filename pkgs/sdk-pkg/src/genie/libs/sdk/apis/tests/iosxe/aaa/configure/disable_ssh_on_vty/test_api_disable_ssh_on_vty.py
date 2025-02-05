from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import disable_ssh_on_vty
from unittest.mock import Mock


class TestDisableSshOnVty(TestCase):

    def test_disable_ssh_on_vty(self):
        self.device = Mock()
        result = disable_ssh_on_vty(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 15', 'no transport input'],)
        )
