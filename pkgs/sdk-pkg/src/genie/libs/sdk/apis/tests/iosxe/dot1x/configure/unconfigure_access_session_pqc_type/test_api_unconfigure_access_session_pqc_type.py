from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import unconfigure_access_session_pqc_type
from unittest.mock import Mock


class TestUnconfigureAccessSessionPqcType(TestCase):

    def test_unconfigure_access_session_pqc_type(self):
        self.device = Mock()
        result = unconfigure_access_session_pqc_type(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no access-session pqc-type',)
        )
