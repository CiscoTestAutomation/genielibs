# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Genie
from genie.libs.ops.interface.ios.interface import Interface
from genie.libs.ops.interface.ios.tests.interface_output import InterfaceOutput

# ios show_interface
from genie.libs.parser.ios.show_interface import ShowInterfaces, \
                                        ShowIpInterface,  \
                                        ShowIpv6Interface, \
                                        ShowInterfacesAccounting
                                        
from genie.libs.parser.ios.show_vrf import ShowVrfDetail

# Set values
outputs = {}
outputs['show interfaces'] = InterfaceOutput.ShowInterfaces
outputs['show ip interface'] = InterfaceOutput.ShowIpInterface
outputs['show ipv6 interface'] = InterfaceOutput.ShowIpv6Interface
outputs['show interfaces accounting'] = InterfaceOutput.ShowInterfacesAccounting
outputs['show vrf detail'] = InterfaceOutput.ShowVrfDetail


def mapper(key):
    return outputs[key]


class test_interface(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        intf.learn()

        # Verify Ops was created successfully
        self.assertEqual(intf.info, InterfaceOutput.InterfaceOpsOutput_info)

        # Check specific attribute values
        self.assertEqual(intf.info['FastEthernet0']['oper_status'], 'up')
        self.assertEqual(intf.info['FastEthernet0']['ipv4']['10.1.8.146/24']['ip'], '10.1.8.146')
        self.assertEqual(intf.info['Vlan1']['accounting']['arp']['chars_in'], 4506480)

    def test_empty_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        outputs['show interfaces'] = ''
        outputs['show ip interface'] = ''
        outputs['show ipv6 interface'] = ''
        outputs['show interfaces accounting'] = ''
        outputs['show vrf detail'] = ''

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        intf.learn()

        # Check no attribute not found
        # info - oper_status
        with self.assertRaises(AttributeError):
            intf.info['FastEthernet0']['oper_status']

        # revert the output
        outputs['show interfaces'] = InterfaceOutput.ShowInterfaces
        outputs['show ip interface'] = InterfaceOutput.ShowIpInterface
        outputs['show ipv6 interface'] = InterfaceOutput.ShowIpv6Interface
        outputs['show interfaces accounting'] = InterfaceOutput.ShowInterfacesAccounting
        outputs['show vrf detail'] = InterfaceOutput.ShowVrfDetail

    def test_incomplete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        outputs['show interfaces'] = InterfaceOutput.ShowInterfaces
        outputs['show ip interface'] = InterfaceOutput.ShowIpInterface
        outputs['show ipv6 interface'] = ''
        outputs['show interfaces accounting'] = InterfaceOutput.ShowInterfacesAccounting
        outputs['show vrf detail'] = InterfaceOutput.ShowVrfDetail

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        intf.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(InterfaceOutput.InterfaceOpsOutput_info)
        del(expect_dict['Vlan99']['ipv6'])

        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, expect_dict)

        # revert the output
        outputs['show ipv6 interface'] = InterfaceOutput.ShowIpv6Interface


if __name__ == '__main__':
    unittest.main()
