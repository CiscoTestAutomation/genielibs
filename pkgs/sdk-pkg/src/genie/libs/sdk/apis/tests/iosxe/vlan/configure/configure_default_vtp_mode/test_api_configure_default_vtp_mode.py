from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vlan.configure import configure_default_vtp_mode
from unittest.mock import Mock


class TestConfigureDefaultVtpMode(TestCase):

    def test_configure_default_vtp_mode(self):
        self.device = Mock()
        result = configure_default_vtp_mode(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('default vtp mode',)
        )
