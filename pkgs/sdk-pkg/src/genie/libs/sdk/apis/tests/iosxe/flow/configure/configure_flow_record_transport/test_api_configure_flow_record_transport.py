from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_record_transport
from unittest.mock import Mock


class TestConfigureFlowRecordTransport(TestCase):

    def test_configure_flow_record_transport(self):
        self.device = Mock()
        result = configure_flow_record_transport(self.device, 'r4out', 'match', 'source-port', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow record r4out', 'match transport source-port'],)
        )
