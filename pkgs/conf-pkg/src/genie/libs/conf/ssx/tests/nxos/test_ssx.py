#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device
from genie.conf.base.attributes import UnsupportedAttributeWarning

# ssx
from genie.libs.conf.ssx.ssx import Ssx


class test_ssx(TestCase):

    def setUp(self):

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        self.dev = Device(name='node01', testbed=testbed, os='nxos')

        # ssx object
        self.ssx = Ssx()
        self.dev.add_feature(self.ssx)

    def test_ssx_config(self):

        self.maxDiff = None
        self.ssx.device_attr[self.dev].enable_hardware_telemetry = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].enable_hardware_telemetry_ssx = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp1']
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp1'].source_ip = '15.15.15.15'
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp1'].dest_ip = '14.1.1.2'
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp1'].source_port = 100
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp1'].dest_port = 200
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp1'].dscp = 20
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp2']
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp2'].source_ip = '25.25.25.25'
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp2'].dest_ip = '15.1.1.2'
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp2'].source_port = 300
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp2'].dest_port = 400
        self.ssx.device_attr[self.dev].hwtele_attr[None].exporter_attr['exp2'].dscp = 25
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec1']
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec1'].egress_queue_drops = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec1'].egress_queue_peak = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec1'].egress_queue_depth = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec1'].ingress_queue_drops = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec1'].ingress_queue_depth = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec1'].record_interval = 2000
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec2']
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec2'].egress_queue_microburst = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec2'].egress_pool_group_depth = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec2'].egress_buffer_depth = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec2'].ethernet_counters = True
        self.ssx.device_attr[self.dev].hwtele_attr[None].record_attr['rec2'].record_interval = 4000
        self.ssx.device_attr[self.dev].hwtele_attr[None].monitor_attr['mon1']
        self.ssx.device_attr[self.dev].hwtele_attr[None].monitor_attr['mon1'].rec_name = 'rec1'
        self.ssx.device_attr[self.dev].hwtele_attr[None].monitor_attr['mon1'].exp_name = 'exp1'
        self.ssx.device_attr[self.dev].hwtele_attr[None].monitor_attr['mon2']
        self.ssx.device_attr[self.dev].hwtele_attr[None].monitor_attr['mon2'].rec_name = 'rec2'
        self.ssx.device_attr[self.dev].hwtele_attr[None].monitor_attr['mon2'].exp_name = 'exp2'
        self.ssx.device_attr[self.dev].hwtele_attr[None].ssx_system_monitor = ['mon1','mon2']
        self.ssx.device_attr[self.dev].hwtele_attr[None].ssx_id = 5

        # Build ssx configuration
        cfgs = self.ssx.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'feature hardware-telemetry',
                'hardware-telemetry ssx',
                ' ssx exporter exp1',
                '  source 15.15.15.15',
                '  destination 14.1.1.2 use-vrf default',
                '  transport udp src-port 100 and dst-port 200',
                '  dscp 20',
                '  exit',
                ' ssx exporter exp2',
                '  source 25.25.25.25',
                '  destination 15.1.1.2 use-vrf default',
                '  transport udp src-port 300 and dst-port 400',
                '  dscp 25',
                '  exit',
                ' ssx record rec1',
                '  collect egress queue drops',
                '  collect egress queue peak',
                '  collect egress queue depth',
                '  collect ingress queue drops',
                '  collect ingress queue depth',
                '  interval 2000',
                '  exit',
                ' ssx record rec2',
                '  collect egress queue microburst',
                '  collect ethernet counters',
                '  collect egress pool-group depth',
                '  collect egress buffer depth',
                '  interval 4000',
                '  exit',
                ' ssx monitor mon1',
                '  record rec1',
                '  exporter exp1',
                '  exit',
                ' ssx monitor mon2',
                '  record rec2',
                '  exporter exp2',
                '  exit',
                ' ssx system monitor mon1',
                ' ssx system monitor mon2',
                ' ssx system system-id 5',
                ' exit'
            ]))

        cfgs = self.ssx.build_unconfig(apply=False)

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'no feature hardware-telemetry',
            ]))

        #############
        #partial config testcases 
        #############

        cfgs = self.ssx.build_unconfig(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': { '*': {'exporter_attr': { 'exp1': {'source_ip': None}}}}}}})
        

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'hardware-telemetry ssx',
                ' ssx exporter exp1',
                '  no source 15.15.15.15',
                '  exit',
                ' exit'
            ]))

        cfgs = self.ssx.build_unconfig(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': { '*': {'exporter_attr': { '*': {'source_ip': None}}}}}}})

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'hardware-telemetry ssx',
                ' ssx exporter exp1',
                '  no source 15.15.15.15',
                '  exit',
                ' ssx exporter exp2',
                '  no source 25.25.25.25',
                '  exit',
                ' exit'
            ]))

        cfgs = self.ssx.build_config(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': { '*': {'exporter_attr': { 'exp1': {'source_ip': '*'}}}}}}})
        

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'hardware-telemetry ssx',
                ' ssx exporter exp1',
                '  source 15.15.15.15',
                '  exit',
                ' exit'
            ]))

        cfgs = self.ssx.build_config(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': { '*': {'exporter_attr': { '*': {'source_ip': '*' }}}}}}})
        

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'hardware-telemetry ssx',
                ' ssx exporter exp1',
                '  source 15.15.15.15',
                '  exit',
                ' ssx exporter exp2',
                '  source 25.25.25.25',
                '  exit',
                ' exit'
            ]))

        cfgs = self.ssx.build_unconfig(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': { '*': {'record_attr': { '*': {'egress_queue_drops': False}}}}}}})


        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'hardware-telemetry ssx',
                ' ssx record rec1',
                '  no collect egress queue drops',
                '  exit',
                ' exit'
            ]))   


        cfgs = self.ssx.build_unconfig(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': { '*': {'exporter_attr': {  "*":None}}}}}})
        

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'hardware-telemetry ssx',
                ' no ssx exporter exp1',
                ' no ssx exporter exp2',
                ' exit'
            ]))

        cfgs = self.ssx.build_unconfig(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': { '*': {'exporter_attr': { 'exp1':None}}}}}})

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'hardware-telemetry ssx',
                ' no ssx exporter exp1',
                ' exit'
            ]))

        cfgs = self.ssx.build_unconfig(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'hwtele_attr': {  '*':None}}}})

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'no hardware-telemetry ssx'
            ])) 

if __name__ == '__main__':
    unittest.main()