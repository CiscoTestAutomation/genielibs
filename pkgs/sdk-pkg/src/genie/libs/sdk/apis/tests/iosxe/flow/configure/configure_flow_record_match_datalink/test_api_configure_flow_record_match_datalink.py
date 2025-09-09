from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_record_match_datalink
from unittest.mock import Mock


class TestConfigureFlowRecordMatchDatalink(TestCase):

    def test_configure_flow_record_match_datalink(self):
        self.device = Mock()
        result = configure_flow_record_match_datalink(self.device, 'r2out', 'dot1q', None, 'output', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow record r2out', 'match datalink dot1q vlan output'],)
        )
