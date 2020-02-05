# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.mcast.iosxe.mcast import Mcast
from genie.libs.ops.mcast.iosxe.tests.mcast_output import McastOutput

# iosxe show_mcast
from genie.libs.parser.iosxe.show_mcast import ShowIpMroute, ShowIpv6Mroute,\
                                   ShowIpMrouteStatic, ShowIpMulticast
# iosxe show_rpf
from genie.libs.parser.iosxe.show_rpf import ShowIpRpf, ShowIpv6Rpf

# iosxe show_pim
from genie.libs.parser.iosxe.show_pim import ShowIpv6PimInterface

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

outputs = {}
outputs['show ip multicast vrf VRF1'] = McastOutput.ShowIpMulticast_vrf1_output
outputs['show ipv6 pim vrf VRF1 interface'] = McastOutput.ShowIpv6PimInterface_vrf1_output
outputs['show ip mroute vrf VRF1 static'] = McastOutput.ShowIpMrouteStatic_vrf1_output
outputs['show ip mroute vrf VRF1'] = McastOutput.ShowIpMroute_vrf1_output
outputs['show ipv6 mroute vrf VRF1'] = McastOutput.ShowIpv6Mroute_vrf1_output
outputs['show ipv6 rpf vrf VRF1 FF07::1'] = McastOutput.ShowIpv6Rpf_vrf1_output
outputs['show ip multicast'] = McastOutput.ShowIpMulticast_default_output
outputs['show ipv6 pim interface'] = McastOutput.ShowIpv6PimInterface_default_output
outputs['show ip mroute static'] = McastOutput.ShowIpMrouteStatic_default_output
outputs['show ip mroute'] = McastOutput.ShowIpMroute_default_output
outputs['show ipv6 mroute'] = McastOutput.ShowIpv6Mroute_default_output
outputs['show ipv6 rpf FF07::1'] = McastOutput.ShowIpv6Rpf_default_output

def mapper(key):
    return outputs[key]


class test_mcast(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device


    def test_complete_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowVrfDetail] = {'':McastOutput.ShowVrfDetail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mcast.learn()
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertEqual(mcast.info, McastOutput.McastInfo)
        self.assertEqual(mcast.table, McastOutput.McastTable)


    def test_selective_attribute(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowVrfDetail] = {'':McastOutput.ShowVrfDetail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mcast.learn()

        # Test specific attributes in info
        self.assertEqual(mcast.info['vrf']['default']['address_family']['ipv4']\
                ['mroute']['172.16.0.0/16']['path']['172.30.10.13 1']\
                ['neighbor_address'], '172.30.10.13')

        # Test specific attribute in table
        self.assertEqual(mcast.table['vrf']['VRF1']['address_family']\
                ['ipv6']['multicast_group']['FF07::1']\
                ['source_address']['2001:DB8:999::99']['flags'], 'SFT')


    def test_empty_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowVrfDetail] = {'':McastOutput.ShowVrfDetail}
        self.device.execute = Mock()
        self.device.execute.side_effect = ['','','','','','','','','','','','']

        # Learn the feature
        mcast.learn()

        # Check no outputs in mcast.info
        with self.assertRaises(AttributeError):
            neighbor_address = mcast.info['vrf']['default']['address_family']['ipv4']\
                ['mroute']['172.16.0.0/16']['path']['172.30.10.13 1']\
                ['neighbor_address']

        # Check no outputs in mcast.table
        with self.assertRaises(AttributeError):
            flags = mcast.table['vrf']['VRF1']['address_family']\
                ['ipv6']['multicast_group']['FF07::1']\
                ['source_address']['2001:DB8:999::99']['flags']


    def test_incomplete_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowVrfDetail] = {'':McastOutput.ShowVrfDetail}

        self.device.execute = Mock()
        outputs['show ip multicast'] = ''

        self.device.execute.side_effect = mapper

        # Learn the feature
        mcast.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(McastOutput.McastInfo)
        del(expect_dict['vrf']['default']['address_family']['ipv4']['enable'])
        del(expect_dict['vrf']['default']['address_family']['ipv4']['multipath'])
                
        # Verify Ops was created successfully
        self.assertEqual(mcast.info, expect_dict)
        self.assertEqual(mcast.table, McastOutput.McastTable)


if __name__ == '__main__':
    unittest.main()
