import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_logging_buffered_persistent_url


class TestConfigureLoggingBufferedPersistentUrl(unittest.TestCase):

    def test_configure_logging_buffered_persistent_url(self):
        device = Mock()

        result = configure_logging_buffered_persistent_url(device, 'crashinfo:/syslog')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('logging buffered\nlogging persistent url crashinfo:/syslog\n',)
        )