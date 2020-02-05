
# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.ops.base import Base
from genie.ops.base.maker import Maker
from genie.libs.ops.hsrp.iosxe.hsrp import Hsrp
from genie.libs.ops.hsrp.iosxe.tests.hsrp_output import HsrpOutput

# Parser
from genie.libs.parser.iosxe.show_standby import ShowStandbyInternal,\
                                      ShowStandbyAll,\
                                      ShowStandbyDelay


class test_hsrp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full(self):
        f = Hsrp(device=self.device)
        # Get 'show standby all' output
        f.maker.outputs[ShowStandbyAll] = {'':HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        f.maker.outputs[ShowStandbyInternal] = \
            {'':HsrpOutput.showStandbyInternalOutput}
        # Get 'show standby delay' output
        f.maker.outputs[ShowStandbyDelay] = \
            {'':HsrpOutput.showStandbyDelayOutput}
        # Learn the feature
        f.learn()
        # Check
        self.maxDiff = None
        self.assertEqual(f.info, HsrpOutput.hsrpOpsOutput)

    def test_selective_attribute(self):
        f = Hsrp(device=self.device)
        # Get 'show standby all' output
        f.maker.outputs[ShowStandbyAll] = {'':HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        f.maker.outputs[ShowStandbyInternal] = \
            {'':HsrpOutput.showStandbyInternalOutput}
        # Get 'show standby delay' output
        f.maker.outputs[ShowStandbyDelay] = \
            {'':HsrpOutput.showStandbyDelayOutput}
        # Get 'show standby delay' output
        f.maker.outputs[ShowStandbyDelay] = \
            {'':HsrpOutput.showStandbyDelayOutput}
        # Learn the feature
        f.learn()
        # Check match
        self.assertEqual('0000.0c9f.f000', f.info['GigabitEthernet1/0/1']\
            ['address_family']['ipv4']['version'][2]['groups'][0]\
            ['virtual_mac_address'])
        # Check does not match
        self.assertNotEqual(True, f.info['GigabitEthernet1/0/1']['use_bia'])

    def test_missing_attributes(self):
        f = Hsrp(device=self.device)
        # Get 'show standby all' output
        f.maker.outputs[ShowStandbyAll] = {'':HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        f.maker.outputs[ShowStandbyInternal] = \
            {'':HsrpOutput.showStandbyInternalOutput}
        # Get 'show standby delay' output
        f.maker.outputs[ShowStandbyDelay] = \
            {'':HsrpOutput.showStandbyDelayOutput}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            hsrp_bfd_sessions_total=f.info['num_bfd_sessions']

    def test_incomplete_output(self):
        f = Hsrp(device=self.device)
        # Get 'show standby all' output
        f.maker.outputs[ShowStandbyAll] = {'':''}
        # Get 'show standby internal' output
        f.maker.outputs[ShowStandbyInternal] = \
            {'':HsrpOutput.showStandbyInternalOutput}
        # Get 'show standby delay' output
        f.maker.outputs[ShowStandbyDelay] = \
            {'':HsrpOutput.showStandbyDelayOutput}
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            hsrp_groups=f.info['groups']

    def test_ignored(self):
        f = Hsrp(device=self.device)
        # Get 'show standby all' output
        f.maker.outputs[ShowStandbyAll] = {'':HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        f.maker.outputs[ShowStandbyInternal] = \
            {'':HsrpOutput.showStandbyInternalOutput}
        # Get 'show standby delay' output
        f.maker.outputs[ShowStandbyDelay] = \
            {'':HsrpOutput.showStandbyDelayOutput}
        
        g = Hsrp(device=self.device)
        # Get 'show standby all' output
        g.maker.outputs[ShowStandbyAll] = {'':HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        g.maker.outputs[ShowStandbyInternal] = \
            {'':HsrpOutput.showStandbyInternalOutput}
        # Get 'show standby delay' output
        g.maker.outputs[ShowStandbyDelay] = \
            {'':HsrpOutput.showStandbyDelayOutput}
        
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
