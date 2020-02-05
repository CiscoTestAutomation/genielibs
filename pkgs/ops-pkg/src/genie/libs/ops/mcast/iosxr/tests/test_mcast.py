# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.mcast.iosxr.mcast import Mcast
from genie.libs.ops.mcast.iosxr.tests.mcast_output import McastOutput

# iosxr show_pim
from genie.libs.parser.iosxr.show_pim import ShowPimVrfMstatic, ShowPimVrfRpfSummary,\
                                  ShowPimVrfInterfaceDetail

# iosxr show_mrib
from genie.libs.parser.iosxr.show_mrib import ShowMribVrfRoute

# iosxr show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail

outputs = {}
outputs['show pim vrf VRF1 ipv4 interface detail'] = McastOutput.PimVrfVRF1Ipv4InterfaceDetail
outputs['show pim vrf VRF1 ipv4 rpf summary'] = McastOutput.PimVrfVRF1Ipv4RpfSummary
outputs['show pim vrf VRF1 ipv4 mstatic'] = McastOutput.PimVrfVRF1Ipv4Mstatic
outputs['show mrib vrf VRF1 ipv4 route'] = McastOutput.MribVrfVRF1Ipv4Route
outputs['show pim vrf VRF1 ipv6 interface detail'] = McastOutput.PimVrfVRF1Ipv6InterfaceDetail
outputs['show pim vrf VRF1 ipv6 rpf summary'] = McastOutput.PimVrfVRF1Ipv6RpfSummary
outputs['show pim vrf VRF1 ipv6 mstatic'] = McastOutput.PimVrfVRF1Ipv6Mstatic
outputs['show mrib vrf VRF1 ipv6 route'] = McastOutput.MribVrfVRF1Ipv6Route
outputs['show pim vrf default ipv4 interface detail'] = McastOutput.PimVrfDefaultIpv4InterfaceDetail
outputs['show pim vrf default ipv4 rpf summary'] = McastOutput.PimVrfDefaultIpv4RpfSummary
outputs['show pim vrf default ipv4 mstatic'] = McastOutput.PimVrfDefaultIpv4Mstatic
outputs['show mrib vrf default ipv4 route'] = McastOutput.MribVrfDefaultIpv4Route
outputs['show pim vrf default ipv6 interface detail'] = McastOutput.PimVrfDefaultIpv6InterfaceDetail
outputs['show pim vrf default ipv6 rpf summary'] = McastOutput.PimVrfDefaultIpv6RpfSummary
outputs['show pim vrf default ipv6 mstatic'] = McastOutput.PimVrfDefaultIpv6Mstatic
outputs['show mrib vrf default ipv6 route'] = McastOutput.MribVrfDefaultIpv6Route

def mapper(key):
    return outputs[key]


class test_mcast(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device
        self.maxDiff = None

    def test_complete_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowVrfAllDetail] = {'':McastOutput.ShowVrfAllDetail}
        
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mcast.learn()

        # Verify Ops was created successfully
        self.assertEqual(mcast.info, McastOutput.McastInfo)
        self.assertEqual(mcast.table, McastOutput.McastTable)


    def test_selective_attribute(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowVrfAllDetail] = {'':McastOutput.ShowVrfAllDetail}
        
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mcast.learn()

        # Test specific attributes in info
        self.assertEqual(mcast.info['vrf']['VRF1']['address_family']['ipv4']\
            ['mroute']['10.135.10.10/32']['path']\
            ['192.168.1.0 GigabitEthernet1/0/0/0 10']['admin_distance'], 10)

        # Test specific attribute in table
        self.assertEqual(mcast.table['vrf']['default']['address_family']\
            ['ipv4']['multicast_group']['224.0.0.0/24']\
            ['source_address']['*']['flags'], 'D P')


    def test_empty_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowVrfAllDetail] = {'':McastOutput.ShowVrfAllDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = ['', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '', '', '', '', '',\
                                           '', '', '', '', '']

        # Learn the feature
        mcast.learn()

        # Check no outputs in mcast.info
        with self.assertRaises(AttributeError):
            admin_distance = mcast.info['vrf']['VRF1']['address_family']\
                ['ipv4']['mroute']['10.135.10.10/32']['path']\
                ['192.168.1.0 GigabitEthernet1/0/0/0 10']['admin_distance']

        # Check no outputs in mcast.table
        with self.assertRaises(AttributeError):
            flags = mcast.table['vrf']['default']['address_family']['ipv4']\
                ['multicast_group']['224.0.0.0/24']['source_address']['*']\
                ['flags']


if __name__ == '__main__':
    unittest.main()