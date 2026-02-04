from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.get import get_cdp_neighbors_output
from unittest.mock import Mock


class TestGetCdpNeighborsOutput(TestCase):

    def test_get_cdp_neighbors_output(self):
        self.device = Mock()
        results_map = {
            'show cdp neighbors': 
            '''Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone, 
                D - Remote, C - CVTA, M - Two-port Mac Relay 

            Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
            DNAC-4           Gig 0/1/7         175             R S I  C1127-8PM Gig 0/1/7
            DNAC-4           Gig 0/1/0         176             R S I  C1127-8PM Gig 0/1/0
            SW-177.177.lab   Gig 0/0/0         142             R S I  C1100TG-1 Gig 0/2/17

            Total cdp entries displayed : 3'''
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect
        
        result = get_cdp_neighbors_output(self.device)
        self.assertIn(
            'show cdp neighbors',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show cdp neighbors']
        self.assertEqual(result, expected_output)
