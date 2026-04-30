from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_archive_logging


class TestConfigureArchiveLogging(TestCase):

    def test_configure_archive_logging(self):
        device = Mock()
        result = configure_archive_logging(
            device,
            True,
            True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
           (['archive', 'log config', 'logging enable', 'hidekeys', 'notify syslog'],) 
        )