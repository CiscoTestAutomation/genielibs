#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

# Genie Conf
from genie.libs.conf.dlb import Dlb

class test_dlb(TestCase):

    def test_dlb_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object
        dlb = Dlb()
        dlb.device_attr[dev1].mode = 'policy-driven per-packet'
        dlb.device_attr[dev1].dlb_interface = ['Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Ethernet1/4']
        dlb.device_attr[dev1].mac_address = '00:cc:cc:cc:cc:cd'
        dlb.device_attr[dev1].flowlet_aging = '1024'
        dlb.device_attr[dev1].static_pinning = [
            {'source': 'Ethernet1/5', 'destination': 'Ethernet1/6'}
        ]

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " mode policy-driven per-packet",
                    " dlb-interface Ethernet1/1 , Ethernet1/2 , Ethernet1/3 , Ethernet1/4",
                    " mac-address 00:cc:cc:cc:cc:cd",
                    " flowlet-aging 1024",
                    " static-pinning",
                    " source Ethernet1/5 destination Ethernet1/6",
                    " exit"
                ]
            ),
        )

        # Unconfig
        dlb = dlb.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(dlb[dev1.name]),
            "\n".join(
                [
                    "no hardware profile dlb",
                ]
            ),
        )

    def test_dlb_config_all_interfaces(self):
        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="PE1", os="nxos")

        # Create DLB object
        dlb = Dlb()
        dlb.device_attr[dev1].dlb_interface = 'all'

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " dlb-interface all",
                    " exit"
                ]
            ),
        )

    def test_dlb_config_plb(self):
        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object
        dlb = Dlb()
        dlb.device_attr[dev1].dlb_interface = ['Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Ethernet1/4']
        dlb.device_attr[dev1].flowlet_aging = '1024'
        dlb.device_attr[dev1].mode = 'per-packet'
        dlb.device_attr[dev1].mac_address = '00:cc:cc:cc:cc:cd'
        dlb.device_attr[dev1].static_pinning = [
            {'source': 'Ethernet1/5', 'destination': 'Ethernet1/6'}
        ]

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " mode per-packet",
                    " dlb-interface Ethernet1/1 , Ethernet1/2 , Ethernet1/3 , Ethernet1/4",
                    " mac-address 00:cc:cc:cc:cc:cd",
                    " flowlet-aging 1024",
                    " static-pinning",
                    " source Ethernet1/5 destination Ethernet1/6",
                    " exit"
                ]
            ),
        )

    def test_dlb_dre_thresholds(self):
        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object
        dlb = Dlb()
        dlb.device_attr[dev1].dre_thresholds = {
            'level-1': '15',
            'level-2': '20',
            'level-3': '30',
            'level-4': '15',
            'level-5': '10',
            'level-6': '5',
            'level-7': '5'
        }

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " dre-thresholds  level-1 15  level-2 20  level-3 30  level-4 15  level-5 10  level-6 5  level-7 5 ",
                    " exit"
                ]
            ),
        )

    def test_dlb_dre_thresholds_list_format(self):
        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object
        dlb = Dlb()
        # Test list format as used in vxlan_dlb.py
        dlb.device_attr[dev1].dre_thresholds = [
            {'level': '1', 'percentage': '15'},
            {'level': '2', 'percentage': '20'},
            {'level': '3', 'percentage': '30'},
            {'level': '4', 'percentage': '15'},
            {'level': '5', 'percentage': '10'},
            {'level': '6', 'percentage': '5'},
            {'level': '7', 'percentage': '5'}
        ]

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " dre-thresholds  level-1 15  level-2 20  level-3 30  level-4 15  level-5 10  level-6 5  level-7 5 ",
                    " exit"
                ]
            ),
        )

    def test_dlb_optional_parameters(self):
        # Test for Silicon One optional parameters: decay-factor, sampling-interval, load-awareness
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object
        dlb = Dlb()
        dlb.device_attr[dev1].dlb_interface = 'all'
        dlb.device_attr[dev1].flowlet_aging = '600'
        dlb.device_attr[dev1].mode = 'flowlet'
        dlb.device_attr[dev1].decay_factor = 2
        dlb.device_attr[dev1].sampling_interval = 32000
        dlb.device_attr[dev1].load_awareness = True

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " mode flowlet",
                    " dlb-interface all",
                    " flowlet-aging 600",
                    " decay-factor 2",
                    " sampling-interval 32000 nsecs",
                    " load-awareness",
                    " exit"
                ]
            ),
        )

    def test_dlb_no_load_awareness(self):
        # Test disabling load-awareness
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object
        dlb = Dlb()
        dlb.device_attr[dev1].dlb_interface = 'all'
        dlb.device_attr[dev1].load_awareness = False

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " dlb-interface all",
                    " no load-awareness",
                    " exit"
                ]
            ),
        )

    def test_dlb_complete_silicon_one_config(self):
        # Complete configuration example from the guide for Silicon One switches
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object with all Silicon One parameters
        dlb = Dlb()
        dlb.device_attr[dev1].dlb_interface = 'all'
        dlb.device_attr[dev1].flowlet_aging = 600
        dlb.device_attr[dev1].mode = 'flowlet'
        dlb.device_attr[dev1].decay_factor = 2
        dlb.device_attr[dev1].sampling_interval = 32000
        dlb.device_attr[dev1].load_awareness = True

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " mode flowlet",
                    " dlb-interface all",
                    " flowlet-aging 600",
                    " decay-factor 2",
                    " sampling-interval 32000 nsecs",
                    " load-awareness",
                    " exit"
                ]
            ),
        )

    def test_dlb_complete_cloudscale_config(self):
        # Complete configuration example from the guide for CloudScale switches
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="node01", os="nxos")

        # Create DLB object with all CloudScale parameters
        dlb = Dlb()
        dlb.device_attr[dev1].dlb_interface = ['Ethernet1/5', 'Ethernet1/7', 'Ethernet1/17', 'Ethernet1/21', 'Ethernet1/26']
        dlb.device_attr[dev1].dre_thresholds = [
            {'level': '1', 'percentage': '15'},
            {'level': '2', 'percentage': '20'},
            {'level': '3', 'percentage': '30'},
            {'level': '4', 'percentage': '15'},
            {'level': '5', 'percentage': '10'},
            {'level': '6', 'percentage': '5'},
            {'level': '7', 'percentage': '5'}
        ]
        dlb.device_attr[dev1].flowlet_aging = 600
        dlb.device_attr[dev1].mac_address = 'aa:bb:cc:dd:ee:ff'
        dlb.device_attr[dev1].mode = 'flowlet'
        dlb.device_attr[dev1].static_pinning = [
            {'source': 'Ethernet1/1', 'destination': 'Ethernet1/2'}
        ]

        # add feature to device
        dev1.add_feature(dlb)

        # Build config
        cfgs = dlb.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "hardware profile dlb",
                    " mode flowlet",
                    " dlb-interface Ethernet1/5 , Ethernet1/7 , Ethernet1/17 , Ethernet1/21 , Ethernet1/26",
                    " mac-address aa:bb:cc:dd:ee:ff",
                    " flowlet-aging 600",
                    " dre-thresholds  level-1 15  level-2 20  level-3 30  level-4 15  level-5 10  level-6 5  level-7 5 ",
                    " static-pinning",
                    " source Ethernet1/1 destination Ethernet1/2",
                    " exit"
                ]
            ),
        )

if __name__ == '__main__':
    unittest.main()
