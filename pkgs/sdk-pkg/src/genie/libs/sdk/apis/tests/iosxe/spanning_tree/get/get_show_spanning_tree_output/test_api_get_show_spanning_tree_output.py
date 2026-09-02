from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.get import get_show_spanning_tree_output
from unittest.mock import Mock


class TestGetShowSpanningTreeOutput(TestCase):

    def test_get_show_spanning_tree_output(self):
        self.device = Mock()
        results_map = {
            'show spanning-tree': '''
G0:VLAN0100
  Spanning tree enabled protocol ieee
  Root ID    Priority    32868
             Address     10e3.7677.3171
             Cost        20000
             Port        7 (GigabitEthernet0/1/0)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32868  (priority 32768 sys-id-ext 100)
             Address     10e3.767f.fe71
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  30  sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/1/0             Root FWD 20000     128.7    P2p 



G0:VLAN0200
  Spanning tree enabled protocol ieee
  Root ID    Priority    32968
             Address     10e3.7677.3171
             Cost        20000
             Port        14 (GigabitEthernet0/1/7)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32968  (priority 32768 sys-id-ext 200)
             Address     10e3.767f.fe71
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  30  sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- -------------------------------
Gi0/1/7             Root FWD 20000      64.14   P2p'''
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = get_show_spanning_tree_output(self.device)
        self.assertIn(
            'show spanning-tree',
            self.device.execute.call_args_list[0][0]
        )
        self.assertIsNotNone(result)
