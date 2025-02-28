from unittest import TestCase
from genie.libs.sdk.apis.iosxe.logging.configure import unconfigure_logging_source_interface
from unittest.mock import Mock


class TestUnconfigureLoggingSourceInterface(TestCase):

    def test_unconfigure_logging_source_interface(self):
        self.device = Mock()
        result = unconfigure_logging_source_interface(self.device, 'GigabitEthernet1/6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no logging source-interface GigabitEthernet1/6',)
        )
