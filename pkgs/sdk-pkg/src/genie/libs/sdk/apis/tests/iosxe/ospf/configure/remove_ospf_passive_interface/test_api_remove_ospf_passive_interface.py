from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ospf.configure import remove_ospf_passive_interface
from unittest.mock import Mock


class TestRemoveOspfPassiveInterface(TestCase):

    def test_remove_ospf_passive_interface(self):
        self.device = Mock()
        result = remove_ospf_passive_interface(self.device, ['FortyGigabitEthernet1/0/1'], 100, 'NF-COLLECTOR')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router ospf 100 vrf NF-COLLECTOR', 'no passive-interface FortyGigabitEthernet1/0/1'],)
        )
