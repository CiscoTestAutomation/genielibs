
# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.ospf.ios.ospf import Ospf
from genie.libs.ops.ospf.ios.tests.ospf_output import OspfOutput

# ios show_ospf
from genie.libs.parser.ios.show_ospf import ShowIpOspf,\
                                   ShowIpOspfInterface,\
                                   ShowIpOspfNeighborDetail,\
                                   ShowIpOspfShamLinks,\
                                   ShowIpOspfVirtualLinks,\
                                   ShowIpOspfDatabaseRouter,\
                                   ShowIpOspfDatabaseExternal,\
                                   ShowIpOspfDatabaseNetwork,\
                                   ShowIpOspfDatabaseSummary,\
                                   ShowIpOspfDatabaseOpaqueArea,\
                                   ShowIpOspfMplsLdpInterface,\
                                   ShowIpOspfMplsTrafficEngLink

# iosxe show_ospf
from genie.libs.parser.iosxe.show_protocols import ShowIpProtocols

outputs = {}

# Set values
outputs['show ip protocols'] = OspfOutput.ShowIpProtocols
outputs['show ip ospf'] = OspfOutput.ShowIpOspf
outputs['show ip ospf interface'] = OspfOutput.ShowIpOspfInterface
outputs['show ip ospf neighbors detail'] = OspfOutput.ShowIpOspfNeighborDetail
outputs['show ip ospf sham-links'] = OspfOutput.ShowIpOspfShamLinks
outputs['show ip ospf virutal-links'] = OspfOutput.ShowIpOspfVirtualLinks
outputs['show ip ospf database router'] = OspfOutput.ShowIpOspfDatabaseRouter
outputs['show ip ospf database external'] = OspfOutput.ShowIpOspfDatabaseExternal
outputs['show ip ospf database summary'] = OspfOutput.ShowIpOspfDatabaseNetwork
outputs['show ip ospf database network'] = OspfOutput.ShowIpOspfDatabaseSummary
outputs['show ip ospf database opaque-area'] = OspfOutput.ShowIpOspfDatabaseOpaqueArea
outputs['show ip ospf mpls traffic-eng link'] = OspfOutput.ShowIpOspfMplsLdpInterface
outputs['show ip ospf mpls traffic-eng link'] = OspfOutput.ShowIpOspfMplsTrafficEngLink


def mapper(key):
    return outputs[key]


class test_ospf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device


    def test_complete_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowIpProtocols] = {"{'vrf':''}":OspfOutput.ShowIpProtocols}
        ospf.maker.outputs[ShowIpOspf] = {'':OspfOutput.ShowIpOspf}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':''}":OspfOutput.ShowIpOspfInterface}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':''}":OspfOutput.ShowIpOspfNeighborDetail}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {'':OspfOutput.ShowIpOspfShamLinks}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {'':OspfOutput.ShowIpOspfVirtualLinks}
        ospf.maker.outputs[ShowIpOspfDatabaseRouter] = {'':OspfOutput.ShowIpOspfDatabaseRouter}
        ospf.maker.outputs[ShowIpOspfDatabaseExternal] = {'':OspfOutput.ShowIpOspfDatabaseExternal}
        ospf.maker.outputs[ShowIpOspfDatabaseNetwork] = {'':OspfOutput.ShowIpOspfDatabaseNetwork}
        ospf.maker.outputs[ShowIpOspfDatabaseSummary] = {'':OspfOutput.ShowIpOspfDatabaseSummary}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueArea] = {'':OspfOutput.ShowIpOspfDatabaseOpaqueArea}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':''}":OspfOutput.ShowIpOspfMplsLdpInterface}
        ospf.maker.outputs[ShowIpOspfMplsTrafficEngLink] = {'':OspfOutput.ShowIpOspfMplsTrafficEngLink}

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
        ospf.maker.outputs[ShowIpProtocols] = {"{'vrf':''}":OspfOutput.ShowIpProtocols}
        ospf.maker.outputs[ShowIpOspf] = {'':OspfOutput.ShowIpOspf}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':''}":OspfOutput.ShowIpOspfInterface}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':''}":OspfOutput.ShowIpOspfNeighborDetail}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {'':OspfOutput.ShowIpOspfShamLinks}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {'':OspfOutput.ShowIpOspfVirtualLinks}
        ospf.maker.outputs[ShowIpOspfDatabaseRouter] = {'':OspfOutput.ShowIpOspfDatabaseRouter}
        ospf.maker.outputs[ShowIpOspfDatabaseExternal] = {'':OspfOutput.ShowIpOspfDatabaseExternal}
        ospf.maker.outputs[ShowIpOspfDatabaseNetwork] = {'':OspfOutput.ShowIpOspfDatabaseNetwork}
        ospf.maker.outputs[ShowIpOspfDatabaseSummary] = {'':OspfOutput.ShowIpOspfDatabaseSummary}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueArea] = {'':OspfOutput.ShowIpOspfDatabaseOpaqueArea}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':''}":OspfOutput.ShowIpOspfMplsLdpInterface}
        ospf.maker.outputs[ShowIpOspfMplsTrafficEngLink] = {'':OspfOutput.ShowIpOspfMplsTrafficEngLink}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn()

        # Check selective attribute
        self.assertEqual(288, ospf.info['vrf']['VRF1']['address_family']\
                                    ['ipv4']['instance']['2']['areas']\
                                    ['0.0.0.1']['database']['lsa_types'][1]\
                                    ['lsas']['10.1.77.77 10.1.77.77']\
                                    ['ospfv2']['header']['age'])


    def test_empty_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowIpProtocols] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowIpOspf] = {'':{}}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':''}":{}}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':''}":{}}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {'':{}}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {'':{}}
        ospf.maker.outputs[ShowIpOspfDatabaseRouter] = {'':{}}
        ospf.maker.outputs[ShowIpOspfDatabaseExternal] = {'':{}}
        ospf.maker.outputs[ShowIpOspfDatabaseNetwork] = {'':{}}
        ospf.maker.outputs[ShowIpOspfDatabaseSummary] = {'':{}}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueArea] = {'':{}}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':''}":{}}
        ospf.maker.outputs[ShowIpOspfMplsTrafficEngLink] = {'':{}}

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
        ospf.maker.outputs[ShowIpProtocols] = {"{'vrf':''}":{}}
        ospf.maker.outputs[ShowIpOspf] = {'':OspfOutput.ShowIpOspf}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':''}":OspfOutput.ShowIpOspfInterface}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':''}":OspfOutput.ShowIpOspfNeighborDetail}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {'':OspfOutput.ShowIpOspfShamLinks}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {'':OspfOutput.ShowIpOspfVirtualLinks}
        ospf.maker.outputs[ShowIpOspfDatabaseRouter] = {'':OspfOutput.ShowIpOspfDatabaseRouter}
        ospf.maker.outputs[ShowIpOspfDatabaseExternal] = {'':OspfOutput.ShowIpOspfDatabaseExternal}
        ospf.maker.outputs[ShowIpOspfDatabaseNetwork] = {'':OspfOutput.ShowIpOspfDatabaseNetwork}
        ospf.maker.outputs[ShowIpOspfDatabaseSummary] = {'':OspfOutput.ShowIpOspfDatabaseSummary}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueArea] = {'':OspfOutput.ShowIpOspfDatabaseOpaqueArea}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':''}":OspfOutput.ShowIpOspfMplsLdpInterface}
        ospf.maker.outputs[ShowIpOspfMplsTrafficEngLink] = {'':OspfOutput.ShowIpOspfMplsTrafficEngLink}

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
