# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Genie
from genie.libs.ops.interface.nxos.interface import Interface
from genie.libs.ops.interface.nxos.tests.interface_output import InterfaceOutput

# nxos show_interface
from genie.libs.parser.nxos.show_interface import ShowInterface, ShowVrfAllInterface,\
                                 ShowIpv6InterfaceVrfAll, ShowIpInterfaceVrfAll,\
                                 ShowInterfaceSwitchport
from genie.libs.parser.nxos.show_routing import ShowRoutingIpv6VrfAll, ShowRoutingVrfAll


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
        intf.maker.outputs[ShowInterface] = \
            {'':InterfaceOutput.ShowInterface}

        intf.maker.outputs[ShowVrfAllInterface] = \
            {'':InterfaceOutput.ShowVrfAllInterface}

        intf.maker.outputs[ShowIpInterfaceVrfAll] = \
            {'':InterfaceOutput.ShowIpInterfaceVrfAll}

        intf.maker.outputs[ShowIpv6InterfaceVrfAll] = \
            {'':InterfaceOutput.ShowIpv6InterfaceVrfAll}

        intf.maker.outputs[ShowInterfaceSwitchport] = \
            {'':InterfaceOutput.ShowInterfaceSwitchport}

        intf.maker.outputs[ShowRoutingVrfAll] = \
            {'':InterfaceOutput.ShowRoutingVrfAll}

        intf.maker.outputs[ShowRoutingIpv6VrfAll] = \
            {'':InterfaceOutput.ShowRoutingIpv6VrfAll}

        # Learn the feature
        intf.learn()

        # Verify Ops was created successfully
        self.assertEqual(intf.info, InterfaceOutput.InterfaceOpsOutput_info)

    def test_empty_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterface] = {'':''}
        intf.maker.outputs[ShowVrfAllInterface] = {'':''}
        intf.maker.outputs[ShowIpInterfaceVrfAll] = {'':''}
        intf.maker.outputs[ShowIpv6InterfaceVrfAll] = {'':''}
        intf.maker.outputs[ShowInterfaceSwitchport] = {'':''}
        intf.maker.outputs[ShowRoutingVrfAll] = {'':''}
        intf.maker.outputs[ShowRoutingIpv6VrfAll] = {'':''}
        
        # Learn the feature
        intf.learn()

        # Check no attribute not found
        # info - vrf
        with self.assertRaises(AttributeError):
            vrf = (intf.info['mgmt0']['vrf'])

    def test_selective_attribute(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterface] = \
            {'':InterfaceOutput.ShowInterface}

        intf.maker.outputs[ShowVrfAllInterface] = \
            {'':InterfaceOutput.ShowVrfAllInterface}

        intf.maker.outputs[ShowIpInterfaceVrfAll] = \
            {'':InterfaceOutput.ShowIpInterfaceVrfAll}

        intf.maker.outputs[ShowIpv6InterfaceVrfAll] = \
            {'':InterfaceOutput.ShowIpv6InterfaceVrfAll}

        intf.maker.outputs[ShowInterfaceSwitchport] = \
            {'':InterfaceOutput.ShowInterfaceSwitchport}

        intf.maker.outputs[ShowRoutingVrfAll] = \
            {'':InterfaceOutput.ShowRoutingVrfAll}

        intf.maker.outputs[ShowRoutingIpv6VrfAll] = \
            {'':InterfaceOutput.ShowRoutingIpv6VrfAll}

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
        intf.maker.outputs[ShowInterface] = \
            {'':InterfaceOutput.ShowInterface}

        intf.maker.outputs[ShowVrfAllInterface] = \
            {'':InterfaceOutput.ShowVrfAllInterface}

        intf.maker.outputs[ShowIpInterfaceVrfAll] = \
            {'':InterfaceOutput.ShowIpInterfaceVrfAll}

        intf.maker.outputs[ShowIpv6InterfaceVrfAll] = \
            {'':InterfaceOutput.ShowIpv6InterfaceVrfAll}

        intf.maker.outputs[ShowInterfaceSwitchport] = \
            {'':InterfaceOutput.ShowInterfaceSwitchport}

        intf.maker.outputs[ShowRoutingVrfAll] = {'':''}

        intf.maker.outputs[ShowRoutingIpv6VrfAll] = \
            {'':InterfaceOutput.ShowRoutingIpv6VrfAll}

        # Learn the feature
        intf.learn()        

        # Delete missing specific attribute values
        expect_dict = deepcopy(InterfaceOutput.InterfaceOpsOutput_info)
        del(expect_dict['Ethernet2/1']['ipv4']['10.2.2.2/24']['route_tag'])
        del(expect_dict['Ethernet2/1']['ipv4']['10.2.2.2/24']['origin'])
                
        # Verify Ops was created successfully
        self.assertEqual(intf.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
