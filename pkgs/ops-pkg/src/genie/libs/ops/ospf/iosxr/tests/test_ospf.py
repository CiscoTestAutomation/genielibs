
# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.ospf.iosxr.ospf import Ospf
from genie.libs.ops.ospf.iosxr.tests.ospf_output import OspfOutput

# iosxr show_ospf
from genie.libs.parser.iosxr.show_ospf import ShowOspfVrfAllInclusiveInterface,\
                                   ShowOspfVrfAllInclusiveNeighborDetail,\
                                   ShowOspfVrfAllInclusive,\
                                   ShowOspfVrfAllInclusiveShamLinks,\
                                   ShowOspfVrfAllInclusiveVirtualLinks,\
                                   ShowOspfMplsTrafficEngLink,\
                                   ShowOspfVrfAllInclusiveDatabaseRouter,\
                                   ShowOspfVrfAllInclusiveDatabaseExternal,\
                                   ShowOspfVrfAllInclusiveDatabaseNetwork,\
                                   ShowOspfVrfAllInclusiveDatabaseSummary,\
                                   ShowOspfVrfAllInclusiveDatabaseOpaqueArea

# iosxr show_ospf
from genie.libs.parser.iosxr.show_protocol import ShowProtocolsAfiAllAll

outputs = {}

# Set values
outputs['show protocols afi-all all'] = OspfOutput.ShowProtocolsAfiAllAll
outputs['show ospf vrf all-inclusive'] = OspfOutput.ShowOspfVrfAllInclusive
outputs['show ospf vrf all-inclusive sham-links'] = OspfOutput.ShowOspfVrfAllInclusiveShamLinks
outputs['show ospf vrf all-inclusive virutal-links'] = OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks
outputs['show ospf mpls traffic-eng link'] = OspfOutput.ShowOspfMplsTrafficEngLink
outputs['show ospf vrf all-inclusive database router'] = OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter
outputs['show ospf vrf all-inclusive database external'] = OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal
outputs['show ospf vrf all-inclusive database summary'] = OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork
outputs['show ospf vrf all-inclusive database network'] = OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary
outputs['show ospf vrf all-inclusive database opaque-area'] = OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea
outputs['show ospf vrf all-inclusive interface'] = OspfOutput.ShowOspfVrfAllInclusiveInterface
outputs['show ospf vrf all-inclusive neighbors detail'] = OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail


def mapper(key):
    return outputs[key]


class test_ospf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_custom_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)

        # Set outputs
        ospf.maker.outputs[ShowProtocolsAfiAllAll] = {
            '': OspfOutput.ShowProtocolsAfiAllAll}
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusive_custom}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveShamLinks}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {
            '': OspfOutput.ShowOspfMplsTrafficEngLink}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter_custom}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal_custom}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork_custom}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary_custom}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea_custom}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {
            "{'interface':'GigabitEthernet0/0/0/1','vrf':'VRF1'}": OspfOutput.ShowOspfVrfAllInclusiveInterface_custom}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {
            "{'interface':'GigabitEthernet0/0/0/1','neighbor':'10.36.3.3','vrf':'VRF1'}":
                OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail_custom}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn(vrf='VRF1', interface='GigabitEthernet0/0/0/1', neighbor='10.36.3.3')

        # Verify Ops was created successfully
        self.assertEqual(ospf.info, OspfOutput.OspfInfo_custom)

    def test_complete_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowProtocolsAfiAllAll] = {'':OspfOutput.ShowProtocolsAfiAllAll}
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusive}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveShamLinks}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':OspfOutput.ShowOspfMplsTrafficEngLink}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {"{'interface':'','vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveInterface}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {"{'interface':'','neighbor':'','vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn()

        # Verify Ops was created successfully
        self.assertEqual(ospf.info, OspfOutput.OspfInfo)

    def test_selective_attribute(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowProtocolsAfiAllAll] = {'':OspfOutput.ShowProtocolsAfiAllAll}
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusive}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveShamLinks}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':OspfOutput.ShowOspfMplsTrafficEngLink}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {"{'interface':'','vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveInterface}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {"{'interface':'','neighbor':'','vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn()

        # Check selective attribute
        self.assertEqual(1713, ospf.info['vrf']['VRF1']['address_family']\
                                    ['ipv4']['instance']['1']['areas']\
                                    ['0.0.0.1']['database']['lsa_types'][1]\
                                    ['lsas']['10.229.11.11 10.229.11.11']\
                                    ['ospfv2']['header']['age'])

    def test_empty_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowProtocolsAfiAllAll] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {"{'interface':'','vrf':''}":{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {"{'interface':'','neighbor':'','vrf':''}":{}}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn()

        # Verify attribute is missing
        with self.assertRaises(AttributeError):
            ospf.info['vrf']


    def test_missing_attributes(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowProtocolsAfiAllAll] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusive}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveShamLinks}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':OspfOutput.ShowOspfMplsTrafficEngLink}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {"{'vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {"{'interface':'','vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveInterface}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {"{'interface':'','neighbor':'','vrf':''}":OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn()

        # Verify key not created due to ouput missing
        with self.assertRaises(KeyError):
            single_value_preference = ospf.info['vrf']['default']\
                                        ['address_family']['ipv4']['instance']\
                                        ['1']['preference']['single_value']['all']


if __name__ == '__main__':
    unittest.main()
