# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.mcast.nxos.mcast import Mcast
from genie.libs.ops.mcast.nxos.tests.mcast_output import McastOutput

# nxos show_mcast
from genie.libs.parser.nxos.show_mcast import ShowIpMrouteVrfAll, ShowIpv6MrouteVrfAll,\
                                   ShowIpStaticRouteMulticast,\
                                   ShowIpv6StaticRouteMulticast

# nxos show_feature
from genie.libs.parser.nxos.show_feature import ShowFeature


class test_mcast(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device


    def test_complete_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowFeature] = {'':McastOutput.ShowFeature}
        mcast.maker.outputs[ShowIpMrouteVrfAll] = {'':McastOutput.ShowIpMrouteVrfAll}
        mcast.maker.outputs[ShowIpv6MrouteVrfAll] = \
            {'':McastOutput.ShowIpv6MrouteVrfAll}
        mcast.maker.outputs[ShowIpStaticRouteMulticast] = \
            {'':McastOutput.ShowIpStaticRouteMulticast}
        mcast.maker.outputs[ShowIpv6StaticRouteMulticast] = \
            {'':McastOutput.ShowIpv6StaticRouteMulticast}

        # Learn the feature
        mcast.learn()

        # Verify Ops was created successfully
        self.assertEqual(mcast.info, McastOutput.McastInfo)
        self.assertEqual(mcast.table, McastOutput.McastTable)


    def test_selective_attribute(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowFeature] = {'':McastOutput.ShowFeature}
        mcast.maker.outputs[ShowIpMrouteVrfAll] = {'':McastOutput.ShowIpMrouteVrfAll}
        mcast.maker.outputs[ShowIpv6MrouteVrfAll] = \
            {'':McastOutput.ShowIpv6MrouteVrfAll}
        mcast.maker.outputs[ShowIpStaticRouteMulticast] = \
            {'':McastOutput.ShowIpStaticRouteMulticast}
        mcast.maker.outputs[ShowIpv6StaticRouteMulticast] = \
            {'':McastOutput.ShowIpv6StaticRouteMulticast}

        # Learn the feature
        mcast.learn()

        # Test specific attributes in info
        self.assertEqual(mcast.info['vrf']['default']['address_family']['ipv4']\
                ['mroute']['10.49.0.0/8']['path']['0.0.0.0/32 Null0']\
                ['neighbor_address'], '0.0.0.0/32')

        # Test specific attribute in table
        self.assertEqual(mcast.table['vrf']['VRF1']['address_family']\
                ['ipv4']['multicast_group']['232.0.0.0/8']\
                ['source_address']['*']['flags'], 'pim ip')


    def test_empty_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowFeature] = {'':''}
        mcast.maker.outputs[ShowIpMrouteVrfAll] = {'':''}
        mcast.maker.outputs[ShowIpv6MrouteVrfAll] = {'':''}
        mcast.maker.outputs[ShowIpStaticRouteMulticast] = {'':''}
        mcast.maker.outputs[ShowIpv6StaticRouteMulticast] = {'':''}

        # Learn the feature
        mcast.learn()

        # Check no outputs in mcast.info
        with self.assertRaises(AttributeError):
            neighbor_address = mcast.info['vrf']['default']['address_family']\
                ['ipv4']['mroute']['10.49.0.0/8']['path']['0.0.0.0/32 Null0']\
                ['neighbor_address']

        # Check no outputs in mcast.table
        with self.assertRaises(AttributeError):
            flags = mcast.table['vrf']['VRF1']['address_family']\
                ['ip multicast']['multicast_group']['232.0.0.0/8']\
                ['source_address']['*']['flags']


    def test_incomplete_output(self):
        mcast = Mcast(device=self.device)

        # Set outputs
        mcast.maker.outputs[ShowFeature] = {'':McastOutput.ShowFeature}
        mcast.maker.outputs[ShowIpMrouteVrfAll] = {'':McastOutput.ShowIpMrouteVrfAll}
        mcast.maker.outputs[ShowIpv6MrouteVrfAll] = {'':''}
        mcast.maker.outputs[ShowIpStaticRouteMulticast] = \
            {'':McastOutput.ShowIpStaticRouteMulticast}
        mcast.maker.outputs[ShowIpv6StaticRouteMulticast] = {'':''}

        # Learn the feature
        mcast.learn()

        # Test specific attributes in info
        self.assertEqual(mcast.info['vrf']['default']['address_family']['ipv4']\
                ['mroute']['10.49.0.0/8']['path']['0.0.0.0/32 Null0']\
                ['neighbor_address'], '0.0.0.0/32')

        # Test specific attribute in table
        self.assertEqual(mcast.table['vrf']['VRF1']['address_family']\
                ['ipv4']['multicast_group']['232.0.0.0/8']\
                ['source_address']['*']['flags'], 'pim ip')


if __name__ == '__main__':
    unittest.main()