# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie-libs
from genie.libs.ops.vlan.nxos.vlan import Vlan
from genie.libs.ops.vlan.nxos.tests.vlan_output import VlanOutput

from genie.libs.parser.nxos.show_vlan import ShowVlan, \
                                    ShowVlanIdVnSegment,\
                                    ShowVlanInternalInfo, \
                                    ShowVlanFilter, \
                                    ShowVlanAccessMap
from genie.libs.parser.nxos.show_feature import ShowFeature
from genie.libs.parser.nxos.show_igmp import ShowIpIgmpSnooping


from genie.libs.parser.nxos.show_interface import ShowIpInterfaceBriefPipeVlan



class test_new_vlan_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_new_vlan_full(self):
        f = Vlan(device=self.device)
        # Get 'show vlan' output
        f.maker.outputs[ShowVlan] = {'': VlanOutput.showVlan}
        f.maker.outputs[ShowFeature] = {'': VlanOutput.showFeature}
        f.maker.outputs[ShowIpIgmpSnooping] = {'': VlanOutput.showIgmp}
        f.maker.outputs[ShowVlanIdVnSegment] = {'': VlanOutput.showVlanIdVnSegment}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, VlanOutput.vlanOpsOutput)

    def test_new_vlan_selective_attribute(self):
        f = Vlan(device=self.device)
        # Get 'show vlan' output
        f.maker.outputs[ShowVlan] = {'': VlanOutput.showVlan}
        f.maker.outputs[ShowFeature] = {'': VlanOutput.showFeature}
        f.maker.outputs[ShowIpIgmpSnooping] = {'': VlanOutput.showIgmp}
        f.maker.outputs[ShowVlanIdVnSegment] = {'': VlanOutput.showVlanIdVnSegment}

        # Learn the feature
        f.learn()
        # Check match
        self.assertEqual('VLAN0002', f.info['vlans']['2']['name'])
        # Check does not match
        self.assertNotEqual(1, f.info['vlans']['2']['vlan_id'])


    def test_new_vlan_missing_attributes(self):
        f = Vlan(device=self.device)
        # Get 'show vlan' output
        f.maker.outputs[ShowVlan] = {'': VlanOutput.showVlan}
        f.maker.outputs[ShowFeature] = {'': VlanOutput.showFeature}
        f.maker.outputs[ShowIpIgmpSnooping] = {'': VlanOutput.showIgmp}
        f.maker.outputs[ShowVlanIdVnSegment] = {'': VlanOutput.showVlanIdVnSegment}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['vn_segment_id']

    def test_new_vlan_empty_output(self):
        self.maxDiff = None
        f = Vlan(device=self.device)
        # Get outputs
        f.maker.outputs[ShowVlan] = {'': {}}
        f.maker.outputs[ShowFeature] = {'': {}}
        f.maker.outputs[ShowIpIgmpSnooping] = {'': {}}
        f.maker.outputs[ShowVlanIdVnSegment] = {'': {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vlans']

if __name__ == '__main__':
    unittest.main()

