from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_max_path
from unittest.mock import Mock


class TestConfigureOspfv3MaxPath(TestCase):

    def test_configure_ospfv3_max_path(self):
        self.device = Mock()
        result = configure_ospfv3_max_path(self.device, '1', 3)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router ospfv3 1', 'address-family ipv6 unicast', 'maximum-paths 3', 'exit-address-family'],)
        )
