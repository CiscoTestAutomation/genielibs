from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_enroll
from unittest.mock import Mock


class TestConfigurePkiEnroll(TestCase):

    def test_configure_pki_enroll(self):
        self.device = Mock()
        result = configure_pki_enroll(self.device, 'Self', 'cisco123', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('crypto pki enroll Self',)
        )
