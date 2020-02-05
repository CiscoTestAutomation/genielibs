#!/bin/env python

# BASIC LOGGER SETUP {{{
import logging
import pyats.log
logging.root.addHandler(pyats.log.managed_handlers.screen)
# }}}
#logging.root.setLevel(logging.DEBUG)
import types
import unittest
import functools
import os

from pyats.datastructures.logic import And, Not, Or
import pyats.topology
import genie.conf
import genie.conf.base

from genie.libs.conf.topology_mapper import TopologyMapper

firex_topology1_yaml = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'firex_topology1.yaml')

firex_topology3_yaml = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'firex_topology3.yaml')

class TestResolve(unittest.TestCase):

    def test_topology_objects_1(self):

        for subtest, topology_cls in (
                ("TopologyMapper", functools.partial(TopologyMapper,
                                                     topology_file=firex_topology1_yaml)),
                #("TestTopology1", TestTopology1),
        ):
            with self.subTest(subtest):

                topology = topology_cls()
                try:
                    self.assertSequenceEqual(topology.device_names, [
                        'R1', 'R2', 'R3',
                        ])
                    self.assertSequenceEqual(topology.link_names, [
                        'L1', 'L2', 'L3',
                        ])
                    self.assertSequenceEqual(topology.interface_names, [
                        'R1I1', 'R1I2',
                        'R2I1', 'R2I2',
                        'R3I1', 'R3I2',
                        ])
                    self.assertSequenceEqual(tuple(topology.object_names), [
                        'R1', 'R2', 'R3',
                        'L1', 'L2', 'L3',
                        'R1I1', 'R1I2',
                        'R2I1', 'R2I2',
                        'R3I1', 'R3I2',
                        ])
                except AssertionError:
                    self.assertEqual(topology.device_names, None)
                    self.assertEqual(topology.link_names, None)
                    self.assertEqual(topology.interface_names, None)
                    self.assertTrue(type(topology.object_names),
                        types.GeneratorType)

    def test_genie_testbed_1(self):

        pyats_testbed = pyats.topology.loader.load(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'pyats_topology1.yaml'))

        for pyats_device in pyats_testbed.devices.values():
            self.assertIsInstance(pyats_device, pyats.topology.Device)

            for pyats_intf in pyats_device.interfaces.values():
                self.assertIsInstance(pyats_intf, pyats.topology.Interface)

        for pyats_link in list(pyats_testbed.links):
            self.assertIsInstance(pyats_link, pyats.topology.Link)

        genie_testbed = genie.conf.Genie.init(pyats_testbed)

        for xos_device in genie_testbed.devices.values():
            self.assertIsInstance(xos_device, genie.conf.base.Device)

            for xos_intf in xos_device.interfaces.values():
                self.assertIsInstance(xos_intf, genie.conf.base.Interface)

        for xos_link in genie_testbed.links:
            self.assertIsInstance(xos_link, genie.conf.base.Link)

    def test_genie_testbed_2(self):

        pyats_testbed = pyats.topology.loader.load(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'pyats_topology1.yaml'))

        self.assertCountEqual(pyats_testbed.devices.keys(), [
            'router1',
            'router2',
            'router3',
            'router4',
            'ixia',
            ])

        genie_testbed = genie.conf.base.loader.load(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'pyats_topology1.yaml'))

        self.assertCountEqual(
                genie_testbed.devices.keys(),
                pyats_testbed.devices.keys())

        self.assertTrue(len(genie_testbed.find_devices()) ==
            len(pyats_testbed.devices.values()))

        self.assertCountEqual(
                genie_testbed.find_devices(),
                genie_testbed.devices.values())

        router1 = genie_testbed.devices['router1']
        self.assertEqual(router1.name, 'router1')
        self.assertEqual(router1.os, 'iosxr')

        self.assertCountEqual(
                genie_testbed.find_devices(),
                genie_testbed.devices.values())

        self.assertIn(
                router1,
                genie_testbed.find_devices(os=Or('iosxr')))

        self.assertSetEqual(
                set([device.os for device in genie_testbed.find_devices(os=Or('iosxr'))]),
                set(['iosxr']))

if __name__ == "__main__":
    unittest.main()

# vim: ft=python ts=8 sw=4 et
