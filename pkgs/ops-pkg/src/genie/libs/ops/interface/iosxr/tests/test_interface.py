# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

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

outputs = {}
outputs[
    'show interface GigabitEthernet0/0/0/1 detail'] = \
    InterfaceOutput.ShowInterfacesDetail_gi1
outputs[
    'show interfaces GigabitEthernet0/0/0/1 accounting'] = \
    InterfaceOutput.ShowInterfacesAccounting_gi1
outputs['show ethernet tags GigabitEthernet0/0/0/1'] = InterfaceOutput.ShowEthernetTag_gi1
outputs['show ethernet tags'] = InterfaceOutput.ShowEthernetTags_all
outputs['show vrf VRF1 detail'] = InterfaceOutput.ShowVrfAllDetail_vrf1
outputs['show ipv4 vrf VRF1 interface'] = InterfaceOutput.ShowIpv4VrfAllInterface_vrf1
outputs['show ipv6 vrf VRF1 interface'] = InterfaceOutput.ShowIpv6VrfAllInterface_vrf1
outputs['show ipv4 vrf all interface'] = InterfaceOutput.ShowIpv4VrfAllInterface_all
outputs['show ipv6 vrf all interface'] = InterfaceOutput.ShowIpv6VrfAllInterface_all
outputs['show ipv6 vrf VRF1 interface GigabitEthernet0/0/0/1'] = InterfaceOutput.ShowIpv6VrfAllInterface_gi1
outputs['show vrf all detail'] = InterfaceOutput.ShowVrfAllDetail_all
outputs['show interfaces accounting'] = InterfaceOutput.ShowInterfacesAccounting_all

def mapper(key):
    return outputs[key]


class test_interface(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfacesDetail] = \
            {"{'interface':''}": InterfaceOutput.ShowInterfacesDetail}

        intf.maker.outputs[ShowEthernetTags] = \
            {"{'interface':''}": InterfaceOutput.ShowEthernetTags}

        intf.maker.outputs[ShowVrfAllDetail] = \
            {"{'vrf':''}": InterfaceOutput.ShowVrfAllDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {"{'interface':''}": InterfaceOutput.ShowInterfacesAccounting}
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
        intf.maker.outputs[ShowInterfacesDetail] = {"{'interface':''}": ''}
        intf.maker.outputs[ShowIpv4VrfAllInterface] = {"{'vrf':None,'interface':''}": ''}
        intf.maker.outputs[ShowIpv6VrfAllInterface] = {"{'vrf':None,'interface':''}": ''}
        intf.maker.outputs[ShowVrfAllDetail] = {"{'vrf':''}": ''}
        intf.maker.outputs[ShowEthernetTags] = {"{'interface':''}": ''}
        intf.maker.outputs[ShowInterfacesAccounting] = {"{'interface':''}": ''}
        outputs['show ipv4 vrf all interface'] = ''
        outputs['show ipv6 vrf all interface'] = ''
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn()

        # Check no attribute not found
        # info - vrf
        with self.assertRaises(AttributeError):
            vrf = (intf.info['MgmtEth0/0/CPU0/0']['type'])

        outputs['show ipv4 vrf all interface'] = InterfaceOutput.ShowIpv4VrfAllInterface_all
        outputs['show ipv6 vrf all interface'] = InterfaceOutput.ShowIpv6VrfAllInterface_all

    def test_custom_output(self):
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowIpv4VrfAllInterface] = \
            {"{'vrf':''}": InterfaceOutput.ShowIpv4VrfAllInterface}

        intf.maker.outputs[ShowIpv6VrfAllInterface] = \
            {"{'vrf':''}": InterfaceOutput.ShowIpv6VrfAllInterface}

        intf.maker.outputs[ShowVrfAllDetail] = \
            {"{'vrf':''}": InterfaceOutput.ShowVrfAllDetail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn(interface='GigabitEthernet0/0/0/1', address_family='ipv6', vrf='VRF1')

        self.maxDiff = None
        # Verify Ops was created successfully
        self.assertDictEqual(intf.info, InterfaceOutput.interfaceOpsOutput_custom_info)

    def test_selective_attribute(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfacesDetail] = \
            {"{'interface':''}": InterfaceOutput.ShowInterfacesDetail}

        intf.maker.outputs[ShowEthernetTags] = \
            {"{'interface':''}": InterfaceOutput.ShowEthernetTags}

        intf.maker.outputs[ShowIpv4VrfAllInterface] = \
            {"{'vrf':''}": InterfaceOutput.ShowIpv4VrfAllInterface}

        intf.maker.outputs[ShowIpv6VrfAllInterface] = \
            {"{'vrf':''}": InterfaceOutput.ShowIpv6VrfAllInterface}

        intf.maker.outputs[ShowVrfAllDetail] = \
            {"{'vrf':''}": InterfaceOutput.ShowVrfAllDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {"{'interface':''}": InterfaceOutput.ShowInterfacesAccounting}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
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
            {"{'interface':''}": InterfaceOutput.ShowInterfacesDetail}

        intf.maker.outputs[ShowEthernetTags] = \
            {"{'interface':''}": InterfaceOutput.ShowEthernetTags}

        intf.maker.outputs[ShowVrfAllDetail] = \
            {"{'vrf':''}": InterfaceOutput.ShowVrfAllDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {"{'interface':''}": InterfaceOutput.ShowInterfacesAccounting}
        outputs['show ipv4 vrf all interface'] = ''
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        intf.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(InterfaceOutput.InterfaceOpsOutput_info)
        del (expect_dict['GigabitEthernet0/0/0/0']['ipv4'])
        del (expect_dict['GigabitEthernet0/0/0/1']['ipv4'])
        # Verify Ops was created successfully
        self.assertEqual(intf.info, expect_dict)
        outputs['show ipv4 vrf all interface'] = InterfaceOutput.ShowIpv4VrfAllInterface_all

if __name__ == '__main__':
    unittest.main()
