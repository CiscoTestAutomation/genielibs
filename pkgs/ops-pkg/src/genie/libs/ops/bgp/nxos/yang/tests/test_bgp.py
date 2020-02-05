# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie YANG Ops for BGP
from genie.libs.ops.bgp.nxos.yang.bgp import Bgp
from genie.libs.ops.bgp.nxos.yang.tests.bgp_output import BgpOutput

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
outputs['show bgp vrf default all neighbors'] = BgpOutput.vrf_default_output
outputs['show bgp vrf VRF1 all neighbors 10.16.2.10 advertised-routes'] = BgpOutput.nbr1_advertised_routes
outputs['show bgp vrf VRF1 all neighbors 10.16.2.10 routes'] = BgpOutput.nbr1_routes
outputs['show bgp vrf VRF1 all neighbors 10.16.2.10 received-routes'] = BgpOutput.nbr1_received_routes
outputs['show bgp vrf default all neighbors 10.16.2.2 advertised-routes'] = BgpOutput.nbr2_advertised_routes
outputs['show bgp vrf default all neighbors 10.16.2.2 routes'] = BgpOutput.nbr2_routes
outputs['show bgp vrf default all neighbors 10.16.2.2 received-routes'] = BgpOutput.nbr2_received_routes
# YANG command output
outputs['yang_output'] = BgpOutput.yang_output
outputs['show bgp process vrf all'] = BgpOutput.bgp_process_output

def mapper(key):
    if 'subtree' in key:
        key = 'yang_output'
    return outputs[key]


class test_bgp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.mapping['yang']='yang'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device
        self.device.connectionmgr.connections['yang'] = self.device

        # Set context to YANG
        self.device.context = 'yang'

    def test_complete_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        bgp.maker.outputs[ShowVrf] = {"{'vrf':'all'}": BgpOutput.ShowVrf}
        bgp.maker.outputs[ShowRoutingVrfAll] = {
            "{'vrf':'all'}": BgpOutput.ShowRoutingVrfAll}
        bgp.maker.outputs[ShowBgpPeerSession] = {'': BgpOutput.ShowBgpPeerSession}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'': BgpOutput.ShowBgpPeerPolicy}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'': BgpOutput.ShowBgpPeerTemplate}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {
            "{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAll}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] = \
            {"{'address_family':'all','vrf':'all'}":
                 BgpOutput.ShowBgpVrfAllAllNextHopDatabase}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary] = \
            {"{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAllSummary}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] = \
            {
                "{'address_family':'all','vrf':'all'}":
                    BgpOutput.ShowBgpVrfAllAllDampeningParameters}
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.get = Mock()
        self.device.execute.side_effect = mapper
        self.device.get.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Verify Ops was created successfully
        self.assertDictEqual(bgp.info, BgpOutput.BgpOpsOutput_info)
        self.assertEqual(bgp.table, BgpOutput.BgpOpsOutput_table)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.BgpOpsOutput_routesperpeer)

    def test_empty_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        bgp.maker.outputs[ShowVrf] = {"{'vrf':'all'}": ''}
        bgp.maker.outputs[ShowRoutingVrfAll] = {"{'vrf':'all'}": ''}
        bgp.maker.outputs[ShowBgpProcessVrfAll] = {"{'vrf':'all'}":''}
        bgp.maker.outputs[ShowBgpPeerSession] = {'': ''}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'': ''}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'': ''}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {"{'address_family':'all','vrf':'all'}": ''}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] = {
            "{'address_family':'all','vrf':'all'}": ''}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary] = {
            "{'address_family':'all','vrf':'all'}": ''}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] = {
            "{'address_family':'all','vrf':'all'}": ''}

        self.device.execute = Mock()
        self.device.get = Mock()
        self.device.execute.side_effect = mapper
        self.device.get.side_effect = mapper

        # Learn the feature
        bgp.learn()
        # outputs['show bgp process vrf all'] = BgpOutput.bgp_process_output
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


    def test_selective_attribute(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        bgp.maker.outputs[ShowVrf] = {"{'vrf':'all'}": BgpOutput.ShowVrf}
        bgp.maker.outputs[ShowRoutingVrfAll] = {
            "{'vrf':'all'}": BgpOutput.ShowRoutingVrfAll}
        bgp.maker.outputs[ShowBgpPeerSession] = {'': BgpOutput.ShowBgpPeerSession}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'': BgpOutput.ShowBgpPeerPolicy}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'': BgpOutput.ShowBgpPeerTemplate}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {
            "{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAll}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] = \
            {"{'address_family':'all','vrf':'all'}":
                 BgpOutput.ShowBgpVrfAllAllNextHopDatabase}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary] = \
            {"{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAllSummary}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] = \
            {
                "{'address_family':'all','vrf':'all'}":
                    BgpOutput.ShowBgpVrfAllAllDampeningParameters}
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.get = Mock()
        self.device.execute.side_effect = mapper
        self.device.get.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Check specific attribute values
        self.assertEqual(bgp.info['instance']['default']['bgp_id'], 100)
        self.assertEqual(bgp.table['instance']['default']['vrf']['VRF1']\
                ['address_family']['ipv4 unicast']['bgp_table_version'], 35)
        self.assertEqual(bgp.routes_per_peer['instance']['default']['vrf']\
                ['default']['neighbor']['10.16.2.2']['remote_as'], 100)

    def test_incomplete_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Get outputs
        bgp.maker.outputs[ShowVrf] = {"{'vrf':'all'}": BgpOutput.ShowVrf}
        bgp.maker.outputs[ShowRoutingVrfAll] = {
            "{'vrf':'all'}": BgpOutput.ShowRoutingVrfAll}
        bgp.maker.outputs[ShowBgpVrfAllAll] = {
            "{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAll}
        bgp.maker.outputs[ShowBgpVrfAllAllNextHopDatabase] = \
            {"{'address_family':'all','vrf':'all'}":
                 BgpOutput.ShowBgpVrfAllAllNextHopDatabase}
        bgp.maker.outputs[ShowBgpVrfAllAllSummary] = \
            {"{'address_family':'all','vrf':'all'}": BgpOutput.ShowBgpVrfAllAllSummary}
        bgp.maker.outputs[ShowBgpVrfAllAllDampeningParameters] = \
            {
                "{'address_family':'all','vrf':'all'}":
                    BgpOutput.ShowBgpVrfAllAllDampeningParameters}

        # Set empty outputs
        bgp.maker.outputs[ShowBgpPeerSession] = {'':''}
        bgp.maker.outputs[ShowBgpPeerPolicy] = {'':''}
        bgp.maker.outputs[ShowBgpPeerTemplate] = {'':''}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.get = Mock()
        self.device.execute.side_effect = mapper
        self.device.get.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Verify attributes are not learnt in ops
        self.assertTrue('peer_policy' not in bgp.info['instance']['default'])
        self.assertTrue('peer_session' not in bgp.info['instance']['default'])

if __name__ == '__main__':
    unittest.main()
