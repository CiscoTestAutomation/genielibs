from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ntp.configure import configure_no_ntp
from unittest.mock import Mock


class TestConfigureNoNtp(TestCase):

    def test_configure_no_ntp(self):
        self.device = Mock()
        result = configure_no_ntp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ntp',)
        )
