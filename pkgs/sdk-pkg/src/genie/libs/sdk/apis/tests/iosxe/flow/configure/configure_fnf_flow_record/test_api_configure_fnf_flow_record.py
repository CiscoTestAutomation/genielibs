from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_fnf_flow_record
from unittest.mock import Mock


class TestConfigureFnfFlowRecord(TestCase):

    def test_configure_fnf_flow_record(self):
        self.device = Mock()
        result = configure_fnf_flow_record(self.device, 'test_record', False, None, None, None, None, None, False, False, None, None, False, False, False, None, None, False, None, False, False, False, None, None, None, None, None, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow record test_record', 'match routing vrf input'],)
        )
