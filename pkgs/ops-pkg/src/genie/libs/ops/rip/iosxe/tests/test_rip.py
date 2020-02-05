# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock
# genie.libs
from genie.libs.ops.rip.iosxe.rip import Rip
from genie.libs.ops.rip.iosxe.tests.rip_output import RipOutput

from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

outputs = {}
outputs['show ip protocols | sec rip'] = RipOutput.showIpProtocols_default
outputs['show ip protocols vrf VRF1 | sec rip'] = RipOutput.showIpProtocols_vrf1
outputs['show ip rip database'] = RipOutput.showIpRipDatabase_default
outputs['show ip rip database vrf VRF1'] = RipOutput.showIpRipDatabase_vrf1

outputs['show ipv6 protocols | sec rip'] = RipOutput.showIpv6Protocols_default
outputs['show ipv6 protocols vrf VRF1 | sec rip'] = RipOutput.showIpv6Protocols_vrf1
outputs['show ipv6 rip database'] = RipOutput.showIpv6RipDatabase_default
outputs['show ipv6 rip vrf VRF1 database'] = RipOutput.showIpv6RipDatabase_vrf1
outputs['show ipv6 rip'] = RipOutput.showIpv6Rip_default
outputs['show ipv6 rip vrf VRF1'] = RipOutput.showIpv6Rip_vrf1

def mapper(key):
    return outputs[key]

class test_rip_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_rip(self):
        f = Rip(device=self.device)
        f.maker.outputs[ShowVrfDetail] = {'': RipOutput.ShowVrfDetail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, RipOutput.ripOpsOutput)

    def test_selective_attribute_rip(self):
        f = Rip(device=self.device)
        f.maker.outputs[ShowVrfDetail] = {'': RipOutput.ShowVrfDetail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()

        # Check match
        self.assertEqual('auto-summary', f.info['vrf']['VRF1']['address_family']['ipv4']['instance']\
            ['rip']['routes']['10.0.0.0/8']['index'][1]['summary_type'])

        # Check does not match
        self.assertNotEqual('192.168.10.0/24', f.info['vrf']['VRF1']['address_family']['ipv4']\
            ['instance']['rip']['routes'])


    def test_missing_attributes_rip(self):
        f = Rip(device=self.device)
        f.maker.outputs[ShowVrfDetail] = {'': RipOutput.ShowVrfDetail}

        # Get 'show ip static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            metric = f.info['vrf']['VRF1']['address_family']['ipv4']['instance']\
                ['routes']['172.16.11.0/24']['index']['1']['metric']

    def test_empty_output_rip(self):
        self.maxDiff = None
        f = Rip(device=self.device)
        # Get outputs

        f.maker.outputs[ShowVrfDetail] = {'': {}}

        outputs['show ip protocols | sec rip'] = ''
        outputs['show ip protocols vrf VRF1 | sec rip'] = ''
        outputs['show ip rip database'] = ''
        outputs['show ip rip database vrf VRF1'] = ''
        outputs['show ipv6 protocols | sec rip'] = ''
        outputs['show ipv6 protocols vrf VRF1 | sec rip'] = ''
        outputs['show ipv6 rip database'] = ''
        outputs['show ipv6 rip vrf VRF1 database'] = ''
        outputs['show ipv6 rip'] = ''
        outputs['show ipv6 rip vrf VRF1'] = ''
        # Return outputs above as inputs to parser when called

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()

        # revert back
        outputs['show ip protocols | sec rip'] = RipOutput.showIpProtocols_default
        outputs['show ip protocols vrf VRF1 | sec rip'] = RipOutput.showIpProtocols_vrf1
        outputs['show ip rip database'] = RipOutput.showIpRipDatabase_default
        outputs['show ip rip database vrf VRF1'] = RipOutput.showIpRipDatabase_vrf1
        outputs['show ipv6 protocols | sec rip'] = RipOutput.showIpv6Protocols_default
        outputs['show ipv6 protocols vrf VRF1 | sec rip'] = RipOutput.showIpv6Protocols_vrf1
        outputs['show ipv6 rip database'] = RipOutput.showIpv6RipDatabase_default
        outputs['show ipv6 rip vrf VRF1 database'] = RipOutput.showIpv6RipDatabase_vrf1
        outputs['show ipv6 rip'] = RipOutput.showIpv6Rip_default
        outputs['show ipv6 rip vrf VRF1'] = RipOutput.showIpv6Rip_vrf1

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']


if __name__ == '__main__':
    unittest.main()
