# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.bgp.iosxr.bgp import Bgp
from genie.libs.ops.bgp.iosxr.tests.bgp_output import BgpOutput

# Parser
from genie.libs.parser.iosxr.show_bgp import ShowPlacementProgramAll,\
                                  ShowBgpInstanceAfGroupConfiguration,\
                                  ShowBgpInstanceSessionGroupConfiguration,\
                                  ShowBgpInstanceProcessDetail,\
                                  ShowBgpInstanceNeighborsDetail,\
                                  ShowBgpInstanceNeighborsAdvertisedRoutes,\
                                  ShowBgpInstanceNeighborsReceivedRoutes,\
                                  ShowBgpInstanceNeighborsRoutes,\
                                  ShowBgpInstanceSummary,\
                                  ShowBgpInstanceAllAll, ShowBgpInstances

outputs = {}
# info
outputs['show bgp instance all all all process detail'] = BgpOutput.ProcessAllOutput
outputs['show bgp instance default all all process detail'] = BgpOutput.ProcessAllOutput
outputs['show bgp instance default vrf VRF1 ipv4 unicast process detail'] = BgpOutput.ProcessVrf1Ipv4Output
outputs['show bgp instance all vrf all process detail'] = BgpOutput.ProcessVrfOutput
outputs['show bgp instance all vrf all ipv4 unicast process detail'] = BgpOutput.ProcessIpv4Output
outputs['show bgp instance all vrf all ipv6 unicast process detail'] = BgpOutput.ProcessIpv6Output
# table
outputs['show bgp instance all all all'] = BgpOutput.InstanceAllOutput
outputs['show bgp instance all vrf all'] = BgpOutput.InstanceVrfOutput
outputs['show bgp instance default vrf VRF1 ipv4 unicast'] = BgpOutput.InstanceVrf1Ipv4Output
outputs['show bgp instance all vrf all ipv4 unicast'] = BgpOutput.InstanceIpv4Output
outputs['show bgp instance all vrf all ipv6 unicast'] = BgpOutput.InstanceIpv6Output
outputs['show bgp instance all all all summary'] = BgpOutput.SummaryAllOutput
outputs['show bgp instance all vrf all summary'] = BgpOutput.SummaryVrfOutput
outputs['show bgp instance default vrf VRF1 ipv4 unicast summary'] = BgpOutput.SummaryIpv4Output
outputs['show bgp instance all vrf all ipv4 unicast summary'] = BgpOutput.SummaryIpv4Output
outputs['show bgp instance all vrf all ipv6 unicast summary'] = BgpOutput.SummaryIpv6Output
# routes_per_peer
outputs['show bgp instance all all all neighbors detail'] = BgpOutput.NeighborsAllOutput_Simple
outputs['show bgp instance all vrf all neighbors  detail'] = BgpOutput.NeighborsVrfOutput
outputs['show bgp instance all all all neighbors 10.16.2.2 advertised-routes'] = BgpOutput.AdvertisedAllOutput
outputs['show bgp instance all all all neighbors 10.16.2.2 received routes'] = BgpOutput.ReceivedAllOutput
outputs['show bgp instance all all all neighbors 10.16.2.2 routes'] = BgpOutput.RoutesAllOutput
outputs['show bgp instance all vrf all ipv4 unicast neighbors detail'] = BgpOutput.NeighborsIpv4Output_Simple
outputs['show bgp instance default vrf VRF1 ipv4 unicast neighbors 10.1.5.5 detail'] = BgpOutput.NeighborsIpv4Output_Simple
outputs['show bgp instance all vrf all ipv4 unicast neighbors 10.1.5.5 advertised-routes'] = BgpOutput.AdvertisedIpv4Output
outputs['show bgp instance default vrf VRF1 ipv4 unicast neighbors 10.1.5.5 advertised-routes'] = BgpOutput.AdvertisedIpv4Output
outputs['show bgp instance all vrf all ipv4 unicast neighbors 10.1.5.5 received routes'] = BgpOutput.ReceivedIpv4Output
outputs['show bgp instance default vrf VRF1 ipv4 unicast neighbors 10.1.5.5 received routes'] = BgpOutput.ReceivedIpv4Output
outputs['show bgp instance all vrf all ipv4 unicast neighbors 10.1.5.5 routes'] = BgpOutput.RoutesIpv4Output
outputs['show bgp instance default vrf VRF1 ipv4 unicast neighbors 10.1.5.5 routes'] = BgpOutput.RoutesIpv4Output
outputs['show bgp instance all vrf all ipv6 unicast neighbors detail'] = BgpOutput.NeighborsIpv6Output_Simple
outputs['show bgp instance all vrf all ipv6 unicast neighbors 2001:db8:20:1:5::5 advertised-routes'] = BgpOutput.AdvertisedIpv6Output
outputs['show bgp instance all vrf all ipv6 unicast neighbors 2001:db8:20:1:5::5 received routes'] = BgpOutput.ReceivedIpv6Output
outputs['show bgp instance all vrf all ipv6 unicast neighbors 2001:db8:20:1:5::5 routes'] = BgpOutput.RoutesIpv6Output


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
        # Set outputs
        bgp.maker.outputs[ShowBgpInstances] = {'':BgpOutput.ShowBgpInstances}
        bgp.maker.outputs[ShowPlacementProgramAll] = {'':BgpOutput.ShowPlacementProgramAll}
        bgp.maker.outputs[ShowBgpInstanceAfGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceAfGroupConfiguration}
        bgp.maker.outputs[ShowBgpInstanceSessionGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceSessionGroupConfiguration}
        
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Verify Ops was created successfully
        self.assertDictEqual(bgp.info, BgpOutput.BgpInfo)
        self.assertDictEqual(bgp.table, BgpOutput.BgpTable)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.BgpRoutesPerPeer)

    def test_custom_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Set outputs
        bgp.maker.outputs[ShowBgpInstances] = {'': BgpOutput.ShowBgpInstances_custom}
        bgp.maker.outputs[ShowPlacementProgramAll] = {
            '': BgpOutput.ShowPlacementProgramAll}
        bgp.maker.outputs[ShowBgpInstanceAfGroupConfiguration] = {
            '': BgpOutput.ShowBgpInstanceAfGroupConfiguration}
        bgp.maker.outputs[ShowBgpInstanceSessionGroupConfiguration] = {
            '': BgpOutput.ShowBgpInstanceSessionGroupConfiguration}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        bgp.learn(vrf='VRF1', address_family='ipv4 unicast', neighbor='10.1.5.5', instance='default')

        # Verify Ops was created successfully
        self.assertDictEqual(bgp.info, BgpOutput.BgpInfo_custom)
        self.assertDictEqual(bgp.table, BgpOutput.BgpTable_custom)
        self.assertDictEqual(bgp.routes_per_peer, BgpOutput.BgpRoutesPerPeer_custom)

    def test_selective_attribute(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        # Set outputs
        bgp.maker.outputs[ShowBgpInstances] = {'':BgpOutput.ShowBgpInstances}
        bgp.maker.outputs[ShowPlacementProgramAll] = {'':BgpOutput.ShowPlacementProgramAll}
        bgp.maker.outputs[ShowBgpInstanceAfGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceAfGroupConfiguration}
        bgp.maker.outputs[ShowBgpInstanceSessionGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceSessionGroupConfiguration}
        
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper


        # Learn the feature
        bgp.learn()

        # Check specific attribute values
        # bgp.info - bgp_id
        self.assertEqual(bgp.info['instance']['default']['bgp_id'], 100)
        
        # bgp.table - bgp_table_version
        self.assertEqual(bgp.table['instance']['default']['vrf']['VRF1']\
                ['address_family']['vpnv4 unicast']['bgp_table_version'], 47)
        
        # bgp.routes_per_peer - remote_as
        self.assertEqual(bgp.routes_per_peer['instance']['default']['vrf']\
                ['default']['neighbor']['10.16.2.2']['remote_as'], 100)


    def test_empty_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        
        # Set outputs
        bgp.maker.outputs[ShowBgpInstances] = {'':''}
        bgp.maker.outputs[ShowPlacementProgramAll] = {'':''}
        bgp.maker.outputs[ShowBgpInstanceAfGroupConfiguration] = {'':''}
        bgp.maker.outputs[ShowBgpInstanceSessionGroupConfiguration] = {'':''}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = ['', '', '', '', '', '', '', '',
                                           '', '', '', '', '', '', '', '',
                                           '', '', '', '', '', '', '', '']

        # Learn the feature
        bgp.learn()

        # Check no attribute not found
        
        # bgp.info - bgp_id
        with self.assertRaises(AttributeError):
            bgp_id = (bgp.info['instance']['default']['bgp_id'])
        
        # bgp.table - bgp_table_version
        with self.assertRaises(AttributeError):
            bgp_table_version = (bgp.table['instance']['default']['vrf']\
                ['VRF1']['address_family']['vpnv4 unicast']['bgp_table_version'])
        
        # bgp.routes_per_peer - remote_as
        with self.assertRaises(AttributeError):
            remote_as = (bgp.routes_per_peer['instance']['default']['vrf']\
                ['default']['neighbor']['10.16.2.2']['remote_as'])


    def test_incomplete_output(self):
        self.maxDiff = None
        bgp = Bgp(device=self.device)
        
        # Set outputs
        bgp.maker.outputs[ShowBgpInstances] = {'':BgpOutput.ShowBgpInstances}
        bgp.maker.outputs[ShowPlacementProgramAll] = {'':BgpOutput.ShowPlacementProgramAll}
        bgp.maker.outputs[ShowBgpInstanceAfGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceAfGroupConfiguration}
        bgp.maker.outputs[ShowBgpInstanceSessionGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceSessionGroupConfiguration}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = ['', '', '', '', '', '', '', '',
                                           '', '', '', '', '', '', '', '',
                                           '', '', '', '', '', '', '', '']

        # Learn the feature
        bgp.learn()

        # Check attribute values of output provided is found
        
        # bgp.info - protocol_state
        self.assertEqual(bgp.info['instance']['default']['protocol_state'], 'RUNNING')


if __name__ == '__main__':
    unittest.main()
