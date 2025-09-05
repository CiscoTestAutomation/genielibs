from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_fnf_flow_record_match_flow
from unittest.mock import Mock


class TestConfigureFnfFlowRecordMatchFlow(TestCase):

    def test_configure_fnf_flow_record_match_flow(self):
        self.device = Mock()
        result = configure_fnf_flow_record_match_flow(self.device, 'r4in', 'direction', 'None')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow record r4in', 'match flow direction'],)
        )
