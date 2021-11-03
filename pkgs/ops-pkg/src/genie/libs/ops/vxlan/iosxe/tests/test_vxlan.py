# Python
import unittest
# Ats
from pyats.topology import Device
from unittest.mock import Mock

from genie.libs.ops.vxlan.iosxe.vxlan import Vxlan
from genie.libs.ops.vxlan.iosxe.tests.vxlan_output import VxlanOutput

from genie.libs.parser.iosxe.show_nve import ShowNveInterfaceDetail,\
                                             ShowNveVni
from genie.libs.parser.iosxe.show_run import ShowRunInterface


class test_vxlan_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full_vni_vxlan(self):
        f = Vxlan(device=self.device)

        f.maker.outputs[ShowNveVni] = {'': VxlanOutput.ShowNveVni}
        f.maker.outputs[ShowRunInterface] = {"{'interface':'nve1'}": VxlanOutput.ShowRunInterface}
        f.maker.outputs[ShowNveInterfaceDetail] = {"{'nve_num':'1'}": VxlanOutput.ShowNveInterfaceDetail}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        # Check match
        self.maxDiff = None
        self.assertEqual(f.nve, VxlanOutput.VxlanNveOpsOutput)

    def test_selective_attribute_vxlan(self):
        f = Vxlan(device=self.device)

        f.maker.outputs[ShowNveVni] = {'': VxlanOutput.ShowNveVni}
        f.maker.outputs[ShowRunInterface] = {"{'interface':'nve1'}": VxlanOutput.ShowRunInterface}
        f.maker.outputs[ShowNveInterfaceDetail] = {"{'nve_num':'1'}": VxlanOutput.ShowNveInterfaceDetail}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        # Check match
        self.maxDiff = None
        self.assertEqual('11', f.nve['nve1']['vni']['20011']['vlan'])
        self.assertEqual('229.1.1.3', f.nve['nve1']['vni']['20013']['mcast'])
        self.assertEqual('Enabled', f.nve['nve1']['bgp_host_reachability'])

        # Check does not match
        self.assertNotEqual(10, f.nve['nve1']['num_l3vni_cp'])
        self.assertNotEqual('Up', f.nve['nve1']['oper_state'])
        self.assertNotEqual('Loopback0', f.nve['nve1']['src_intf'])

    def test_empty_output_vxlan(self):
        self.maxDiff = None
        f = Vxlan(device=self.device)

        # Get outputs
        f.maker.outputs[ShowNveInterfaceDetail] = {"{'interface':'nve1'}": {}}
        f.maker.outputs[ShowRunInterface] = {"{'nve_num':'1'}": {}}
        f.maker.outputs[ShowNveVni] = {'': {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.nve['instance']


if __name__ == '__main__':
    unittest.main()
