from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_network_type


class TestConfigureOspfv3NetworkType(TestCase):

    def test_configure_ospfv3_network_type(self):
        device = Mock()
        result = configure_ospfv3_network_type(
            device,
            'GigabitEthernet1/0/24',
            'point-to-point'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/24', 'ospfv3 network point-to-point'],)
        )