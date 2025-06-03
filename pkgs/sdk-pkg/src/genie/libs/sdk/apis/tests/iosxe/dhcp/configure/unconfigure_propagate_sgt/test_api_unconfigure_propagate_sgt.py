from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_propagate_sgt
from unittest.mock import Mock


class TestUnconfigurePropagateSgt(TestCase):

    def test_unconfigure_propagate_sgt(self):
        self.device = Mock()
        unconfigure_propagate_sgt(self.device, 'GigabitEthernet1/0/1', 'manual', 'propagate')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'cts manual', 'no propagate sgt'],))
        

        
