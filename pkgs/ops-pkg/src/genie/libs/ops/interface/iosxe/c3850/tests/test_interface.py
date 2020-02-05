# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.interface.iosxe.c3850.interface import Interface
from genie.libs.ops.interface.iosxe.c3850.tests.interface_output import InterfaceOutput

# iosxe show_interface
from genie.libs.parser.iosxe.show_interface import ShowInterfaces, \
                                        ShowInterfacesSwitchport, \
                                        ShowIpInterface,  \
                                        ShowIpv6Interface, \
                                        ShowInterfacesAccounting
                                        
from genie.libs.parser.iosxe.show_vrf import ShowVrf


outputs = {}
outputs['show interfaces GigabitEthernet1/0/1'] = InterfaceOutput.ShowInterfaces_gi1
outputs['show interfaces GigabitEthernet1/0/1 accounting'] = InterfaceOutput.ShowInterfacesAccounting_gi1
outputs['show ip interface GigabitEthernet1/0/1'] = InterfaceOutput.ShowIpInterfaces_gi1
outputs['show ipv6 interface GigabitEthernet1/0/1'] = InterfaceOutput.ShowIpv6Interfaces_gi1
outputs['show interfaces GigabitEthernet1/0/1 switchport']=InterfaceOutput.ShowInterfacesSwitchport_gi1
outputs['show vrf']=InterfaceOutput.ShowVrf_all
outputs['show interfaces'] = InterfaceOutput.ShowInterfaces_all
outputs['show ip interface'] = InterfaceOutput.ShowIpInterfaces_all
outputs['show ipv6 interface'] = InterfaceOutput.ShowIpv6Interfaces_all
outputs['show interfaces accounting'] = InterfaceOutput.ShowInterfacesAccounting_all
outputs['show interfaces switchport']=InterfaceOutput.ShowInterfacesSwitchport_all

def mapper(key):
    return outputs[key]

class test_interface(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn()
        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, InterfaceOutput.InterfaceOpsOutput_info)

    def test_empty_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        outputs['show interfaces GigabitEthernet1/0/1'] = ''
        outputs['show interfaces GigabitEthernet1/0/1 accounting'] = ''
        outputs['show ip interface GigabitEthernet1/0/1'] = ''
        outputs['show ipv6 interface GigabitEthernet1/0/1'] = ''
        outputs['show interfaces GigabitEthernet1/0/1 switchport'] =''
        outputs['show vrf'] =''
        outputs['show interfaces'] = ''
        outputs['show ip interface'] = ''
        outputs['show ipv6 interface'] = ''
        outputs['show interfaces accounting'] = ''
        outputs['show interfaces switchport'] = ''
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        intf.learn()
        outputs[
            'show interfaces GigabitEthernet1/0/1'] = InterfaceOutput.ShowInterfaces_gi1
        outputs[
            'show interfaces GigabitEthernet1/0/1 accounting'] = \
            InterfaceOutput.ShowInterfacesAccounting_gi1
        outputs[
            'show ip interface GigabitEthernet1/0/1'] = \
            InterfaceOutput.ShowIpInterfaces_gi1
        outputs[
            'show ipv6 interface GigabitEthernet1/0/1'] = \
            InterfaceOutput.ShowIpv6Interfaces_gi1
        outputs[
            'show interfaces GigabitEthernet1/0/1 switchport'] = \
            InterfaceOutput.ShowInterfacesSwitchport_gi1

        outputs['show vrf'] = InterfaceOutput.ShowVrf_all
        outputs['show interfaces'] = InterfaceOutput.ShowInterfaces_all
        outputs['show ip interface'] = InterfaceOutput.ShowIpInterfaces_all
        outputs['show ipv6 interface'] = InterfaceOutput.ShowIpv6Interfaces_all
        outputs[
            'show interfaces accounting'] = InterfaceOutput.ShowInterfacesAccounting_all
        outputs[
            'show interfaces switchport'] = InterfaceOutput.ShowInterfacesSwitchport_all

        # Check no attribute not found
        # info - oper_status
        with self.assertRaises(AttributeError):
            vrf = (intf.info['GigabitEthernet1/0/2']['oper_status'])

    def test_custom_output(self):

        intf = Interface(device=self.device)
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn(interface='GigabitEthernet1/0/1', address_family='ipv4')

        self.maxDiff = None
        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, InterfaceOutput.interfaceOpsOutput_custom_info)

    def test_selective_attribute(self):
        self.maxDiff = None
        intf = Interface(device=self.device)

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn()

        # Check specific attribute values
        # info - vrf
        self.assertEqual(intf.info['GigabitEthernet1/0/1']['vrf'], 'VRF1')
        # info - link_status
        self.assertEqual(intf.info['GigabitEthernet1/0/2']['oper_status'], 'up')

    def test_incomplete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        custom = {
            'ShowInterfacesAccounting': {
                '': 'GigabitEthernet1/0/1',
            }
        }
        outputs['show interfaces accounting'] = ''
        outputs['show ip interface'] = ''
        intf.maker.outputs[ShowInterfacesAccounting] = \
            {'':InterfaceOutput.ShowInterfacesAccountingCustom}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn(custom=custom)

        # Delete missing specific attribute values
        outputs[
            'show interfaces accounting'] = InterfaceOutput.ShowInterfacesAccounting_all
        outputs['show ip interface'] = InterfaceOutput.ShowIpInterfaces_all
        expect_dict = deepcopy(InterfaceOutput.InterfaceOpsOutput_info)
        del(expect_dict['GigabitEthernet1/0/1']['ipv4'])
        del(expect_dict['GigabitEthernet1/0/2']['accounting'])
        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, expect_dict)



if __name__ == '__main__':
    unittest.main()
