# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.bgp.nxos.bgp import Bgp
from genie.libs.ops.bgp.nxos.tests.bgp_output import BgpOutput

# nxos show_bgp
from genie.libs.parser.nxos.show_bgp import ShowBgpProcessVrfAll, ShowBgpPeerSession,\
                                 ShowBgpPeerPolicy, ShowBgpPeerTemplate,\
                                 ShowBgpVrfAllAll,\
                                 ShowBgpVrfAllNeighbors,\
                                 ShowBgpVrfAllAllNextHopDatabase,\
                                 ShowBgpVrfAllAllSummary,\
                                 ShowBgpVrfAllAllDampeningParameters,\
                                 ShowBgpVrfAllNeighborsAdvertisedRoutes,\
                                 ShowBgpVrfAllNeighborsRoutes,\
                                 ShowBgpVrfAllNeighborsReceivedRoutes

# nxos show_vrf
from genie.libs.parser.nxos.show_vrf import ShowVrf

# nxos show_routing
from genie.libs.parser.nxos.show_routing import ShowRoutingVrfAll

outputs = {}
outputs['show bgp vrf VRF1 all neighbors'] = BgpOutput.vrf_vrf1_output
outputs['show bgp vrf VRF1 ipv4 unicast neighbors 10.16.2.10'] = BgpOutput.vrf_vrf1_output
outputs['show bgp vrf default all neighbors'] = BgpOutput.vrf_default_output

outputs['show bgp vrf VRF1 all neighbors 10.16.2.10 advertised-routes'] = BgpOutput.nbr1_advertised_routes
outputs['show bgp vrf VRF1 ipv4 unicast neighbors 10.16.2.10 advertised-routes'] = BgpOutput.nbr1_advertised_routes_ipv4
outputs['show bgp vrf VRF1 all neighbors 10.16.2.10 routes'] = BgpOutput.nbr1_routes
outputs['show bgp vrf VRF1 ipv4 unicast neighbors 10.16.2.10 routes'] = BgpOutput.nbr1_routes_ipv4
outputs['show bgp vrf VRF1 all neighbors 10.16.2.10 received-routes'] = BgpOutput.nbr1_received_routes
outputs['show bgp vrf VRF1 ipv4 unicast neighbors 10.16.2.10 received-routes'] = BgpOutput.nbr1_received_routes_ipv4
outputs['show bgp vrf default all neighbors 10.16.2.2 advertised-routes'] = BgpOutput.nbr2_advertised_routes
outputs['show bgp vrf default all neighbors 10.16.2.2 routes'] = BgpOutput.nbr2_routes
outputs['show bgp vrf default all neighbors 10.16.2.2 received-routes'] = BgpOutput.nbr2_received_routes
outputs['show bgp process vrf all'] = BgpOutput.ShowBgpProcessVrfAll_all


def mapper(key):
    return outputs[key]


