from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import configure_bfd_ospf_timers
from unittest.mock import Mock


class TestConfigureBfdOspfTimers(TestCase):

    def test_configure_bfd_ospf_timers(self):
        self.device = Mock()
        result = configure_bfd_ospf_timers(self.device, 10, 200, 200, 500, 200, 200, 500)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router ospf 10', 'timers throttle lsa 200 200 500', 'timers throttle spf 200 200 500'],)
        )
