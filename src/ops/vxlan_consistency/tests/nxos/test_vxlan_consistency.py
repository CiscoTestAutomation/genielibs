# Python
import unittest

# Ats
from ats.topology import Device

# Mock
from unittest.mock import Mock

# genie.libs
from genie.libs.ops.vxlan_consistency.nxos.vxlan_consistency import VxlanConsistency
from genie.libs.ops.vxlan_consistency.nxos.tests.vxlan_consistency_output import VxlanConsistencyOutput

from genie.libs.parser.nxos.show_interface import ShowRunningConfigInterface
from genie.libs.parser.nxos.show_fdb import ShowMacAddressTableVni
from genie.libs.parser.nxos.show_l2route import ShowL2routeEvpnMacEvi
from genie.libs.parser.nxos.show_bgp import ShowBgpL2vpnEvpnWord

outputs = {}
outputs['sh nve interface nve1 detail'] = VxlanConsistencyOutput.interface_detail_output
outputs['show running-config interface nve1'] = VxlanConsistencyOutput.run_config_interface_output
outputs['show running-config interface nve2'] = VxlanConsistencyOutput.run_config_interface_output_empty
outputs['show mac address-table vni 2001001 | grep nve1'] = VxlanConsistencyOutput.mac_address_table_output
outputs['show l2route evpn mac evi 1001 mac 0000.0191.0000'] = VxlanConsistencyOutput.l2_route_output
outputs['show bgp l2vpn evpn 0000.0191.0000 | be "best path, in rib" n 10'] = VxlanConsistencyOutput.bgp_l2vpn_output
outputs['show mac address-table local vni 2001001'] = VxlanConsistencyOutput.local_mac_address_table_output
outputs['show l2route evpn mac evi 1001 mac 0000.0191.0001'] = VxlanConsistencyOutput.local_l2_route_output
outputs['show nve interface nve1 detail | grep Source-Interface'] = VxlanConsistencyOutput.local_nve_interface_output
outputs['show bgp l2vpn evpn 0000.0191.0001 | grep -b 8 -a 10 "best path"'] = VxlanConsistencyOutput.local_bgp_l2vpn_output


def mapper(key):
    return outputs[key]


class test_vxlan_consistency(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_vxlan_consistency(self):
        f = VxlanConsistency(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn(intf='nve1')

        self.maxDiff = None

        self.assertEqual(f.info, VxlanConsistencyOutput.vxlanConsistencyOutput)


    def test_selective_attribute_vxlan_consistency(self):
        f = VxlanConsistency(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn(intf='nve1')

        # Check match
        self.assertEqual('2.0.0.1', f.info['interface']['nve1']['member_vni']\
            ['2001001']['local']['verified_structure']\
            ['mac_address']['0000.0191.0001']['next_hop'])

        # Check does not match
        self.assertNotEqual('4.0.0.3', f.info['interface']['nve1']['member_vni']\
            ['2001001']['local']['verified_structure']\
            ['mac_address']['0000.0191.0001']['next_hop'])

        # Check match
        self.assertEqual('4.0.0.3', f.info['interface']['nve1']['member_vni']\
            ['2001001']['remote']['verified_structure']['mac_address']\
            ['0000.0191.0000']['next_hop'])

        # Check does not match
        self.assertNotEqual('2.0.0.1', f.info['interface']['nve1']['member_vni']\
            ['2001001']['remote']['verified_structure']['mac_address']\
            ['0000.0191.0000']['next_hop'])

    def test_empty(self):
        f = VxlanConsistency(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn(intf='nve2')

        self.maxDiff = None

        with self.assertRaises(AttributeError):
            f.info

if __name__ == '__main__':
    unittest.main()
