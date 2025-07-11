from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import unconfigure_logging_discrimnator
from unittest.mock import Mock


class TestUnconfigureLoggingDiscrimnator(TestCase):

    def test_unconfigure_logging_discrimnator(self):
        self.device = Mock()
        result = unconfigure_logging_discrimnator(self.device, 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no logging discriminator test'],)
        )
