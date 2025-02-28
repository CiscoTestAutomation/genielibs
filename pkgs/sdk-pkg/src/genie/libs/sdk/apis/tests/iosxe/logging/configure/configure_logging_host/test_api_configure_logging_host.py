from unittest import TestCase
from genie.libs.sdk.apis.iosxe.logging.configure import configure_logging_host
from unittest.mock import Mock


class TestConfigureLoggingHost(TestCase):

    def test_configure_logging_host(self):
        self.device = Mock()
        result = configure_logging_host(self.device, '11.1.1.22')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('logging host 11.1.1.22',)
        )
