
# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.ospf.nxos.ospf import Ospf
from genie.libs.ops.ospf.nxos.tests.ospf_output import OspfOutput

# Parser
from genie.libs.parser.nxos.show_ospf import ShowIpOspf,\
                                  ShowIpOspfMplsLdpInterface,\
                                  ShowIpOspfVirtualLinks,\
                                  ShowIpOspfShamLinks,\
                                  ShowIpOspfInterface,\
                                  ShowIpOspfNeighborDetail,\
                                  ShowIpOspfDatabaseExternalDetail,\
                                  ShowIpOspfDatabaseNetworkDetail,\
                                  ShowIpOspfDatabaseSummaryDetail,\
                                  ShowIpOspfDatabaseRouterDetail,\
                                  ShowIpOspfDatabaseOpaqueAreaDetail

# nxos show_feature
from genie.libs.parser.nxos.show_feature import ShowFeature

# Set values
outputs = {}
outputs['show feature'] = OspfOutput.ShowFeature
outputs['show ip ospf vrf all'] = OspfOutput.ShowIpOspfVrfAll
outputs['show ip ospf mpls ldp interface vrf all'] = OspfOutput.ShowIpOspfMplsLdpInterfaceVrfAll
outputs['show ip ospf virtual-links vrf all'] = OspfOutput.ShowIpOspfVirtualLinksVrfAll
outputs['show ip ospf sham-links vrf all'] = OspfOutput.ShowIpOspfShamLinksVrfAll
outputs['show ip ospf interface vrf all'] = OspfOutput.ShowIpOspfInterfaceVrfAll
outputs['show ip ospf neighbors detail vrf all'] = OspfOutput.ShowIpOspfNeighborDetailVrfAll
outputs['show ip ospf database external detail vrf all'] = OspfOutput.ShowIpOspfDatabaseExternalDetailVrfAll
outputs['show ip ospf database network detail vrf all'] = OspfOutput.ShowIpOspfDatabaseNetworkDetailVrfAll
outputs['show ip ospf database summary detail vrf all'] = OspfOutput.ShowIpOspfDatabaseSummaryDetailVrfAll
outputs['show ip ospf database router detail vrf all'] = OspfOutput.ShowIpOspfDatabaseRouterDetailVrfAll
outputs['show ip ospf database opaque-area detail vrf all'] = OspfOutput.ShowIpOspfDatabaseOpaqueAreaDetailVrfAll


def mapper(key):
    return outputs[key]


