from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import disable_ospf_bfd_all_interfaces
from unittest.mock import Mock


class TestDisableOspfBfdAllInterfaces(TestCase):

    def test_disable_ospf_bfd_all_interfaces(self):
        self.device = Mock()
        result = disable_ospf_bfd_all_interfaces(self.device, '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router ospf 1', 'no bfd all-interfaces'],)
        )
