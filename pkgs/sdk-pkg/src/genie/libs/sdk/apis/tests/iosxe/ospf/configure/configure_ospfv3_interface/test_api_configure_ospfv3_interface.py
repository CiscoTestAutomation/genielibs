from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_interface


class TestConfigureOspfv3Interface(TestCase):

    def test_configure_ospfv3_interface(self):
        device = Mock()
        result = configure_ospfv3_interface(
            device,
            'GigabitEthernet1/0/24',
            'mtu-ignore'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/24', 'ospfv3 mtu-ignore'],)
        )