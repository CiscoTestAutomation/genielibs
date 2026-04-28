from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pki.configure import configure_no_pki_enroll


class TestConfigureNoPkiEnroll(TestCase):

    def test_configure_no_pki_enroll(self):
        device = Mock()
        result = configure_no_pki_enroll(
            device,
            'tp_wo_pass_enc'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no crypto pki enroll tp_wo_pass_enc',)
        )