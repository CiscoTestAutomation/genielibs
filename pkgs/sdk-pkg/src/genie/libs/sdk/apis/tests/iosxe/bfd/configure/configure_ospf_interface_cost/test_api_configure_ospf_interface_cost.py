from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import configure_ospf_interface_cost
from unittest.mock import Mock


class TestConfigureOspfInterfaceCost(TestCase):

    def test_configure_ospf_interface_cost(self):
        self.device = Mock()
        result = configure_ospf_interface_cost(self.device, 'Te1/0/1', 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Te1/0/1', 'ip ospf cost 10'],)
        )
