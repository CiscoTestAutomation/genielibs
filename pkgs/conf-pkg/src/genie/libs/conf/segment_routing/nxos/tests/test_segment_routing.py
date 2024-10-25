#!/usr/bin/env python

import unittest
from unittest.mock import Mock

# Genie Imports
from genie.conf import Genie
from genie.conf.base import Testbed, Device
from genie.conf.base.attributes import UnsupportedAttributeWarning

# SegmentRouting Imports
from genie.libs.conf.segment_routing import SegmentRouting, PrefixSidMapEntry

from ipaddress import IPv4Network

class TestSegmentRouting(unittest.TestCase):
    """Unit tests for SegmentRouting configuration."""

    def setUp(self):
        """Set up the test environment before each test."""
        # Initialize the Genie testbed
        testbed = Testbed()
        Genie.testbed = testbed

        # Create a device with OS 'nxos'
        self.dev = Device(name='node01', testbed=testbed, os='nxos')

        # Initialize SegmentRouting and add it to the device
        self.sr = SegmentRouting()
        self.dev.add_feature(self.sr)

    def test_segment_routing_config(self):
        """
        Test SegmentRouting configuration by setting attributes directly.
        """
        self.maxDiff = None  # Allow full diff output on failure

        # Set SegmentRouting attributes directly
        self.sr.device_attr[self.dev].mpls = True
        self.sr.device_attr[self.dev].global_block = range(70000, 100000)
        self.sr.device_attr[self.dev].timers_srgb_cleanup = 120
        self.sr.device_attr[self.dev].timers_srgb_retry = 240

        # Access the address_family_attr for 'ipv4'
        ipv4_af_attr = self.sr.device_attr[self.dev].address_family_attr['ipv4']

        # Create PrefixSidMapEntry instances
        entry1 = PrefixSidMapEntry(prefix=IPv4Network('99.1.1.4/32'), index=4)
        entry2 = PrefixSidMapEntry(prefix=IPv4Network('98.1.1.1/32'), index=3)
        entry3 = PrefixSidMapEntry(prefix=IPv4Network('10.1.1.4/32'), absolute=100)

        # Add entries to connected_prefix_sid_map using the provided method
        ipv4_af_attr.add_connected_prefix_sid_map_entry(entry1)
        ipv4_af_attr.add_connected_prefix_sid_map_entry(entry2)
        ipv4_af_attr.add_connected_prefix_sid_map_entry(entry3)

        # **Remove the incorrect assignment**
        # self.sr.device_attr[self.dev].connected_prefix_sid_map = ipv4_af_attr
        self.sr.device_attr[self.dev].connected_prefix_sid_map = {entry1, entry2, entry3}
    
        # Build SegmentRouting configuration without applying
        cfgs = self.sr.build_config(apply=False)

        # Define the expected configuration
        expected_config = '\n'.join([
            'segment-routing',
            ' mpls',
            ' global-block 70000 100000',
            ' timers srgb cleanup 120',
            ' timers srgb retry 240',
            ' connected-prefix-sid-map',
            '  address-family ipv4',
            '   98.1.1.1/32 index 3',
            '   99.1.1.4/32 index 4',
            '   10.1.1.4/32 absolute 100',
            '   exit',
            '  exit',
            ' exit'
        ])
        # Compare the generated configuration with the expected configuration
        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            expected_config
        )

    def test_segment_routing_config_shutdown(self):
        """
        Test SegmentRouting configuration by setting attributes directly.
        """
        self.maxDiff = None  # Allow full diff output on failure

        # Set SegmentRouting attributes directly
        self.sr.device_attr[self.dev].mpls = True
        self.sr.device_attr[self.dev].shutdown = True 
        self.sr.device_attr[self.dev].global_block = range(70000, 100000)
        self.sr.device_attr[self.dev].timers_srgb_cleanup = 120
        self.sr.device_attr[self.dev].timers_srgb_retry = 240

        # Create PrefixSidMapEntry instances
        entry1 = PrefixSidMapEntry(prefix=IPv4Network('99.1.1.4/32'), index=4)
        entry2 = PrefixSidMapEntry(prefix=IPv4Network('98.1.1.1/32'), index=3)
        entry3 = PrefixSidMapEntry(prefix=IPv4Network('10.1.1.4/32'), absolute=100)

        self.sr.device_attr[self.dev].connected_prefix_sid_map = {entry1, entry2, entry3}
    
        # Build SegmentRouting configuration without applying
        cfgs = self.sr.build_config(apply=False)

        # Define the expected configuration
        expected_config = '\n'.join([
            'segment-routing',
            ' mpls',
            ' shutdown',
            ' global-block 70000 100000',
            ' timers srgb cleanup 120',
            ' timers srgb retry 240',
            ' connected-prefix-sid-map',
            '  address-family ipv4',
            '   98.1.1.1/32 index 3',
            '   99.1.1.4/32 index 4',
            '   10.1.1.4/32 absolute 100',
            '   exit',
            '  exit',
            ' exit'
        ])
        # Compare the generated configuration with the expected configuration
        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            expected_config
        )

    def test_segment_routing_unconfig(self):
        """
        Test unconfiguring SegmentRouting settings.
        """
        self.maxDiff = None  # Allow full diff output on failure

        # Define attributes to set first
        attributes = {
            'device_attr': { 
                self.dev.name: {
                    'mpls': True,
                    'global_block': range(70000, 100000), 
                    'timers_srgb_cleanup': 120,
                    'timers_srgb_retry': 240,
                    'address_family_attr': {
                        'ipv4': {
                        'connected_prefix_sid_map': [
                            {'prefix': '99.1.1.4/32', 'index': 4}, 
                            {'prefix': '98.1.1.1/32', 'index': 3}, 
                            {'prefix': '10.1.1.4/32', 'absolute': 100}
                            ]
                            }
                        }
                    }
            }
        }

        # Apply the attributes to configure SegmentRouting
        self.sr.build_config(apply=False, attributes=attributes)

        # Now, attempt to unconfigure SegmentRouting
        cfgs = self.sr.build_unconfig(apply=False)

        # Define the expected unconfiguration
        expected_unconfig = '\n'.join([
            'no segment-routing',
        ])

        # Compare the generated unconfiguration with the expected result
        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            expected_unconfig
        )

if __name__ == '__main__':
    unittest.main()
