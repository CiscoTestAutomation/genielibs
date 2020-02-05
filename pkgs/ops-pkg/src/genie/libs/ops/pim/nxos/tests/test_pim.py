# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.pim.nxos.pim import Pim
from genie.libs.ops.pim.nxos.tests.pim_output import PimOutput

# Parser
from genie.libs.parser.nxos.show_pim import ShowIpPimInterface,\
                                 ShowIpv6PimVrfAllDetail,\
                                 ShowIpPimRp,\
                                 ShowIpPimGroupRange,\
                                 ShowIpPimVrfDetail,\
                                 ShowIpPimNeighbor,\
                                 ShowIpv6PimGroupRange,\
                                 ShowIpPimRoute,\
                                 ShowIpv6PimNeighbor,\
                                 ShowIpv6PimRoute,\
                                 ShowIpPimDf,\
                                 ShowIpv6PimDf,\
                                 ShowIpv6PimRp,\
                                 ShowIpv6PimInterface, \
                                 ShowIpPimPolicyStaticticsRegisterPolicy

from genie.libs.parser.nxos.show_feature import ShowFeature

from genie.libs.parser.nxos.show_mcast import ShowIpMrouteVrfAll, \
                                   ShowIpv6MrouteVrfAll


class test_pim(unittest.TestCase):

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
        pim = Pim(device=self.device)
        # Get outputs
        pim.maker.outputs[ShowFeature] = \
            {'': PimOutput.ShowFeature}

        pim.maker.outputs[ShowIpMrouteVrfAll] = \
            {'': PimOutput.ShowIpMrouteVrfAll}

        pim.maker.outputs[ShowIpv6MrouteVrfAll] = \
            {'': PimOutput.ShowIpv6MrouteVrfAll}

        pim.maker.outputs[ShowIpPimInterface] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimInterfaceVrfAll}

        pim.maker.outputs[ShowIpv6PimInterface] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimInterfaceVrfAll}

        pim.maker.outputs[ShowIpPimRp] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimRpVrfAll}

        pim.maker.outputs[ShowIpv6PimRp] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimRpVrfAll}            

        pim.maker.outputs[ShowIpPimDf] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimDfVrfAll}

        pim.maker.outputs[ShowIpv6PimDf] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimDfVrfAll}            

        pim.maker.outputs[ShowIpPimVrfDetail] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimVrfVallDetail}

        pim.maker.outputs[ShowIpv6PimVrfAllDetail] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimVrfAllDetail}

        pim.maker.outputs[ShowIpPimGroupRange] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimGroupRangeVrfAll}

        pim.maker.outputs[ShowIpv6PimGroupRange] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimGroupRangeVrfAll}

        pim.maker.outputs[ShowIpPimNeighbor] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimNeighborVrfAll}

        pim.maker.outputs[ShowIpv6PimNeighbor] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimNeighborVrfAll}

        pim.maker.outputs[ShowIpPimRoute] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimRouteVrfAll}

        pim.maker.outputs[ShowIpv6PimRoute] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimRouteVrfAll}

        pim.maker.outputs[ShowIpPimPolicyStaticticsRegisterPolicy] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimPolicyStaticticsRegisterPolicyVrfAll}

        # Learn the feature
        pim.learn()

        # Verify Ops was created successfully
        self.assertEqual(pim.info, PimOutput.Pim_info)

    def test_empty_output(self):
        self.maxDiff = None
        pim = Pim(device=self.device)
        # Get outputs
        pim.maker.outputs[ShowFeature] = \
            {'': {}}

        pim.maker.outputs[ShowIpMrouteVrfAll] = \
            {'': {}}
            
        pim.maker.outputs[ShowIpv6MrouteVrfAll] = \
            {'': {}}

        pim.maker.outputs[ShowIpPimInterface] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpv6PimInterface] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpPimRp] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpv6PimRp] = \
            {"{'vrf':'all'}": {}}            

        pim.maker.outputs[ShowIpPimDf] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpv6PimDf] = \
            {"{'vrf':'all'}": {}}            

        pim.maker.outputs[ShowIpPimVrfDetail] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpv6PimVrfAllDetail] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpPimGroupRange] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpv6PimGroupRange] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpPimNeighbor] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpv6PimNeighbor] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpPimRoute] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpv6PimRoute] = \
            {"{'vrf':'all'}": {}}

        pim.maker.outputs[ShowIpPimPolicyStaticticsRegisterPolicy] = \
            {"{'vrf':'all'}": {}}

        # Learn the feature
        pim.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            pim.info['vrf']
        with self.assertRaises(AttributeError):
            pim.info['feature_pim']
        with self.assertRaises(AttributeError):
            pim.info['feature_pim6']

    def test_selective_attribute(self):
        self.maxDiff = None
        pim = Pim(device=self.device)

        # Get outputs
        pim.maker.outputs[ShowFeature] = \
            {'': PimOutput.ShowFeature}

        pim.maker.outputs[ShowIpMrouteVrfAll] = \
            {'': PimOutput.ShowIpMrouteVrfAll}
            
        pim.maker.outputs[ShowIpv6MrouteVrfAll] = \
            {'': PimOutput.ShowIpv6MrouteVrfAll}

        pim.maker.outputs[ShowIpPimInterface] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimInterfaceVrfAll}

        pim.maker.outputs[ShowIpv6PimInterface] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimInterfaceVrfAll}

        pim.maker.outputs[ShowIpPimRp] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimRpVrfAll}

        pim.maker.outputs[ShowIpv6PimRp] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimRpVrfAll}            

        pim.maker.outputs[ShowIpPimDf] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimDfVrfAll}

        pim.maker.outputs[ShowIpv6PimDf] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimDfVrfAll}            

        pim.maker.outputs[ShowIpPimVrfDetail] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimVrfVallDetail}

        pim.maker.outputs[ShowIpv6PimVrfAllDetail] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimVrfAllDetail}

        pim.maker.outputs[ShowIpPimGroupRange] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimGroupRangeVrfAll}

        pim.maker.outputs[ShowIpv6PimGroupRange] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimGroupRangeVrfAll}

        pim.maker.outputs[ShowIpPimNeighbor] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimNeighborVrfAll}

        pim.maker.outputs[ShowIpv6PimNeighbor] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimNeighborVrfAll}

        pim.maker.outputs[ShowIpPimRoute] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimRouteVrfAll}

        pim.maker.outputs[ShowIpv6PimRoute] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimRouteVrfAll}

        pim.maker.outputs[ShowIpPimPolicyStaticticsRegisterPolicy] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimPolicyStaticticsRegisterPolicyVrfAll}

        # Learn the feature
        pim.learn()      

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(pim.info['vrf']['default']['interfaces']\
                                 ['Ethernet2/1']['address_family']\
                                 ['ipv4']['dr_priority'], 1)
        # info - vrf VRF1
        self.assertEqual(pim.info['vrf']['VRF1']['address_family']\
                                  ['ipv6']['topology_tree_info']\
                                  ['ff30::/12 * True']['is_rpt'], True)

    def test_incomplete_output(self):
        self.maxDiff = None
        
        pim = Pim(device=self.device)

        # Get outputs
        pim.maker.outputs[ShowFeature] = \
            {'': {}}

        pim.maker.outputs[ShowIpMrouteVrfAll] = \
            {'': PimOutput.ShowIpMrouteVrfAll}
            
        pim.maker.outputs[ShowIpv6MrouteVrfAll] = \
            {'': PimOutput.ShowIpv6MrouteVrfAll}

        pim.maker.outputs[ShowIpPimInterface] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimInterfaceVrfAll}

        pim.maker.outputs[ShowIpv6PimInterface] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimInterfaceVrfAll}

        pim.maker.outputs[ShowIpPimRp] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimRpVrfAll}

        pim.maker.outputs[ShowIpv6PimRp] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimRpVrfAll}            

        pim.maker.outputs[ShowIpPimDf] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimDfVrfAll}

        pim.maker.outputs[ShowIpv6PimDf] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimDfVrfAll}            

        pim.maker.outputs[ShowIpPimVrfDetail] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimVrfVallDetail}

        pim.maker.outputs[ShowIpv6PimVrfAllDetail] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimVrfAllDetail}

        pim.maker.outputs[ShowIpPimGroupRange] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimGroupRangeVrfAll}

        pim.maker.outputs[ShowIpv6PimGroupRange] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimGroupRangeVrfAll}

        pim.maker.outputs[ShowIpPimNeighbor] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimNeighborVrfAll}

        pim.maker.outputs[ShowIpv6PimNeighbor] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimNeighborVrfAll}

        pim.maker.outputs[ShowIpPimRoute] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimRouteVrfAll}

        pim.maker.outputs[ShowIpv6PimRoute] = \
            {"{'vrf':'all'}": PimOutput.ShowIpv6PimRouteVrfAll}

        pim.maker.outputs[ShowIpPimPolicyStaticticsRegisterPolicy] = \
            {"{'vrf':'all'}": PimOutput.ShowIpPimPolicyStaticticsRegisterPolicyVrfAll}

        # Learn the feature
        pim.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(PimOutput.Pim_info)
        del(expect_dict['feature_pim6'])
        del(expect_dict['feature_pim'])

                
        # Verify Ops was created successfully
        self.assertEqual(pim.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
