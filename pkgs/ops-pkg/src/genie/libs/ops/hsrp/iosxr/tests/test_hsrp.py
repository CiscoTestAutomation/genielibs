
# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.ops.base import Base
from genie.ops.base.maker import Maker
from genie.libs.ops.hsrp.iosxr.hsrp import Hsrp
from genie.libs.ops.hsrp.iosxr.tests.hsrp_output import HsrpOutput

# Parser
from genie.libs.parser.iosxr.show_hsrp import ShowHsrpSummary, ShowHsrpDetail


class test_hsrp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full(self):
        self.maxDiff = None
        f = Hsrp(device=self.device)
        # Get 'show hsrp detail' output
        f.maker.outputs[ShowHsrpDetail] = {'':HsrpOutput.showHsrpDetailOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Learn the feature
        f.learn()
        # Check all match
        self.assertEqual(f.info, HsrpOutput.hsrpOpsOutput)
    
    def test_selective_attribute(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp detail' output
        f.maker.outputs[ShowHsrpDetail] = {'':HsrpOutput.showHsrpDetailOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Learn the feature
        f.learn()
        # Check match
        self.assertEqual('active', f.info['GigabitEthernet0/0/0/0']\
            ['address_family']['ipv4']['version'][1]['groups'][10]\
            ['hsrp_router_state'])
        # Check does not match
        self.assertNotEqual(6, f.info['GigabitEthernet0/0/0/0']['bfd']\
                ['detection_multiplier'])

    def test_missing_attributes(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp detail' output
        f.maker.outputs[ShowHsrpDetail] = {'':HsrpOutput.showHsrpDetailOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            hsrp_track_objects_up=f.info['GigabitEthernet0/0/0/0']\
                ['address_family']['ipv4']['version'][2]

    def test_incomplete_output(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp detail' output
        f.maker.outputs[ShowHsrpDetail] \
            = {'':HsrpOutput.showHsrpDetailOutputIncomplete}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            hsrp_groups=f.info['GigabitEthernet0/0/0/0']['address_family']\
                ['ipv4']['version'][1]['groups'][0]['timers']

    def test_ignored(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp detail' output
        f.maker.outputs[ShowHsrpDetail] = {'':HsrpOutput.showHsrpDetailOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = \
            {'':HsrpOutput.showHsrpSummaryOutput}
        
        g = Hsrp(device=self.device)
        # Get 'show hsrp detail' output
        g.maker.outputs[ShowHsrpDetail] = {'':HsrpOutput.showHsrpDetailOutput}
        # Get 'show hsrp summary' output
        g.maker.outputs[ShowHsrpSummary] = \
            {'':HsrpOutput.showHsrpSummaryOutput}
        
        # Learn the feature
        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f, g)
        
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ("+s: 2")
        self.assertEqual(sorted_diff, sorted_result)

if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4
