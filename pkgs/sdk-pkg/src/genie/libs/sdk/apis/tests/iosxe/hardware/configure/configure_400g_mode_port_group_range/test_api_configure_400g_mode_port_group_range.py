from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hardware.configure import configure_400g_mode_port_group_range
from unittest.mock import Mock


class TestConfigure400gModePortGroupRange(TestCase):

    def test_configure_400g_mode_port_group_range(self):
        self.device = Mock()
        result = configure_400g_mode_port_group_range(self.device, 1, 100)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hw-module slot 1 port-group range 1-2 mode 400G',)
        )
