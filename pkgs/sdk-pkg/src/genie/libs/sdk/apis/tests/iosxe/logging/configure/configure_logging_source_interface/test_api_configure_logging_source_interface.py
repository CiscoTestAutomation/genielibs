from unittest import TestCase
from genie.libs.sdk.apis.iosxe.logging.configure import configure_logging_source_interface
from unittest.mock import Mock


class TestConfigureLoggingSourceInterface(TestCase):

    def test_configure_logging_source_interface(self):
        self.device = Mock()
        result = configure_logging_source_interface(self.device, 'GigabitEthernet1/6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('logging source-interface GigabitEthernet1/6',)
        )
