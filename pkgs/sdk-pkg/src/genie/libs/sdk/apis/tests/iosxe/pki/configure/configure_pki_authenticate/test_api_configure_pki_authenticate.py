from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_authenticate


class TestConfigurePkiAuthenticate(TestCase):

    def test_configure_pki_authenticate(self):
        device = Mock()
        result = configure_pki_authenticate(
            device,
            'client'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('crypto pki authenticate client',)
        )