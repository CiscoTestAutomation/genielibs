from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import configure_logging_discrimnator
from unittest.mock import Mock


class TestConfigureLoggingDiscrimnator(TestCase):

    def test_configure_logging_discrimnator(self):
        self.device = Mock()
        result = configure_logging_discrimnator(self.device, 'test', 'mnemonics', 'CONFIG_I', 'drops')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['logging discriminator test mnemonics drops CONFIG_I'],)
        )
