from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import enable_eigrp_bfd_all_interfaces
from unittest.mock import Mock


class TestEnableEigrpBfdAllInterfaces(TestCase):

    def test_enable_eigrp_bfd_all_interfaces(self):
        self.device = Mock()
        result = enable_eigrp_bfd_all_interfaces(self.device, 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router eigrp 10', 'bfd all-interfaces'],)
        )
