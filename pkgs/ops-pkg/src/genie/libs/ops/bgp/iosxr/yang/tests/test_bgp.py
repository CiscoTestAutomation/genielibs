# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie YANG Ops for BGP
from genie.libs.ops.bgp.iosxr.yang.bgp import Bgp
from genie.libs.ops.bgp.iosxr.yang.tests.bgp_output import BgpOutput

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
outputs['show bgp instance all all all '] = BgpOutput.InstanceAllOutput
outputs['show bgp instance all vrf all ipv6 unicast'] = BgpOutput.InstanceIpv6Output
outputs['show bgp instance all vrf all ipv4 unicast'] = BgpOutput.InstanceIpv4Output
outputs['show bgp instance all all all  summary'] = BgpOutput.SummaryAllOutput
outputs['show bgp instance all vrf all ipv4 unicast summary'] = BgpOutput.SummaryIpv4Output
outputs['show bgp instance all vrf all ipv6 unicast summary'] = BgpOutput.SummaryIpv6Output
outputs['show bgp instance all all all  neighbors 10.16.2.2 advertised-routes'] = BgpOutput.AdvertisedAllOutput
outputs['show bgp instance all all all  neighbors 10.16.2.2 received routes'] = BgpOutput.ReceivedAllOutput
outputs['show bgp instance all all all  neighbors 10.16.2.2 routes'] = BgpOutput.RoutesAllOutput
outputs['show bgp instance all vrf all ipv4 unicast neighbors 10.16.2.2 advertised-routes'] = ''
outputs['show bgp instance all vrf all ipv4 unicast neighbors 10.16.2.2 received routes'] = ''
outputs['show bgp instance all vrf all ipv4 unicast neighbors 10.16.2.2 routes'] = ''
outputs['show bgp instance all vrf all ipv6 unicast neighbors 10.16.2.2 advertised-routes'] = ''
outputs['show bgp instance all vrf all ipv6 unicast neighbors 10.16.2.2 received routes'] = ''
outputs['show bgp instance all vrf all ipv6 unicast neighbors 10.16.2.2 routes'] = ''
# YANG command output
outputs['yang_output'] = BgpOutput.yang_output


def mapper(key):
    if 'subtree' in key:
        key = 'yang_output'
    return outputs[key]


class test_bgp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
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
        # Set outputs
        bgp.maker.outputs[ShowBgpInstances] = {'':BgpOutput.ShowBgpInstances}
        bgp.maker.outputs[ShowPlacementProgramAll] = {'':BgpOutput.ShowPlacementProgramAll}
        bgp.maker.outputs[ShowBgpInstanceAfGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceAfGroupConfiguration}
        bgp.maker.outputs[ShowBgpInstanceSessionGroupConfiguration] = {'':BgpOutput.ShowBgpInstanceSessionGroupConfiguration}
        
        # Return outputs above as inputs to parser when called
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.get = Mock()
        self.device.execute.side_effect = mapper
        self.device.get.side_effect = mapper

        # Learn the feature
        bgp.learn()

        # Verify Ops was created successfully
        self.assertEqual(bgp.info, BgpOutput.BgpInfo)
        self.assertEqual(bgp.table, BgpOutput.BgpTable)
        self.assertEqual(bgp.routes_per_peer, BgpOutput.BgpRoutesPerPeer)


if __name__ == '__main__':
    unittest.main()
