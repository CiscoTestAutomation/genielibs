from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hardware.configure import unconfigure_400g_mode_port_group_range
from unittest.mock import Mock


class TestUnconfigure400gModePortGroupRange(TestCase):

    def test_unconfigure_400g_mode_port_group_range(self):
        self.device = Mock()
        result = unconfigure_400g_mode_port_group_range(self.device, 1, 200)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no hw-module slot 1 port-group range 1-2 mode 400G',)
        )
