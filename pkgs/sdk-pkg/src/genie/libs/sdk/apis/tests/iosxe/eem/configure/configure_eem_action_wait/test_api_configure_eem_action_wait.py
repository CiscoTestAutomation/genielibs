from unittest import TestCase
from genie.libs.sdk.apis.iosxe.eem.configure import configure_eem_action_wait
from unittest.mock import Mock


class TestConfigureEemActionWait(TestCase):

    def test_configure_eem_action_wait(self):
        self.device = Mock()
        result = configure_eem_action_wait(self.device, 'WRITE_MEM_EEM', 1.3, 5)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['event manager applet WRITE_MEM_EEM', 'action 1.3 wait 5'],)
        )