class test_ospf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_custom_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)

        # Set outputs
        ospf.maker.outputs[ShowFeature] = {'': OspfOutput.ShowFeature}
        ospf.maker.outputs[ShowIpOspf] = {"{'vrf':'VRF1'}": OspfOutput.ShowIpOspfVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {
            "{'interface':'Ethernet2/1','vrf':'VRF1'}": OspfOutput.ShowIpOspfMplsLdpInterfaceVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowIpOspfVirtualLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowIpOspfShamLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfInterface] = {
            "{'interface':'Ethernet2/1','vrf':'VRF1'}": OspfOutput.ShowIpOspfInterfaceVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {
            "{'neighbor':'10.84.66.66','vrf':'VRF1'}": OspfOutput.ShowIpOspfNeighborDetailVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfDatabaseExternalDetail] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowIpOspfDatabaseExternalDetailVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfDatabaseNetworkDetail] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowIpOspfDatabaseNetworkDetailVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfDatabaseSummaryDetail] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowIpOspfDatabaseSummaryDetailVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfDatabaseRouterDetail] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowIpOspfDatabaseRouterDetailVrfAll_custom}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueAreaDetail] = {
            "{'vrf':'VRF1'}": OspfOutput.ShowIpOspfDatabaseOpaqueAreaDetailVrfAll_custom}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn(vrf='VRF1', interface='Ethernet2/1', neighbor='10.84.66.66')

        # Verify Ops was created successfully
        self.assertEqual(ospf.info, OspfOutput.OspfInfo_custom)

    def test_complete_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowFeature] = {'':OspfOutput.ShowFeature}
        ospf.maker.outputs[ShowIpOspf] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfVrfAll}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':'','vrf':'all'}":OspfOutput.ShowIpOspfMplsLdpInterfaceVrfAll}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfVirtualLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfShamLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':'','vrf':'all'}":OspfOutput.ShowIpOspfInterfaceVrfAll}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':'','vrf':'all'}":OspfOutput.ShowIpOspfNeighborDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseExternalDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseExternalDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseNetworkDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseNetworkDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseSummaryDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseSummaryDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseRouterDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseRouterDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueAreaDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseOpaqueAreaDetailVrfAll}
        
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
        ospf.maker.outputs[ShowFeature] = {'':OspfOutput.ShowFeature}
        ospf.maker.outputs[ShowIpOspf] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfVrfAll}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':'','vrf':'all'}":OspfOutput.ShowIpOspfMplsLdpInterfaceVrfAll}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfVirtualLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfShamLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':'','vrf':'all'}":OspfOutput.ShowIpOspfInterfaceVrfAll}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':'','vrf':'all'}":OspfOutput.ShowIpOspfNeighborDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseExternalDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseExternalDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseNetworkDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseNetworkDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseSummaryDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseSummaryDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseRouterDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseRouterDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueAreaDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseOpaqueAreaDetailVrfAll}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn()

        # Check selective attribute
        self.assertEqual(646, ospf.info['vrf']['VRF1']['address_family']\
                                    ['ipv4']['instance']['1']['areas']\
                                    ['0.0.0.1']['database']['lsa_types'][1]\
                                    ['lsas']['10.229.11.11 10.229.11.11']\
                                    ['ospfv2']['header']['age'])

    def test_empty_output(self):
        self.maxDiff = None
        ospf = Ospf(device=self.device)
        
        # Set outputs
        ospf.maker.outputs[ShowFeature] = {'':{}}
        ospf.maker.outputs[ShowIpOspf] = {"{'vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':'','vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {"{'vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {"{'vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':'','vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':'','vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfDatabaseExternalDetail] = {"{'vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfDatabaseNetworkDetail] = {"{'vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfDatabaseSummaryDetail] = {"{'vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfDatabaseRouterDetail] = {"{'vrf':'all'}":{}}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueAreaDetail] = {"{'vrf':'all'}":{}}

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
        ospf.maker.outputs[ShowFeature] = {'':{}}
        ospf.maker.outputs[ShowIpOspf] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfVrfAll}
        ospf.maker.outputs[ShowIpOspfMplsLdpInterface] = {"{'interface':'','vrf':'all'}":OspfOutput.ShowIpOspfMplsLdpInterfaceVrfAll}
        ospf.maker.outputs[ShowIpOspfVirtualLinks] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfVirtualLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfShamLinks] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfShamLinksVrfAll}
        ospf.maker.outputs[ShowIpOspfInterface] = {"{'interface':'','vrf':'all'}":OspfOutput.ShowIpOspfInterfaceVrfAll}
        ospf.maker.outputs[ShowIpOspfNeighborDetail] = {"{'neighbor':'','vrf':'all'}":OspfOutput.ShowIpOspfNeighborDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseExternalDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseExternalDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseNetworkDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseNetworkDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseSummaryDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseSummaryDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseRouterDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseRouterDetailVrfAll}
        ospf.maker.outputs[ShowIpOspfDatabaseOpaqueAreaDetail] = {"{'vrf':'all'}":OspfOutput.ShowIpOspfDatabaseOpaqueAreaDetailVrfAll}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ospf.learn()

        # Verify key not created due to ouput missing
        with self.assertRaises(KeyError):
            feature_ospf = ospf.info['feature_ospf']


if __name__ == '__main__':
    unittest.main()