from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_record_with_match
from unittest.mock import Mock


class TestConfigureFlowRecordWithMatch(TestCase):

    def test_configure_flow_record_with_match(self):
        self.device = Mock()
        result = configure_flow_record_with_match(self.device, 'A', 'record A', ['connection', 'client', 'ipv4', 'address'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow record A', 'description record A', 'match connection client ipv4 address'],)
        )
