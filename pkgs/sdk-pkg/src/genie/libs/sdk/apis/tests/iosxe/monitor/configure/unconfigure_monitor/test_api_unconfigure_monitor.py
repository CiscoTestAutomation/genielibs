from unittest import TestCase
from genie.libs.sdk.apis.iosxe.monitor.configure import unconfigure_monitor
from unittest.mock import Mock


class TestUnconfigureMonitor(TestCase):

    def test_unconfigure_monitor(self):
        self.device = Mock()
        result = unconfigure_monitor(self.device, 'event-trace')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no monitor event-trace',)
        )
