# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Genie
from genie.libs.ops.bgp.iosxe.bgp import Bgp
from genie.libs.ops.bgp.iosxe.tests.bgp_output import BgpOutput

# iosxe show_bgp
from genie.libs.parser.iosxe.show_bgp import ShowBgpAllSummary, ShowBgpAllClusterIds, \
                                  ShowBgpAllNeighborsAdvertisedRoutes, \
                                  ShowBgpAllNeighborsReceivedRoutes, \
                                  ShowBgpAllNeighborsRoutes, \
                                  ShowIpBgpTemplatePeerPolicy, \
                                  ShowBgpAllNeighbors, \
                                  ShowIpBgpAllDampeningParameters, \
                                  ShowIpBgpTemplatePeerSession, \
                                  ShowBgpAllNeighborsPolicy, \
                                  ShowBgpAllDetail, \
                                  ShowBgpAll

outputs = {}

outputs['show bgp vpnv4 unicast all neighbors 10.16.2.2 advertised-routes'] = BgpOutput.nbr1_ipv4_advertised_routes
outputs['show bgp vpnv4 unicast all neighbors 10.16.2.2 routes'] = BgpOutput.nbr1_ipv4_routes
outputs['show bgp vpnv4 unicast all neighbors 10.16.2.2 received-routes'] = BgpOutput.nbr1_ipv4_received_routes

outputs['show bgp all neighbors 10.16.2.2 policy'] = BgpOutput.nbr1_bgp_policy
outputs['show bgp all neighbors 10.36.3.3 policy'] = BgpOutput.nbr2_bgp_policy
outputs['show bgp all neighbors | i BGP neighbor'] = BgpOutput.nbr1_bgp_all_neighbors
outputs['show bgp all neighbors 10.16.2.2 advertised-routes'] = BgpOutput.nbr1_advertised_routes
outputs['show bgp all neighbors 10.16.2.2 routes'] = BgpOutput.nbr1_routes
outputs['show bgp all neighbors 10.16.2.2 received-routes'] = BgpOutput.nbr1_received_routes
outputs['show bgp all neighbors | i BGP neighbor'] = BgpOutput.bgp_all_neighbors
outputs['show bgp all neighbors 10.36.3.3 advertised-routes'] = BgpOutput.nbr2_advertised_routes
outputs['show bgp all neighbors 10.36.3.3 routes'] = BgpOutput.nbr2_routes
outputs['show bgp all neighbors 10.36.3.3 received-routes'] = BgpOutput.nbr2_received_routes


def mapper(key):
    return outputs[key]


