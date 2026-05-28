from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rip.configure import unconfigure_rip_version
from unittest.mock import Mock


class TestUnconfigureRipVersion(TestCase):

    def test_unconfigure_rip_version(self):
        self.device = Mock()
        result = unconfigure_rip_version(self.device, 2)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router rip', 'no version 2'],)
        )
