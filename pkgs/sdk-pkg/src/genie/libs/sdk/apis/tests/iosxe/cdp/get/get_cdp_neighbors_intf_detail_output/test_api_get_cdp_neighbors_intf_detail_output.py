from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.get import get_cdp_neighbors_intf_detail_output
from unittest.mock import Mock


class TestGetCdpNeighborsIntfDetailOutput(TestCase):

    def test_get_cdp_neighbors_intf_detail_output(self):
        self.device = Mock()
        results_map = {
            'show cdp neighbors GigabitEthernet0/1/7 detail': 
            '''-------------------------
            Device ID: DNAC-4
            Entry address(es): 
            IP address: 10.74.9.185
            Platform: cisco C1127-8PMLTEP,  Capabilities: Router Switch IGMP 
            Interface: GigabitEthernet0/1/7,  Port ID (outgoing port): GigabitEthernet0/1/7
            Holdtime : 178 sec

            Version :
            Cisco IOS Software [IOSXE], ISR Software (ARMV8EL_LINUX_IOSD-UNIVERSALK9-M), Experimental Version 17.18.20250519:021129 [BLD_V1718_THROTTLE_LATEST_20250519_010438:/nobackup/mcpre/s2c-build-ws 101]
            Copyright (c) 1986-2025 by Cisco Systems, Inc.
            Compiled Sun 18-May-25 19:11 by mcpre

            advertisement version: 2
            Peer Source MAC: 10e3.767f.fe0f


            Total cdp entries displayed : 1''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = get_cdp_neighbors_intf_detail_output(self.device, 'GigabitEthernet0/1/7')
        self.assertIn(
            'show cdp neighbors GigabitEthernet0/1/7 detail',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show cdp neighbors GigabitEthernet0/1/7 detail']
        self.assertEqual(result, expected_output)
