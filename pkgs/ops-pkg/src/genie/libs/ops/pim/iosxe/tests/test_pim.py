# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.pim.iosxe.pim import Pim
from genie.libs.ops.pim.iosxe.tests.pim_output import PimOutput

# Parser
from genie.libs.parser.iosxe.show_pim import ShowIpv6PimInterface,\
                                  ShowIpPimInterfaceDetail,\
                                  ShowIpPimInterface, \
                                  ShowIpv6PimBsrCandidateRp, \
                                  ShowIpPimRpMapping, \
                                  ShowIpv6PimBsrElection, \
                                  ShowIpPimBsrRouter, \
                                  ShowIpPimNeighbor, \
                                  ShowIpv6PimNeighborDetail, \
                                  ShowIpPimInterfaceDf

from genie.libs.parser.iosxe.show_mcast import ShowIpMroute,\
                                    ShowIpv6Mroute

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class test_pim(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        pim = Pim(device=self.device)
        
        # Get outputs
        pim.maker.outputs[ShowVrfDetail] = \
            {'': PimOutput.ShowVrfDetail}

        pim.maker.outputs[ShowIpv6PimInterface] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimInterface_default}

        pim.maker.outputs[ShowIpv6PimInterface].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6PimInterface_VRF1})

        pim.maker.outputs[ShowIpPimInterface] = \
            {"{'vrf':''}": PimOutput.ShowIpPimInterface_default}

        pim.maker.outputs[ShowIpPimInterface].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimInterface_VRF1})

        pim.maker.outputs[ShowIpv6PimBsrElection] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimBsrElection_default}

        pim.maker.outputs[ShowIpv6PimBsrElection].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6PimBsrElection_VRF1})

        pim.maker.outputs[ShowIpv6PimBsrCandidateRp] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimBsrCandidateRp_default}

        pim.maker.outputs[ShowIpv6PimBsrCandidateRp].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6PimBsrCandidateRp_VRF1})           

        pim.maker.outputs[ShowIpPimBsrRouter] = \
            {"{'vrf':''}": PimOutput.ShowIpPimBsrRouter_default}

        pim.maker.outputs[ShowIpPimBsrRouter].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimBsrRouter_VRF1})

        pim.maker.outputs[ShowIpPimRpMapping] = \
            {"{'vrf':''}": PimOutput.ShowIpPimRpMapping_default}

        pim.maker.outputs[ShowIpPimRpMapping].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimRpMapping_VRF1})

        pim.maker.outputs[ShowIpPimInterfaceDetail] = \
            {"{'vrf':''}": PimOutput.ShowIpPimInterfaceDetail_default}

        pim.maker.outputs[ShowIpPimInterfaceDetail].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimInterfaceDetail_VRF1})

        pim.maker.outputs[ShowIpMroute] = \
            {"{'vrf':''}": PimOutput.ShowIpMroute_default}

        pim.maker.outputs[ShowIpMroute].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpMroute_VRF1})

        pim.maker.outputs[ShowIpv6Mroute] = \
            {"{'vrf':''}": PimOutput.ShowIpv6Mroute_default}

        pim.maker.outputs[ShowIpv6Mroute].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6Mroute_VRF1})

        pim.maker.outputs[ShowIpPimNeighbor] = \
            {"{'vrf':''}": PimOutput.ShowIpPimNeighbor_default}

        pim.maker.outputs[ShowIpPimNeighbor].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimNeighbor_VRF1})

        pim.maker.outputs[ShowIpv6PimNeighborDetail] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimNeighborDetail_default}

        pim.maker.outputs[ShowIpv6PimNeighborDetail].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6PimNeighborDetail_VRF1})

        pim.maker.outputs[ShowIpPimInterfaceDf] = \
            {"{'vrf':''}": PimOutput.ShowIpPimInterfaceDf_default}

        pim.maker.outputs[ShowIpPimInterfaceDf].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimInterfaceDf_VRF1})

        # Learn the feature
        pim.learn()

        # Verify Ops was created successfully
        self.assertEqual(pim.info, PimOutput.Pim_info)

        # Verify Select Attributes 
        # Check specific attribute values
        # info - default vrf
        self.assertEqual(pim.info['vrf']['default']['address_family']\
                                 ['ipv4']['rp']['bsr']\
                                 ['Loopback0']['address'], '10.16.2.2')
        # info - vrf VRF1
        self.assertEqual(pim.info['vrf']['VRF1']['interfaces']\
                                  ['GigabitEthernet3']['address_family']['ipv4']\
                                  ['bsr_border'], False)


    def test_empty_output(self):
        self.maxDiff = None
        pim = Pim(device=self.device)
        # Get outputs
        pim.maker.outputs[ShowVrfDetail] = \
            {'': PimOutput.ShowVrfDetail}

        pim.maker.outputs[ShowIpv6PimInterface] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpv6PimInterface].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpPimInterface] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpPimInterface].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpv6PimBsrElection] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpv6PimBsrElection].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpv6PimBsrCandidateRp] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpv6PimBsrCandidateRp].update(
            {"{'vrf':'VRF1'}": {}})           

        pim.maker.outputs[ShowIpPimBsrRouter] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpPimBsrRouter].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpPimRpMapping] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpPimRpMapping].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpPimInterfaceDetail] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpPimInterfaceDetail].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpMroute] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpMroute].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpv6Mroute] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpv6Mroute].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpPimNeighbor] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpPimNeighbor].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpv6PimNeighborDetail] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpv6PimNeighborDetail].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpPimInterfaceDf] = \
            {"{'vrf':''}": {}}

        pim.maker.outputs[ShowIpPimInterfaceDf].update(
            {"{'vrf':'VRF1'}": {}})

        # Learn the feature
        pim.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            pim.info['vrf']

    def test_incomplete_output(self):
        self.maxDiff = None
        
        pim = Pim(device=self.device)

        # Get outputs
        pim.maker.outputs[ShowVrfDetail] = \
            {'': PimOutput.ShowVrfDetail}

        pim.maker.outputs[ShowIpv6PimInterface] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimInterface_default}

        pim.maker.outputs[ShowIpv6PimInterface].update(
            {"{'vrf':'VRF1'}": {}})

        pim.maker.outputs[ShowIpPimInterface] = \
            {"{'vrf':''}": PimOutput.ShowIpPimInterface_default}

        pim.maker.outputs[ShowIpPimInterface].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimInterface_VRF1})

        pim.maker.outputs[ShowIpv6PimBsrElection] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimBsrElection_default}

        pim.maker.outputs[ShowIpv6PimBsrElection].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6PimBsrElection_VRF1})

        pim.maker.outputs[ShowIpv6PimBsrCandidateRp] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimBsrCandidateRp_default}

        pim.maker.outputs[ShowIpv6PimBsrCandidateRp].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6PimBsrCandidateRp_VRF1})           

        pim.maker.outputs[ShowIpPimBsrRouter] = \
            {"{'vrf':''}": PimOutput.ShowIpPimBsrRouter_default}

        pim.maker.outputs[ShowIpPimBsrRouter].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimBsrRouter_VRF1})

        pim.maker.outputs[ShowIpPimRpMapping] = \
            {"{'vrf':''}": PimOutput.ShowIpPimRpMapping_default}

        pim.maker.outputs[ShowIpPimRpMapping].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimRpMapping_VRF1})

        pim.maker.outputs[ShowIpPimInterfaceDetail] = \
            {"{'vrf':''}": PimOutput.ShowIpPimInterfaceDetail_default}

        pim.maker.outputs[ShowIpPimInterfaceDetail].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimInterfaceDetail_VRF1})

        pim.maker.outputs[ShowIpMroute] = \
            {"{'vrf':''}": PimOutput.ShowIpMroute_default}

        pim.maker.outputs[ShowIpMroute].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpMroute_VRF1})

        pim.maker.outputs[ShowIpv6Mroute] = \
            {"{'vrf':''}": PimOutput.ShowIpv6Mroute_default}

        pim.maker.outputs[ShowIpv6Mroute].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6Mroute_VRF1})

        pim.maker.outputs[ShowIpPimNeighbor] = \
            {"{'vrf':''}": PimOutput.ShowIpPimNeighbor_default}

        pim.maker.outputs[ShowIpPimNeighbor].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimNeighbor_VRF1})

        pim.maker.outputs[ShowIpv6PimNeighborDetail] = \
            {"{'vrf':''}": PimOutput.ShowIpv6PimNeighborDetail_default}

        pim.maker.outputs[ShowIpv6PimNeighborDetail].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpv6PimNeighborDetail_VRF1})

        pim.maker.outputs[ShowIpPimInterfaceDf] = \
            {"{'vrf':''}": PimOutput.ShowIpPimInterfaceDf_default}

        pim.maker.outputs[ShowIpPimInterfaceDf].update(
            {"{'vrf':'VRF1'}": PimOutput.ShowIpPimInterfaceDf_VRF1})

        # Learn the feature
        pim.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(PimOutput.Pim_info)
        del(expect_dict['vrf']['VRF1']['interfaces']['Loopback1'])
        del(expect_dict['vrf']['VRF1']['interfaces']['Tunnel6'])
        del(expect_dict['vrf']['VRF1']['interfaces']['Tunnel5'])
        del(expect_dict['vrf']['VRF1']['interfaces']['Tunnel7'])
        del(expect_dict['vrf']['VRF1']['interfaces']['GigabitEthernet3']['address_family']['ipv6'])

                
        # Verify Ops was created successfully
        self.assertEqual(pim.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
