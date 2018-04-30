#!/usr/bin/env python

import unittest
from pprint import pprint
import re
from unittest.mock import Mock
from genie.conf.tests import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device
from genie.libs.conf.lisp import (Lisp,
                                        Encapsulation,
                                        ServiceType)


class TestLisp(TestCase):

    def setUp(self):
        tb = Genie.testbed = Testbed()
        self.xtr1 = Device(name="xtr1", testbed=tb, os='iosxe')
        self.msmr = Device(name="msmr", testbed=tb, os='iosxe')
        self.lisp = Lisp()
        self.xtr1.add_feature(self.lisp)

    def test_top_level(self):
        self.lisp.device_attr['xtr1'].router_lisp_id = ""
        self.lisp.device_attr['xtr1'].vrf_attr[None].security = "high"
        self.lisp.device_attr['xtr1'].vrf_attr[None].locator_table = "default"
        self.lisp.device_attr['xtr1'].vrf_attr[None].control_packet = 1450
        self.lisp.device_attr['xtr1'].vrf_attr[None].ddt = "root 2001:db8::1"
        self.lisp.device_attr['xtr1'].vrf_attr[None].decapsulation = "filter rloc source locator-set FOO"
        self.lisp.device_attr['xtr1'].vrf_attr[None].default = "filter"
        self.lisp.device_attr['xtr1'].vrf_attr[None].disable_ttl_propagate = True
        self.lisp.device_attr['xtr1'].vrf_attr[None].locator = "FOO"
        self.lisp.device_attr['xtr1'].vrf_attr[None].locator_down = "2001:db8::1"
        self.lisp.device_attr['xtr1'].vrf_attr[None].map_request = "FOO"
        cfgs = self.lisp.build_config(devices=['xtr1'], apply=False)
        #print(cfgs)
        self.assertMultiLineDictEqual(cfgs,
                                      {self.xtr1.name: '\n '.join(['router lisp ',
                                                                   'security high',
                                                                   'locator-table default',
                                                                   'control-packet mtu 1450',
                                                                   'ddt root 2001:db8::1',
                                                                   'decapsulation filter rloc source locator-set FOO',
                                                                   'default filter',
                                                                   'disable-ttl-propagate',
                                                                   'locator default-set FOO',
                                                                   'locator-down 2001:db8::1',
                                                                   'map-request itr-rlocs FOO',
                                                                   'exit'])})
        self.lisp.build_unconfig(apply=False)

    def test_locator_scope_block(self):

        self.lisp.device_attr['xtr1'].router_lisp_id = '1'
        self.lisp.device_attr['xtr1'].vrf_attr[None].locator_scope_attr['IPV4']
        self.lisp.device_attr['xtr1'].vrf_attr[None].locator_scope_attr['IPV4'].rloc_prefix = "10.1.1.0/24"
        self.lisp.device_attr['xtr1'].vrf_attr[None].locator_scope_attr['IPV4'].rtr_locator_set = "FOO"
        cfgs = self.lisp.build_config(devices=['xtr1'], apply=False)
        #print(cfgs)
        self.assertMultiLineDictEqual(cfgs,
                                      {self.xtr1.name: '\n '.join(['router lisp 1',
                                                                   'locator-scope IPV4',
                                                                   ' rloc-prefix 10.1.1.0/24',
                                                                   ' rtr-locator-set FOO',
                                                                   ' exit',
                                                                   'exit'])})

    def test_lispset_block(self):
        self.lisp.device_attr['xtr1'].router_lisp_id = '1'
        self.lisp.device_attr['xtr1'].vrf_attr[None].security = "high"
        # This initializes the locator attribute class
        self.lisp.device_attr['xtr1'].vrf_attr[None].locatorset_attr['TARDIS']
        self.lisp.device_attr['xtr1'].vrf_attr[None].locatorset_attr['TARDIS'].auto_discover_rlocs = True
        self.lisp.device_attr['xtr1'].vrf_attr[None].locatorset_attr['TARDIS'].rloc_value = "10.1.1.1 priority 1 weight 100"
        cfgs = self.lisp.build_config(devices=['xtr1'], apply=False)
        #print(cfgs)
        self.assertMultiLineDictEqual(cfgs,
                                      {self.xtr1.name: '\n'.join(['router lisp 1',
                                                                  ' security high',
                                                                  ' locator-set TARDIS',
                                                                  '  10.1.1.1 priority 1 weight 100',
                                                                  '  auto-discover-rlocs',
                                                                  '  exit',
                                                                  ' exit'])})

    def test_service_ethernet(self):

        # ethernet service config
        self.lisp.device_attr['xtr1'].router_lisp_id = '1'
        self.lisp.device_attr['xtr1'].vrf_attr[None].service_attr['ethernet']
        self.lisp.device_attr['xtr1'].vrf_attr[None].service_attr['ethernet'].encapsulation = Encapsulation('vxlan')
        self.lisp.device_attr['xtr1'].vrf_attr[None].service_attr['ethernet'].map_resolver_enabled = True
        self.lisp.device_attr['xtr1'].vrf_attr[None].service_attr['ethernet'].map_server_enabled = True
        self.lisp.device_attr['xtr1'].vrf_attr[None].service_attr['ethernet'].map_cache_limit = 4

        cfgs = self.lisp.build_config(devices=['xtr1'], apply=False)
        #pprint(cfgs)
        self.assertMultiLineDictEqual(cfgs,
                                      {self.xtr1.name: '\n'.join(['router lisp 1',
                                                                  ' service ethernet',
                                                                  '  map-resolver',
                                                                  '  map-server',
                                                                  '  encapsulation vxlan',
                                                                  '  map-cache-limit 4',
                                                                  '  exit',
                                                                  ' exit'])})

    def test_service_ipv4(self):
        #print('testing service block...')
        self.lisp.device_attr['xtr1'].router_lisp_id = '2'
        top_service_level = self.lisp.device_attr['xtr1'].vrf_attr[None].service_attr['ipv4']
        self.lisp.device_attr['xtr1'].vrf_attr[None].service_attr['ipv4']
        top_service_level.encapsulation = Encapsulation('lisp')
        top_service_level.itr_enabled = True
        top_service_level.itr_values = ["map-resolver 10.1.1.1 key cisco123"]
        top_service_level.etr_enabled = True
        top_service_level.map_request_source = '10.1.1.1'
        top_service_level.use_petr = '10.1.1.1'
        top_service_level.map_cache_persistence_interval = 100
        top_service_level.site_registrations = 100
        etr_value_list = []
        etr_value_list.append("map-server 10.1.1.1 key cisco123")
        etr_value_list.append("map-cache-limit 1234")
        etr_value_list.append("accept-map-request-mapping verify")
        top_service_level.etr_values = etr_value_list
        cfgs = self.lisp.build_config(devices=['xtr1'], apply=False)
        self.assertMultiLineDictEqual(cfgs,
                                      {self.xtr1.name: '\n'.join(['router lisp 2',
                                                                  ' service ipv4',
                                                                  '  itr',
                                                                  '  etr',
                                                                  '  encapsulation lisp',
                                                                  '  itr map-resolver 10.1.1.1 key cisco123',
                                                                  '  etr map-server 10.1.1.1 key cisco123',
                                                                  '  etr map-cache-limit 1234',
                                                                  '  etr accept-map-request-mapping verify',
                                                                  '  map-request-source 10.1.1.1',
                                                                  '  use-petr 10.1.1.1',
                                                                  '  site-registrations limit 100',
                                                                  '  map-cache-persistent interval 100',
                                                                  '  exit',
                                                                  ' exit'])})

    def test_config_with_site(self):
        #print("Testing msm config...")
        self.lisp.device_attr['xtr1'].router_lisp_id = '3'
        self.lisp.device_attr['xtr1'].vrf_attr[None].site_attr[1]
        self.lisp.device_attr['xtr1'].vrf_attr[None].site_attr[1].authentication_key = "cisco123"
        eid_records = []
        eid_records.append("anymac")
        eid_records.append("instance-id 10 192.168.1.0/24 accept-more-specific")
        eid_records.append("instance-id 1 1.1.1.1/32")
        eid_records.append("instance-id 1 2.2.2.1/32")
        self.lisp.device_attr['xtr1'].vrf_attr[None].site_attr[1].eid_records = eid_records
        cfgs = self.lisp.build_config(devices=['xtr1'], apply=False)
        #print(cfgs['xtr1'])
        self.assertMultiLineDictEqual(cfgs,
                                      {self.xtr1.name: '\n'.join(['router lisp 3',
                                                                  ' site 1',
                                                                  '  authentication-key cisco123',
                                                                  '  eid-record anymac',
                                                                  '  eid-record instance-id 10 192.168.1.0/24 accept-more-specific',
                                                                  '  eid-record instance-id 1 1.1.1.1/32',
                                                                  '  eid-record instance-id 1 2.2.2.1/32',
                                                                  '  exit',
                                                                  ' exit'])})

    def test_instance_block(self):
        #print("Testing instance block...")
        self.maxDiff = None
        self.lisp.device_attr['xtr1'].router_lisp_id = '1'
        instance_level = self.lisp.device_attr['xtr1'].vrf_attr[None].instance_attr[1]
        self.lisp.device_attr['xtr1'].vrf_attr[None].instance_attr[1]
        instance_level.service_attr['ipv4']
        instance_level.service_attr['ipv4'].itr_enabled = True
        instance_level.service_attr['ipv4'].itr_values = ["map-resolver 10.1.1.1"]
        instance_level.service_attr['ipv4'].map_request_source = '10.1.1.1'
        instance_level.service_attr['ipv4'].use_petr = '10.1.1.1'
        instance_level.service_attr['ipv4'].map_cache_persistence_interval = 100
        instance_level.service_attr['ipv4'].site_registrations = 100
        instance_level.service_attr['ipv4'].eid_table = "default"
        ipv4_db_map = []
        ipv4_db_map.append('192.168.2.0/24 locator-set RLOC_SET_1')
        ipv4_db_map.append('192.168.3.0/24 locator-set RLOC_SET 1')
        instance_level.ipv4_db_map = ipv4_db_map
        instance_level.dynamic_eid_attr['192_168_1_0'].database_mapping =\
            "192.168.1.0/24 locator-set RLOC_SET_1"
        instance_level.service_attr['ipv6']
        instance_level.service_attr['ipv6'].eid_table = "default"
        ipv6_db_map = []
        ipv6_db_map.append('database-mapping 2001:db8::/64 locator-set RLOC_SET_1')
        cfgs = self.lisp.build_config(devices=['xtr1'], apply=False)
        self.assertMultiLineDictEqual(cfgs,
                                      {self.xtr1.name: '\n'.join(['router lisp 1',
                                                                  ' instance-id 1',
                                                                  '  service ipv4',
                                                                  '   itr',
                                                                  '   itr map-resolver 10.1.1.1',
                                                                  '   eid-table default',
                                                                  '   map-request-source 10.1.1.1',
                                                                  '   use-petr 10.1.1.1',
                                                                  '   site-registrations limit 100',
                                                                  '   map-cache-persistent interval 100',
                                                                  '   database-mapping 192.168.2.0/24 locator-set RLOC_SET_1',
                                                                  '   database-mapping 192.168.3.0/24 locator-set RLOC_SET 1',
                                                                  '   exit',
                                                                  '  service ipv6',
                                                                  '   eid-table default',
                                                                  '   exit',
                                                                  '  dynamic-eid 192_168_1_0',
                                                                  '   database-mapping 192.168.1.0/24 locator-set RLOC_SET_1',
                                                                  '   exit',
                                                                  '  exit',
                                                                  ' exit'])})


if __name__ == "__main__":
    unittest.main()
