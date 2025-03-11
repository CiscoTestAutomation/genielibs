from unittest import TestCase
from genie.libs.sdk.apis.iosxe.logging.configure import unconfigure_logging_host
from unittest.mock import Mock


class TestUnconfigureLoggingHost(TestCase):

    def test_unconfigure_logging_host(self):
        self.device = Mock()
        result = unconfigure_logging_host(self.device, '11.1.1.22')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no logging host 11.1.1.22',)
        )
