# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.vlan.iosxe.vlan import Vlan
from genie.libs.ops.vlan.iosxe.tests.vlan_output import VlanOutput

from genie.libs.parser.iosxe.show_vlan import ShowVlan, \
                                   ShowVlanMtu, \
                                   ShowVlanRemoteSpan, \
                                   ShowVlanAccessMap, \
                                   ShowVlanFilter


class test_vlan_new_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_vlan_new(self):
        f = Vlan(device=self.device)
        # Get 'show vlan' output
        f.maker.outputs[ShowVlan] = {'': VlanOutput.showVlan}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, VlanOutput.vlanOpsOutput)

    def test_selective_attribute_vlan_new(self):
        f = Vlan(device=self.device)

        # Get 'show vlan' output
        f.maker.outputs[ShowVlan] = {'': VlanOutput.showVlan}

        # Learn the feature
        f.learn()
        # Check match
        self.assertEqual('VLAN0020', f.info['vlans']['20']['name'])
        # Check does not match
        self.assertNotEqual(10, f.info['vlans']['20']['vlan_id'])


    def test_missing_attributes_vlan_new(self):
        f = Vlan(device=self.device)
        # Get 'show vlan' output
        f.maker.outputs[ShowVlan] = {'': VlanOutput.showVlan}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['interfaces']

    def test_empty_output_vlan_new(self):
        self.maxDiff = None
        f = Vlan(device=self.device)

        # Get outputs
        f.maker.outputs[ShowVlan] = {'': {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vlans']


if __name__ == '__main__':
    unittest.main()
