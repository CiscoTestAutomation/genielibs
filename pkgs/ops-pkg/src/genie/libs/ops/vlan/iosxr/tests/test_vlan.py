# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

# genie.libs
from genie.libs.ops.vlan.iosxr.vlan import Vlan
from genie.libs.ops.vlan.iosxr.tests.vlan_output import VlanOutput
from genie.libs.parser.iosxr.show_ethernet import ShowEthernetTags, \
                                       ShowEthernetTrunkDetail


class test_vlan_all(unittest.TestCase):

    def setUp(self):

        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_sample(self):

        f = Vlan(device=self.device)

        f.maker.outputs[ShowEthernetTags] = \
            {'':VlanOutput.showEthernetTags}

        f.learn()

        self.assertEqual(f.name, VlanOutput.vlan_all)

    def test_missing_attributes(self):
        f = Vlan(device=self.device)

        f.maker.outputs[ShowEthernetTags] = \
            {'':VlanOutput.showEthernetTags}

        f.learn()

        with self.assertRaises(KeyError):
            interface_mtu =(f.name['6']['sub_interfaces'])

    def test_ignored(self):

        f = Vlan(device=self.device)
        g = Vlan(device=self.device)

        f.maker.outputs[ShowEthernetTags] = \
            {'':VlanOutput.showEthernetTags}

        g.maker.outputs[ShowEthernetTags] = \
            {'':VlanOutput.showEthernetTags}

        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f,g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('+s: 2')
        self.assertEqual(sorted_diff,sorted_result)

    def test_selective_attribute(self):

        f = Vlan(device=self.device, attributes = ['name[(.*)][sub_interface]'])

        f.maker.outputs[ShowEthernetTags] = \
            {'':VlanOutput.showEthernetTags}

        f.learn()

        self.assertIn('Gi0/0/0/0.501', f.name['4']['sub_interface'])
        self.assertNotIn('Gi0/0/0/0.502', f.name['4']['sub_interface'])

    def test_empty_parser_output(self):

        f = Vlan(device=self.device)

        f.maker.outputs[ShowEthernetTags] = \
            {'':VlanOutput.showEthernetTagsempty}

        f.learn()

        # f is empty since show ethernet tags is the primary 
        # parser for the maker.
        print ('f did not get learned as expected in test_empty_parser_output')

if __name__ == '__main__':
    unittest.main()
