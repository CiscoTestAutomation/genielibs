from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import apply_logging_discrimnator
from unittest.mock import Mock


class TestApplyLoggingDiscrimnator(TestCase):

    def test_apply_logging_discrimnator(self):
        self.device = Mock()
        result = apply_logging_discrimnator(self.device, 'test', '10.64.69.167', 'tls', 'syslog_2', 'None')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('logging host 10.64.69.167 vrf None transport tls profile syslog_2 '
 'discriminator test'),)
        )
