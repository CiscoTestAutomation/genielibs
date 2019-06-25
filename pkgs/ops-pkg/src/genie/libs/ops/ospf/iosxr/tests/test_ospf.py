
# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

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


    def test_complete_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowProtocolsAfiAllAll] = {'':OspfOutput.ShowProtocolsAfiAllAll}
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {'':OspfOutput.ShowOspfVrfAllInclusive}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {'':OspfOutput.ShowOspfVrfAllInclusiveShamLinks}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {'':OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':OspfOutput.ShowOspfMplsTrafficEngLink}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {'':OspfOutput.ShowOspfVrfAllInclusiveInterface}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {'':OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail}

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
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {'':OspfOutput.ShowOspfVrfAllInclusive}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {'':OspfOutput.ShowOspfVrfAllInclusiveShamLinks}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {'':OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':OspfOutput.ShowOspfMplsTrafficEngLink}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {'':OspfOutput.ShowOspfVrfAllInclusiveInterface}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {'':OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail}

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
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {'':{}}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {'':{}}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {'':{}}

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
        ospf.maker.outputs[ShowOspfVrfAllInclusive] = {'':OspfOutput.ShowOspfVrfAllInclusive}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveShamLinks] = {'':OspfOutput.ShowOspfVrfAllInclusiveShamLinks}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveVirtualLinks] = {'':OspfOutput.ShowOspfVrfAllInclusiveVirtualLinks}
        ospf.maker.outputs[ShowOspfMplsTrafficEngLink] = {'':OspfOutput.ShowOspfMplsTrafficEngLink}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseRouter] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseRouter}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseExternal] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseExternal}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseNetwork] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseNetwork}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseSummary] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseSummary}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveDatabaseOpaqueArea] = {'':OspfOutput.ShowOspfVrfAllInclusiveDatabaseOpaqueArea}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveInterface] = {'':OspfOutput.ShowOspfVrfAllInclusiveInterface}
        ospf.maker.outputs[ShowOspfVrfAllInclusiveNeighborDetail] = {'':OspfOutput.ShowOspfVrfAllInclusiveNeighborDetail}

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
