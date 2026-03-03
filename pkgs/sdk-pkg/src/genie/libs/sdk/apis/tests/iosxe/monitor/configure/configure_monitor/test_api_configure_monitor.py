from unittest import TestCase
from genie.libs.sdk.apis.iosxe.monitor.configure import configure_monitor
from unittest.mock import Mock


class TestConfigureMonitor(TestCase):

    def test_configure_monitor(self):
        self.device = Mock()
        result = configure_monitor(self.device, 'event-trace')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('monitor event-trace',)
        )
