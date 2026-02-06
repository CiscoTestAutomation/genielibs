from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_access_session_pqc_type
from unittest.mock import Mock


class TestConfigureAccessSessionPqcType(TestCase):

    def test_configure_access_session_pqc_type(self):
        self.device = Mock()
        result = configure_access_session_pqc_type(self.device, 'non-pqc')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('access-session pqc-type non-pqc',)
        )
