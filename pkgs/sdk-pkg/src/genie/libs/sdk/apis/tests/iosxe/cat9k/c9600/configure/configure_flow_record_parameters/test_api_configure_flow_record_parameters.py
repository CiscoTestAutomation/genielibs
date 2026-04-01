from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat9k.c9600.configure import configure_flow_record_parameters
from unittest.mock import Mock


class TestConfigureFlowRecordParameters(TestCase):

    def test_configure_flow_record_parameters(self):
        self.device = Mock()
        result = configure_flow_record_parameters(self.device, 'test_record', 'direction', 'input', True, True, 'tos', 'vrf input', ['destination-port', 'source-port'], 'output', ['source as peer 4-octet', 'destination as peer 4-octet'], 'tcp flags', True, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow record test_record', 'match flow direction', 'match interface input', 'match ipv4 destination address', 'match ipv4 source address', 'match ipv4 tos', 'match routing vrf input', 'match transport destination-port', 'match transport source-port', 'collect interface output', 'collect routing source as peer 4-octet', 'collect routing destination as peer 4-octet', 'collect transport tcp flags', 'collect counter bytes', 'collect counter packets'],)
        )