class test_bgp(unittest.TestCase):

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
        bgp = Bgp(device=self.device)
        # Get outputs
        bgp.maker.outputs[ShowVrf] = {"{'vrf':'all'}":BgpOutput.ShowVrf}
        bgp.maker.outputs[ShowRoutingVrfAll] = {"{'vrf':'all'}":BgpOutput.ShowRoutingVrfAll}
        bgp.maker.outputs[ShowBgpProcessVrfAll] = {"{'vrf':'all'}":BgpOutput.ShowBgpProcessVrfAll}
        bgp.maker.outputs[ShowBgpPeerSession] = {'':BgpOutput.ShowBgpPeerSession}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'':BgpOutput.ShowBgpPeerPolicy}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'':BgpOutput.ShowBgpPeerTemplate}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {"{'address_family':'all','vrf':'all'}":BgpOutput.ShowBgpVrfAllAll}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] =\
            {"{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAllNextHopDatabase}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary]=\
            {"{'address_family':'all','vrf':'all'}":BgpOutput.ShowBgpVrfAllAllSummary}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] =\
            {"{'address_family':'all','vrf':'all'}":BgpOutput.ShowBgpVrfAllAllDampeningParameters}
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Verify Ops was created successfully
        self.assertDictEqual(bgp.info, BgpOutput.BgpOpsOutput_info)
        self.assertDictEqual(bgp.table, BgpOutput.BgpOpsOutput_table)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.BgpOpsOutput_routesperpeer)

    def test_custom_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        bgp.maker.outputs[ShowVrf] = {"{'vrf':'VRF1'}": BgpOutput.ShowVrf_vrf1}
        bgp.maker.outputs[ShowRoutingVrfAll] = {
            "{'vrf':'VRF1'}": BgpOutput.ShowRoutingVrfAll_vrf1}
        bgp.maker.outputs[ShowBgpProcessVrfAll] = {
            "{'vrf':'VRF1'}": BgpOutput.ShowBgpProcessVrfAll_vrf1}
        bgp.maker.outputs[ShowBgpPeerSession] = {'': BgpOutput.ShowBgpPeerSession}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'': BgpOutput.ShowBgpPeerPolicy}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'': BgpOutput.ShowBgpPeerTemplate}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {
            "{'address_family':'ipv4 unicast','vrf':'VRF1'}": BgpOutput.ShowBgpVrfAllAll_vrf1}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] = \
            {
                "{'address_family':'ipv4 unicast','vrf':'VRF1'}":
                    BgpOutput.ShowBgpVrfAllAllNextHopDatabase_vrf1}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary] = \
            {"{'address_family':'ipv4 unicast','vrf':'VRF1'}": BgpOutput.ShowBgpVrfAllAllSummary_vrf1}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] = \
            {
                "{'address_family':'ipv4 unicast','vrf':'VRF1'}":
                    BgpOutput.ShowBgpVrfAllAllDampeningParameters_vrf1}
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn(vrf='VRF1', address_family='ipv4 unicast', neighbor='10.16.2.10')

        # Verify Ops was created successfully
        self.assertDictEqual(bgp.info, BgpOutput.BgpOpsOutput_info_custom)
        self.assertDictEqual(bgp.table, BgpOutput.BgpOpsOutput_table_custom)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.BgpOpsOutput_routesperpeer_custom)

    def test_empty_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        outputs['show bgp process vrf all'] = ''

        bgp.maker.outputs[ShowVrf] = {"{'vrf':'all'}":''}
        bgp.maker.outputs[ShowRoutingVrfAll] = {"{'vrf':'all'}":''}
        bgp.maker.outputs[ShowBgpProcessVrfAll] = {"{'vrf':'all'}":''}
        bgp.maker.outputs[ShowBgpPeerSession] = {'':''}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'':''}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'':''}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {"{'address_family':'all','vrf':'all'}":''}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] = {"{'address_family':'all','vrf':'all'}":''}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary] = {"{'address_family':'all','vrf':'all'}":''}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] = {"{'address_family':'all','vrf':'all'}":''}
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
                ['VRF1']['address_family']['ipv4 unicast']['bgp_table_version'])
        # routes_per_peer - remote_as
        with self.assertRaises(AttributeError):
            remote_as = (bgp.routes_per_peer['instance']['default']['vrf']\
                ['VRF1']['neighbor']['10.16.2.10']['remote_as'])

        outputs['show bgp process vrf all'] = BgpOutput.ShowBgpProcessVrfAll_all


    def test_selective_attribute(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        bgp.maker.outputs[ShowVrf] = {"{'vrf':'all'}":BgpOutput.ShowVrf}
        bgp.maker.outputs[ShowRoutingVrfAll] = {"{'vrf':'all'}":BgpOutput.ShowRoutingVrfAll}
        bgp.maker.outputs[ShowBgpProcessVrfAll] = {"{'vrf':'all'}":BgpOutput.ShowBgpProcessVrfAll}
        bgp.maker.outputs[ShowBgpPeerSession] = {'':BgpOutput.ShowBgpPeerSession}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'':BgpOutput.ShowBgpPeerPolicy}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'':BgpOutput.ShowBgpPeerTemplate}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {"{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAll}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] = \
            {"{'address_family':'all','vrf':'all'}":
                    BgpOutput.ShowBgpVrfAllAllNextHopDatabase}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary] = \
            {"{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAllSummary}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] = \
            {"{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAllDampeningParameters}
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        
        # Learn the feature
        bgp.learn()

        # Check specific attribute values
        # info - bgp_id
        self.assertEqual(bgp.info['instance']['default']['bgp_id'], 100)
        # table - bgp_table_version
        self.assertEqual(bgp.table['instance']['default']['vrf']['VRF1']\
                ['address_family']['ipv4 unicast']['bgp_table_version'], 35)
        # routes_per_peer - remote_as
        self.assertEqual(bgp.routes_per_peer['instance']['default']['vrf']\
                ['VRF1']['neighbor']['10.16.2.10']['remote_as'], 0)


    def test_incomplete_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        bgp.maker.outputs[ShowVrf] = {'':BgpOutput.ShowVrf}
        bgp.maker.outputs[ShowRoutingVrfAll] = {'':BgpOutput.ShowRoutingVrfAll}
        bgp.maker.outputs[ShowBgpProcessVrfAll] = {'':BgpOutput.ShowBgpProcessVrfAll}
        bgp.maker.outputs[ShowBgpPeerSession] = {'':BgpOutput.ShowBgpPeerSession}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'':BgpOutput.ShowBgpPeerPolicy}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'':BgpOutput.ShowBgpPeerTemplate}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {'':BgpOutput.ShowBgpVrfAllAll}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] =\
            {'': BgpOutput.ShowBgpVrfAllAllNextHopDatabase}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary]=\
            {'':BgpOutput.ShowBgpVrfAllAllSummary}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] =\
            {'':BgpOutput.ShowBgpVrfAllAllDampeningParameters}
        # Outputs from side_effect set to empty
        bgp.maker.outputs[ShowBgpVrfAllNeighbors] = {'':''}
        bgp.maker.outputs[ShowBgpVrfAllNeighborsAdvertisedRoutes] = {'':''}
        bgp.maker.outputs[ShowBgpVrfAllNeighborsRoutes] = {'':''}
        bgp.maker.outputs[ShowBgpVrfAllNeighborsReceivedRoutes] = {'':''}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = ['', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '']

        # Learn the feature
        bgp.learn()

if __name__ == '__main__':
    unittest.main()
