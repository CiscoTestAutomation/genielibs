from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import enable_ssh_on_vty
from unittest.mock import Mock


class TestEnableSshOnVty(TestCase):

    def test_enable_ssh_on_vty(self):
        self.device = Mock()
        result = enable_ssh_on_vty(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 15', 'transport input ssh'],)
        )
