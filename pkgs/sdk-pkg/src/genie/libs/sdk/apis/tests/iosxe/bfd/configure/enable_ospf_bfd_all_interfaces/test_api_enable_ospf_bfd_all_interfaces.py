from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import enable_ospf_bfd_all_interfaces
from unittest.mock import Mock


class TestEnableOspfBfdAllInterfaces(TestCase):

    def test_enable_ospf_bfd_all_interfaces(self):
        self.device = Mock()
        result = enable_ospf_bfd_all_interfaces(self.device, 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router ospf 10', 'bfd all-interfaces'],)
        )
