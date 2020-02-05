
# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.ops.base import Base
from genie.ops.base.maker import Maker
from genie.libs.ops.hsrp.nxos.hsrp import Hsrp
from genie.libs.ops.hsrp.nxos.tests.hsrp_output import HsrpOutput

# Parser
from genie.libs.parser.nxos.show_hsrp import ShowHsrpSummary, ShowHsrpAll, ShowHsrpDelay


class test_hsrp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full(self):

        f = Hsrp(device=self.device)
        # Get 'show hsrp all' output
        f.maker.outputs[ShowHsrpAll] = {'':HsrpOutput.showHsrpAllOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Get 'show hsrp delay' output
        f.maker.outputs[ShowHsrpDelay] = {'':HsrpOutput.showHsrpDelayOutput}
        # Learn the feature
        f.learn()
        # Check
        self.maxDiff = None
        self.assertEqual(f.info, HsrpOutput.hsrpOpsOutput)

    def test_selective_attribute(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp all' output
        f.maker.outputs[ShowHsrpAll] = {'':HsrpOutput.showHsrpAllOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Get 'show hsrp delay' output
        f.maker.outputs[ShowHsrpDelay] = {'':HsrpOutput.showHsrpDelayOutput}
        # Learn the feature
        f.learn()
        # Check match
        self.assertEqual(110, f.info['Ethernet1/3']['address_family']['ipv4']\
                ['version'][2]['groups'][0]['priority'])
        # Check does not match
        self.assertNotEqual(100, f.info['Ethernet1/3']['delay']\
            ['minimum_delay'])

    def test_missing_attributes(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp all' output
        f.maker.outputs[ShowHsrpAll] = {'':HsrpOutput.showHsrpAllOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Get 'show hsrp delay' output
        f.maker.outputs[ShowHsrpDelay] = {'':HsrpOutput.showHsrpDelayOutput}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            hsrp_bfd_sessions_total=f.info['bfd_sessions_total']

    def test_incomplete_output(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp all' output
        f.maker.outputs[ShowHsrpAll] = {'':HsrpOutput.showHsrpAllOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Get 'show hsrp delay' output
        f.maker.outputs[ShowHsrpDelay] = {'':''}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            hsrp_groups=f.info['Ethernet1/3']['delay']['reload_delay']

    def test_ignored(self):
        f = Hsrp(device=self.device)
        # Get 'show hsrp all' output
        f.maker.outputs[ShowHsrpAll] = {'':HsrpOutput.showHsrpAllOutput}
        # Get 'show hsrp summary' output
        f.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Get 'show hsrp delay' output
        f.maker.outputs[ShowHsrpDelay] = {'':HsrpOutput.showHsrpDelayOutput}        
        g = Hsrp(device=self.device)
        # Get 'show hsrp all' output
        g.maker.outputs[ShowHsrpAll] = {'':HsrpOutput.showHsrpAllOutput}
        # Get 'show hsrp summary' output
        g.maker.outputs[ShowHsrpSummary] = {'':HsrpOutput.showHsrpSummaryOutput}
        # Get 'show hsrp delay' output
        g.maker.outputs[ShowHsrpDelay] = {'':HsrpOutput.showHsrpDelayOutput}
        
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
