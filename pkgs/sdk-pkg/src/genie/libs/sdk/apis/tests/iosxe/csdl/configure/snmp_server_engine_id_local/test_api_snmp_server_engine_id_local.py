from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.configure import snmp_server_engine_id_local


class TestSnmpServerEngineIdLocal(TestCase):
    def test_snmp_server_engine_id_local(self):
        device = Mock()
        result = snmp_server_engine_id_local(device, '0101928333')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['snmp-server engineID local 0101928333'],)
        )