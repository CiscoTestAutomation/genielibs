# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.interface.nxos.interface import Interface
from genie.libs.ops.interface.nxos.tests.interface_output import InterfaceOutput

# nxos show_interface
from genie.libs.parser.nxos.show_interface import ShowInterface, ShowVrfAllInterface,\
                                 ShowIpv6InterfaceVrfAll, ShowIpInterfaceVrfAll,\
                                 ShowInterfaceSwitchport
from genie.libs.parser.nxos.show_routing import ShowRoutingIpv6VrfAll, ShowRoutingVrfAll
outputs = {}
outputs['show interface'] = InterfaceOutput.ShowInterface_all
outputs['show vrf all interface'] = InterfaceOutput.ShowVrfAllInterface_all
outputs['show interface switchport'] = InterfaceOutput.ShowInterfaceSwitchport_all
outputs['show ip interface vrf all'] = InterfaceOutput.ShowIpInterfaceVrfAll_all
outputs['show ipv6 interface vrf all'] = InterfaceOutput.ShowIpv6InterfaceVrfAll_all
outputs['show interface Ethernet2/1'] = InterfaceOutput.ShowInterface_eth2
outputs['show vrf VRF1 interface Ethernet2/1'] = InterfaceOutput.ShowVrfAllInterface_vrf1_eth2
outputs['show interface Ethernet2/1 switchport'] = InterfaceOutput.ShowInterfaceSwitchport_eth2
outputs['show ip interface Ethernet2/1 vrf VRF1'] = InterfaceOutput.ShowIpInterfaceVrfAll_all

def mapper(key):
    return outputs[key]

class test_interface(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs

        intf.maker.outputs[ShowRoutingVrfAll] = \
            {"{'vrf':''}":InterfaceOutput.ShowRoutingVrfAll}

        intf.maker.outputs[ShowRoutingIpv6VrfAll] = \
            {"{'vrf':''}":InterfaceOutput.ShowRoutingIpv6VrfAll}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        intf.learn()

        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, InterfaceOutput.InterfaceOpsOutput_info)
    def test_custom_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs

        intf.maker.outputs[ShowRoutingVrfAll] = \
            {"{'vrf':'VRF1'}":InterfaceOutput.ShowRoutingVrfAll_vrf1}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        intf.learn(interface='Ethernet2/1', vrf='VRF1', address_family='ipv4')

        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, InterfaceOutput.InterfaceOpsOutput_custom_info)
    def test_empty_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        outputs['show interface'] = ''
        outputs['show vrf all interface'] = ''
        outputs['show interface switchport'] = ''
        outputs['show ip interface vrf all'] = ''
        outputs[
            'show ipv6 interface vrf all'] = ''
        intf.maker.outputs[ShowRoutingVrfAll] = {"{'vrf':''}":''}
        intf.maker.outputs[ShowRoutingIpv6VrfAll] = {"{'vrf':''}":''}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn()

        # Check no attribute not found
        # info - vrf
        with self.assertRaises(AttributeError):
            vrf = (intf.info['Mgmt0']['vrf'])

        outputs['show interface'] = InterfaceOutput.ShowInterface_all
        outputs['show vrf all interface'] = InterfaceOutput.ShowVrfAllInterface_all
        outputs['show interface switchport'] = InterfaceOutput.ShowInterfaceSwitchport_all
        outputs['show ip interface vrf all'] = InterfaceOutput.ShowIpInterfaceVrfAll_all
        outputs['show ipv6 interface vrf all'] = InterfaceOutput.ShowIpv6InterfaceVrfAll_all
    def test_selective_attribute(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs

        intf.maker.outputs[ShowRoutingVrfAll] = \
            {"{'vrf':''}":InterfaceOutput.ShowRoutingVrfAll}

        intf.maker.outputs[ShowRoutingIpv6VrfAll] = \
            {"{'vrf':''}":InterfaceOutput.ShowRoutingIpv6VrfAll}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn()        

        # Check specific attribute values
        # info - vrf
        self.assertEqual(intf.info['Mgmt0']['vrf'], 'management')
        # info - link_status
        self.assertEqual(intf.info['Mgmt0']['oper_status'], 'up')

    def test_incomplete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs


        intf.maker.outputs[ShowRoutingVrfAll] = \
            {"{'vrf':''}":''}

        intf.maker.outputs[ShowRoutingIpv6VrfAll] = \
            {"{'vrf':''}":InterfaceOutput.ShowRoutingIpv6VrfAll}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn()        

        # Delete missing specific attribute values
        expect_dict = deepcopy(InterfaceOutput.InterfaceOpsOutput_info)
        del(expect_dict['Ethernet2/1']['ipv4']['10.2.2.2/24']['route_tag'])
        del(expect_dict['Ethernet2/1']['ipv4']['10.2.2.2/24']['origin'])
                
        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
