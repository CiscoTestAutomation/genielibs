from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_enroll


class TestConfigurePkiEnroll(TestCase):

    def test_configure_pki_enroll(self):
        device = Mock()
        result = configure_pki_enroll(
            device,
            'Self',
            'cisco123',
            False
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('crypto pki enroll Self',)
        )