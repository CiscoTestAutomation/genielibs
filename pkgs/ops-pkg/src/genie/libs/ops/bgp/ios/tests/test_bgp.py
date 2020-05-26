# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.bgp.ios.bgp import Bgp
from genie.libs.ops.bgp.ios.tests.bgp_output import BgpOutput

# ios show_bgp
from genie.libs.parser.ios.show_bgp import ShowBgpAllSummary, ShowBgpAllClusterIds, \
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

outputs['show bgp all summary'] = BgpOutput.show_bgp_all_summary
outputs['show vrf detail | inc \(VRF'] = BgpOutput.show_vrf_detail
outputs['show bgp all cluster-ids'] = BgpOutput.show_bgp_all_cluster_ids

outputs['show bgp all neighbors'] = BgpOutput.show_bgp_all_neighbors
outputs['show bgp all neighbors 2.2.2.2 policy'] = BgpOutput.show_neighbor_policy_1
outputs['show bgp all neighbors 2001:2:2:2::2 policy'] = BgpOutput.show_neighbor_policy_2
outputs['show bgp all neighbors 2001:3:3:3::3 policy'] = BgpOutput.show_neighbor_policy_3
outputs['show bgp all neighbors 3.3.3.3 policy'] = BgpOutput.show_neighbor_policy_4

outputs['show bgp all'] = BgpOutput.show_bgp_all
outputs['show bgp all detail'] = BgpOutput.show_bgp_all_detail

outputs['show bgp all neighbors 2.2.2.2 routes'] = BgpOutput.nbr_routes_1
outputs['show bgp all neighbors 2001:2:2:2::2 routes'] = BgpOutput.nbr_routes_2
outputs['show bgp all neighbors 2001:3:3:3::3 routes'] = BgpOutput.nbr_routes_3
outputs['show bgp all neighbors 3.3.3.3 routes'] = BgpOutput.nbr_routes_4

outputs['show bgp all neighbors 2.2.2.2 advertised-routes'] = BgpOutput.nbr_adv_routes_1
outputs['show bgp all neighbors 2001:2:2:2::2 advertised-routes'] = BgpOutput.nbr_adv_routes_1
outputs['show bgp all neighbors 2001:3:3:3::3 advertised-routes'] = BgpOutput.nbr_adv_routes_1
outputs['show bgp all neighbors 3.3.3.3 advertised-routes'] = BgpOutput.nbr_adv_routes_1

outputs['show bgp all neighbors 2.2.2.2 received-routes'] = ''
outputs['show bgp all neighbors 2001:2:2:2::2 received-routes'] = ''
outputs['show bgp all neighbors 2001:3:3:3::3 received-routes'] = ''
outputs['show bgp all neighbors 3.3.3.3 received-routes'] = ''

outputs['show bgp vpnv4 unicast all neighbors 2.2.2.2'] = BgpOutput.custom_output_1
outputs['show bgp vpnv4 unicast all'] = BgpOutput.custom_output_2
outputs['show bgp vpnv4 unicast all neighbors 2.2.2.2 advertised-routes'] = BgpOutput.custom_output_3
outputs['show bgp all neighbors | i BGP neighbor'] = BgpOutput.custom_output_4
outputs['show bgp vpnv4 unicast all neighbors 2.2.2.2 routes'] = BgpOutput.custom_output_5
outputs['show bgp vpnv4 unicast all neighbors 2.2.2.2 received-routes'] = ''

outputs['show ip bgp template peer-session'] = ''
outputs['show ip bgp template peer-policy'] = ''
outputs['show ip bgp all dampening parameters'] = ''


def mapper(key):
    return outputs[key]
 

class test_bgp(unittest.TestCase):

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
        bgp = Bgp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Verify Ops was created successfully
        self.assertEqual(bgp.info, BgpOutput.bgp_info)
        self.assertDictEqual(bgp.table, BgpOutput.bgp_table)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.bgp_routes_per_peer)

    def test_custom_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn(address_family='vpnv4 unicast', vrf='default', neighbor='2.2.2.2')

        # Verify Ops was created successfully
        self.assertDictEqual(bgp.info, BgpOutput.bgp_info_custom)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.bgp_routes_per_peer_custom)
        with self.assertRaises(AttributeError):
            bgp.table

    def test_empty_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        outputs['show bgp all summary'] = ''
        outputs['show bgp all'] = ''
        outputs['show bgp all detail'] = ''
        outputs['show bgp all neighbors'] = ''

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        bgp.learn()

        # put back output
        outputs['show bgp all summary'] = BgpOutput.show_bgp_all_summary
        outputs['show bgp all'] = BgpOutput.show_bgp_all
        outputs['show bgp all detail'] = BgpOutput.show_bgp_all_detail
        outputs['show bgp all neighbors'] = BgpOutput.show_bgp_all_neighbors

        # Check no attribute not found
        # info - bgp_id
        with self.assertRaises(KeyError):
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

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Check specific attribute values
        # info - bgp_id
        self.assertEqual(bgp.info['instance']['default']['bgp_id'], 65000)
        # table - bgp_table_version
        self.assertEqual(bgp.table['instance']['default']['vrf']['VRF1']\
                ['address_family']['vpnv4 unicast RD 65000:1']\
                ['bgp_table_version'], 4)
        # routes_per_peer - remote_as
        self.assertEqual(bgp.routes_per_peer['instance']['default']['vrf']\
                ['VRF1']['neighbor']['2.2.2.2']['remote_as'], 65000)


if __name__ == '__main__':
    unittest.main()
