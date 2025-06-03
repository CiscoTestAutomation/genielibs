from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import configure_rep_preempt_and_block
from unittest.mock import Mock


class TestConfigureRepPreemptAndBlock(TestCase):

    def test_configure_rep_preempt_and_block(self):
        self.device = Mock()
        result = configure_rep_preempt_and_block(self.device, 'FortyGigabitEthernet1/0/15', '15', '-1', '1-4094')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface FortyGigabitEthernet1/0/15', 'rep preempt delay 15', 'rep block port -1 vlan 1-4094'],)
        )
