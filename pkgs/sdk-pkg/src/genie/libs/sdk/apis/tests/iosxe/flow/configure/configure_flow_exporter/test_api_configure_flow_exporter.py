from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_exporter
from unittest.mock import Mock


class TestConfigureFlowExporter(TestCase):

    def test_configure_flow_exporter(self):
        self.device = Mock()
        result = configure_flow_exporter(self.device, 'FNF-EXP-WITH-IPFIX', '30.30.30.2', None, None, None, None, None, None, None, None, 'vrf1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow exporter FNF-EXP-WITH-IPFIX', 'destination 30.30.30.2 vrf vrf1'],)
        )
