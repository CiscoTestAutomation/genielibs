from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_flow_record_from_monitor
from unittest.mock import Mock


class TestUnconfigureFlowRecordFromMonitor(TestCase):

    def test_unconfigure_flow_record_from_monitor(self):
        self.device = Mock()
        result = unconfigure_flow_record_from_monitor(self.device, 'ipv4_monitor_in', 'ipv4_record_in')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow monitor ipv4_monitor_in', 'no record ipv4_record_in'],)
        )