class test_bgp(unittest.TestCase):

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
        bgp = Bgp(device=self.device)

        # Get outputs
        bgp.maker.outputs[ShowBgpAllSummary] = \
            {"{'address_family':'','vrf':''}":BgpOutput.ShowBgpAllSummary}
        bgp.maker.outputs[ShowBgpAllClusterIds] = \
            {'':BgpOutput.ShowBgpAllClusterIds}
        bgp.maker.outputs[ShowIpBgpTemplatePeerPolicy] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerPolicy}
        bgp.maker.outputs[ShowBgpAllNeighbors] = \
            {"{'address_family':'','neighbor':''}":BgpOutput.ShowBgpAllNeighbors}
        bgp.maker.outputs[ShowIpBgpAllDampeningParameters] = \
            {'':BgpOutput.ShowIpBgpAllDampeningParameters}
        bgp.maker.outputs[ShowIpBgpTemplatePeerSession] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerSession}
        bgp.maker.outputs[ShowBgpAllDetail] = \
            {"{'address_family':'','vrf':''}":BgpOutput.ShowBgpAllDetail}
        bgp.maker.outputs[ShowBgpAll] = \
            {"{'address_family':''}":BgpOutput.ShowBgpAll}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Verify Ops was created successfully
        self.assertEqual(bgp.info, BgpOutput.BgpOpsOutput_info)
        self.assertDictEqual(bgp.table, BgpOutput.BgpOpsOutput_table)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.BgpOpsOutput_routesperpeer)

    def test_custom_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        outputs[
            'show bgp all neighbors | i BGP neighbor'] = BgpOutput.nbr1_bgp_all_neighbors
        # Get outputs
        bgp.maker.outputs[ShowBgpAllSummary] = \
            {"{'address_family':'vpnv4 unicast','vrf':'VRF1'}":BgpOutput.ShowBgpAllSummary_custom}
        bgp.maker.outputs[ShowBgpAllClusterIds] = \
            {'':BgpOutput.ShowBgpAllClusterIds}
        bgp.maker.outputs[ShowIpBgpTemplatePeerPolicy] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerPolicy}
        bgp.maker.outputs[ShowBgpAllNeighbors] = \
            {"{'address_family':'vpnv4 unicast','neighbor':'10.16.2.2'}":BgpOutput.ShowBgpAllNeighbors_nbr1}
        bgp.maker.outputs[ShowIpBgpAllDampeningParameters] = \
            {'':BgpOutput.ShowIpBgpAllDampeningParameters}
        bgp.maker.outputs[ShowIpBgpTemplatePeerSession] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerSession}
        bgp.maker.outputs[ShowBgpAllDetail] = \
            {"{'address_family':'vpnv4 unicast','vrf':'VRF1'}":BgpOutput.ShowBgpAllDetail_custom}
        bgp.maker.outputs[ShowBgpAll] = \
            {"{'address_family':'vpnv4 unicast'}":BgpOutput.ShowBgpAll_custom}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn(address_family='vpnv4 unicast RD 300:1', vrf='VRF1', neighbor='10.16.2.2')
        outputs[
            'show bgp all neighbors | i BGP neighbor'] = BgpOutput.bgp_all_neighbors
        # Verify Ops was created successfully
        self.assertDictEqual(bgp.info, BgpOutput.BgpOpsOutput_info_custom)
        self.assertDictEqual(bgp.table, BgpOutput.BgpOpsOutput_table_custom)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.BgpOpsOutput_routesperpeer_custom)

    def test_empty_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        bgp.maker.outputs[ShowBgpAllSummary] = \
            {"{'address_family':'','vrf':''}":''}
        bgp.maker.outputs[ShowBgpAllClusterIds] = \
            {'':''}
        bgp.maker.outputs[ShowIpBgpTemplatePeerPolicy] = \
            {'':''}
        bgp.maker.outputs[ShowBgpAllNeighbors] = \
            {"{'address_family':'','neighbor':''}":''}
        bgp.maker.outputs[ShowIpBgpAllDampeningParameters] = \
            {'':''}
        bgp.maker.outputs[ShowIpBgpTemplatePeerSession] = \
            {'':''}
        bgp.maker.outputs[ShowBgpAllDetail] = \
            {"{'address_family':'','vrf':''}":''}
        bgp.maker.outputs[ShowBgpAll] = \
            {"{'address_family':''}":''}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        bgp.learn()

        # Check no attribute not found
        # info - bgp_id
        with self.assertRaises(AttributeError):
            bgp_id = (bgp.info['instance']['default']['bgp_id'])
        # table - bgp_table_version
        with self.assertRaises(AttributeError):
            bgp_table_version = (bgp.table['instance']['default']['vrf']\
                ['default']['address_family']['ipv4 unicast']\
                ['bgp_table_version'])
        # routes_per_peer - remote_as
        with self.assertRaises(AttributeError):
            remote_as = (bgp.routes_per_peer['instance']['default']['vrf']\
                ['default']['neighbor']['10.16.2.2']['remote_as'])

    def test_selective_attribute(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)

        # Get outputs
        bgp.maker.outputs[ShowBgpAllSummary] = \
            {"{'address_family':'','vrf':''}":BgpOutput.ShowBgpAllSummary}
        bgp.maker.outputs[ShowBgpAllClusterIds] = \
            {'':BgpOutput.ShowBgpAllClusterIds}
        bgp.maker.outputs[ShowIpBgpTemplatePeerPolicy] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerPolicy}
        bgp.maker.outputs[ShowBgpAllNeighbors] = \
            {"{'address_family':'','neighbor':''}":BgpOutput.ShowBgpAllNeighbors}
        bgp.maker.outputs[ShowIpBgpAllDampeningParameters] = \
            {'':BgpOutput.ShowIpBgpAllDampeningParameters}
        bgp.maker.outputs[ShowIpBgpTemplatePeerSession] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerSession}
        bgp.maker.outputs[ShowBgpAllDetail] = \
            {"{'address_family':'','vrf':''}":BgpOutput.ShowBgpAllDetail}
        bgp.maker.outputs[ShowBgpAll] = \
            {"{'address_family':''}":BgpOutput.ShowBgpAll}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Check specific attribute values
        # info - bgp_id
        self.assertEqual(bgp.info['instance']['default']['bgp_id'], 100)
        # table - bgp_table_version
        self.assertEqual(bgp.table['instance']['default']['vrf']['evpn1']\
                ['address_family']['vpnv4 unicast RD 65535:1']\
                ['bgp_table_version'], 5)
        # routes_per_peer - localprf
        self.assertEqual(bgp.routes_per_peer['instance']['default']['vrf']\
                ['default']['neighbor']['10.16.2.2']['address_family']\
                ['ipv4 unicast']['advertised']['10.1.1.0/24']['index'][1]\
                ['localprf'], 100)

    def test_incomplete_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)

        # Get outputs
        bgp.maker.outputs[ShowBgpAllSummary] = \
            {"{'address_family':'','vrf':''}":BgpOutput.ShowBgpAllSummary}
        bgp.maker.outputs[ShowBgpAllClusterIds] = \
            {'':BgpOutput.ShowBgpAllClusterIds}
        bgp.maker.outputs[ShowIpBgpTemplatePeerPolicy] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerPolicy}
        bgp.maker.outputs[ShowBgpAllNeighbors] = \
            {"{'address_family':'','neighbor':''}":BgpOutput.ShowBgpAllNeighbors}
        bgp.maker.outputs[ShowIpBgpAllDampeningParameters] = \
            {'':BgpOutput.ShowIpBgpAllDampeningParameters}
        bgp.maker.outputs[ShowIpBgpTemplatePeerSession] = \
            {'':BgpOutput.ShowIpBgpTemplatePeerSession}
        bgp.maker.outputs[ShowBgpAllDetail] = \
            {"{'address_family':'','vrf':''}":BgpOutput.ShowBgpAllDetail}
        bgp.maker.outputs[ShowBgpAll] = \
            {"{'address_family':''}":BgpOutput.ShowBgpAll}

        # Outputs from side_effect set to empty
        bgp.maker.outputs[ShowBgpAllNeighborsPolicy] = {'':''}
        bgp.maker.outputs[ShowBgpAllNeighborsAdvertisedRoutes] = {'':''}
        bgp.maker.outputs[ShowBgpAllNeighborsRoutes] = {'':''}
        bgp.maker.outputs[ShowBgpAllNeighborsReceivedRoutes] = {'':''}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = ['', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '']

        # Learn the feature
        bgp.learn()

        # Check attribute values of output provided is found
        
        # bgp.info - bgp_id
        self.assertEqual(bgp.info['instance']['default']['bgp_id'], 100)

if __name__ == '__main__':
    unittest.main()
