from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_snmp_if_index_on_ospfv3_process_id


class TestConfigureSnmpIfIndexOnOspfv3ProcessId(TestCase):

    def test_configure_snmp_if_index_on_ospfv3_process_id(self):
        device = Mock()
        result = configure_snmp_if_index_on_ospfv3_process_id(
            device,
            '10535'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ipv6 router ospf 10535', 'interface-id snmp-if-index'],)
        )