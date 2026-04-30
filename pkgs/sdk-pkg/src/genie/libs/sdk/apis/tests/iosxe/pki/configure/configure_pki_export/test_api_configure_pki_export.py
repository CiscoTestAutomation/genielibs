from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_export


class TestConfigurePkiExport(TestCase):

    def test_configure_pki_export(self):
        device = Mock()
        result = configure_pki_export(
            device,
            'Self',
            'pem',
            'cisco123',
            None,
            None,
            None,
            'terminal',
            None,
            None,
            None,
            'aes'
        )
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('crypto pki export Self pem terminal aes password cisco123',)
        )