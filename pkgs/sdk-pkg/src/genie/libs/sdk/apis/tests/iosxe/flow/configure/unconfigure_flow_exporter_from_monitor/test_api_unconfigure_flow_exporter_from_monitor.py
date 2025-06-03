from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_flow_exporter_from_monitor
from unittest.mock import Mock


class TestUnconfigureFlowExporterFromMonitor(TestCase):

    def test_unconfigure_flow_exporter_from_monitor(self):
        self.device = Mock()
        result = unconfigure_flow_exporter_from_monitor(self.device, 'datalink_monitor_out', 'FNF-EXP-WITHOUT-IPFIX')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow monitor datalink_monitor_out', 'no exporter FNF-EXP-WITHOUT-IPFIX'],)
        )
