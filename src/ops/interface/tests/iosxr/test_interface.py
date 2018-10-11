# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Genie
from genie.libs.ops.interface.iosxr.interface import Interface
from genie.libs.ops.interface.iosxr.tests.interface_output import InterfaceOutput

# nxos show_interface
from genie.libs.parser.iosxr.show_interface import ShowInterfacesDetail, \
                                    ShowEthernetTags, \
                                    ShowIpv4VrfAllInterface, \
                                    ShowIpv6VrfAllInterface, \
                                    ShowInterfacesAccounting

from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail


class test_interface(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfacesDetail] = \
            {'':InterfaceOutput.ShowInterfacesDetail}

        intf.maker.outputs[ShowEthernetTags] = \
            {'':InterfaceOutput.ShowEthernetTags}

        intf.maker.outputs[ShowIpv4VrfAllInterface] = \
            {'':InterfaceOutput.ShowIpv4VrfAllInterface}

        intf.maker.outputs[ShowIpv6VrfAllInterface] = \
            {'':InterfaceOutput.ShowIpv6VrfAllInterface}

        intf.maker.outputs[ShowVrfAllDetail] = \
            {'':InterfaceOutput.ShowVrfAllDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {'':InterfaceOutput.ShowInterfacesAccounting}

        # Learn the feature
        intf.learn()

        # Verify Ops was created successfully
        self.assertEqual(intf.info, InterfaceOutput.InterfaceOpsOutput_info)

    def test_empty_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfacesDetail] = {'':''}
        intf.maker.outputs[ShowIpv4VrfAllInterface] = {'':''}
        intf.maker.outputs[ShowIpv6VrfAllInterface] = {'':''}
        intf.maker.outputs[ShowVrfAllDetail] = {'':''}            
        intf.maker.outputs[ShowEthernetTags] = {'':''}
        intf.maker.outputs[ShowInterfacesAccounting] = {'':''}

        # Learn the feature
        intf.learn()

        # Check no attribute not found
        # info - vrf
        with self.assertRaises(AttributeError):
            vrf = (intf.info['MgmtEth0/0/CPU0/0']['type'])

    def test_selective_attribute(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfacesDetail] = \
            {'':InterfaceOutput.ShowInterfacesDetail}
            
        intf.maker.outputs[ShowEthernetTags] = \
            {'':InterfaceOutput.ShowEthernetTags}

        intf.maker.outputs[ShowIpv4VrfAllInterface] = \
            {'':InterfaceOutput.ShowIpv4VrfAllInterface}

        intf.maker.outputs[ShowIpv6VrfAllInterface] = \
            {'':InterfaceOutput.ShowIpv6VrfAllInterface}

        intf.maker.outputs[ShowVrfAllDetail] = \
            {'':InterfaceOutput.ShowVrfAllDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {'':InterfaceOutput.ShowInterfacesAccounting}

        # Learn the feature
        intf.learn()        

        # Check specific attribute values
        # info - type
        self.assertEqual(intf.info['MgmtEth0/0/CPU0/0']['type'], 'Management Ethernet')

    def test_incomplete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfacesDetail] = \
            {'':InterfaceOutput.ShowInterfacesDetail}
            
        intf.maker.outputs[ShowEthernetTags] = \
            {'':InterfaceOutput.ShowEthernetTags}

        intf.maker.outputs[ShowIpv4VrfAllInterface] = {'':''}

        intf.maker.outputs[ShowIpv6VrfAllInterface] = \
            {'':InterfaceOutput.ShowIpv6VrfAllInterface}

        intf.maker.outputs[ShowVrfAllDetail] = \
            {'':InterfaceOutput.ShowVrfAllDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {'':InterfaceOutput.ShowInterfacesAccounting}

        # Learn the feature
        intf.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(InterfaceOutput.InterfaceOpsOutput_info)
        del(expect_dict['GigabitEthernet0/0/0/0']['ipv4'])
                
        # Verify Ops was created successfully
        self.assertEqual(intf.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
