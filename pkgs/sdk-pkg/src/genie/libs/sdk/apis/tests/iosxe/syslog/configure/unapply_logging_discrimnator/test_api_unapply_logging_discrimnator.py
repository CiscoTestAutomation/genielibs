from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import unapply_logging_discrimnator
from unittest.mock import Mock


class TestUnapplyLoggingDiscrimnator(TestCase):

    def test_unapply_logging_discrimnator(self):
        self.device = Mock()
        result = unapply_logging_discrimnator(self.device, '10.64.69.167', 'tls', 'test', 'None')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no logging host 10.64.69.167 vrf None transport tls discriminator test',)
        )
