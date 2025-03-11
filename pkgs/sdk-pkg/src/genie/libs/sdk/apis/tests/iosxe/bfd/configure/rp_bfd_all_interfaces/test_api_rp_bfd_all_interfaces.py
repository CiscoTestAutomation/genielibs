from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import rp_bfd_all_interfaces
from unittest.mock import Mock


class TestRpBfdAllInterfaces(TestCase):

    def test_rp_bfd_all_interfaces(self):
        self.device = Mock()
        result = rp_bfd_all_interfaces(self.device, 'rip', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router rip', 'bfd all-interfaces'],)
        )
