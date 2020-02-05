#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie Conf
from genie.libs.conf.interface import Interface
from genie.libs.conf.lisp import Lisp


class test_lisp(TestCase):

    def test_lisp_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create Interface object
        intf1 = Interface(name='GigabitEthernet1', device=dev1)

        # Create LISP object
        lisp1 = Lisp()

        # DeviceAttributes
        #   InterfaceAttributes
        lisp1.device_attr[dev1].intf_attr[intf1].if_mobility_liveness_test_disabled = True

        # DeviceAttributes
        #   InterfaceAttributes
        #     MobilityDynamicEidAttributes
        lisp1.device_attr[dev1].intf_attr[intf1].mobility_dynamic_eid_attr['wired']
        lisp1.device_attr[dev1].intf_attr[intf1].mobility_dynamic_eid_attr['wired_v6']

        # DeviceAttributes
        #   RouterInstanceAttributes
        lisp1.device_attr[dev1].router_instance_attr[0]

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     LocatorSetAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC1']
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC2']
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC3']

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     LocatorSetAttributes
        #       InterfaceAttributes
        #         InterfaceTypeAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC1'].locator_set_intf_attr['Loopback1'].locator_set_intf_type_attr['ipv4'].ls_priority = 10
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC1'].locator_set_intf_attr['Loopback1'].locator_set_intf_type_attr['ipv4'].ls_weight = 30
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC2'].locator_set_intf_attr['Loopback2'].locator_set_intf_type_attr['ipv4']
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC2'].locator_set_intf_attr['Loopback3'].locator_set_intf_type_attr['ipv4']
        lisp1.device_attr[dev1].router_instance_attr[0].locator_set_attr['RLOC2'].locator_set_intf_attr['Loopback4'].locator_set_intf_type_attr['ipv6']

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     ServiceAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].itr_enabled = True
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].etr_enabled = True
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].proxy_etr_enabled = True
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].ms_enabled = True
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].mr_enabled = True
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].encapsulation = 'vxlan'

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     ServiceAttributes
        #       ItrMrAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].itr_mr_attr['4.4.4.4']
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].itr_mr_attr['13.13.13.13']
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].itr_mr_attr['16.16.16.16']

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     ServiceAttributes
        #       EtrMsAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].etr_ms_attr['4.4.4.4'].etr_auth_key = 'cisco123'
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].etr_ms_attr['4.4.4.4'].etr_proxy_reply = True
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].etr_ms_attr['5.5.5.5'].etr_auth_key = 'roZes123'
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv4'].etr_ms_attr['5.5.5.5'].etr_auth_key_type = 'hmac-sha-1-96'
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].etr_ms_attr['6.6.6.6'].etr_auth_key = 'test123'
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].etr_ms_attr['6.6.6.6'].etr_auth_key_type = 'hmac-sha-256-128'

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     ServiceAttributes
        #       ProxyItrAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].proxy_attr['10.10.10.10']
        lisp1.device_attr[dev1].router_instance_attr[0].service_attr['ipv6'].proxy_attr['20.20.20.20']

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     InstanceAttributes
        #       DynamicEidAttributes
        #         DbMappingAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].dynamic_eid_attr['192'].db_mapping_attr['172.168.0.0/24']
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].dynamic_eid_attr['192'].db_mapping_attr['192.168.0.0/24'].etr_dyn_eid_rlocs = 'RLOC'

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     InstanceAttributes
        #       ServiceAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv4']
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].etr_eid_vrf = 'red'

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     InstanceAttributes
        #       ServiceAttributes
        #         DbMappingAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv4'].service_db_mapping_attr['172.168.0.0/24']
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].service_db_mapping_attr['192.168.0.0/24'].etr_eid_rlocs = 'RLOC2'

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     InstanceAttributes
        #       ServiceAttributes
        #         UsePetrAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv4'].use_petr_attr['15.15.15.15'].etr_use_petr_priority = 10
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv4'].use_petr_attr['15.15.15.15'].etr_use_petr_weight = 20
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv4'].use_petr_attr['16.16.16.16'].etr_use_petr_priority = 20
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv4'].use_petr_attr['16.16.16.16'].etr_use_petr_weight = 50
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].use_petr_attr['22.22.22.22'].etr_use_petr_priority = 20
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].use_petr_attr['22.22.22.22'].etr_use_petr_weight = 30
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].use_petr_attr['13.13.13.13'].etr_use_petr_priority = 30
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].use_petr_attr['13.13.13.13'].etr_use_petr_weight = 60

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     InstanceAttributes
        #       ServiceAttributes
        #         MapCacheAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv4'].map_cache_attr['10.1.1.0/24']
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].map_cache_attr['12.1.1.0/24']
        lisp1.device_attr[dev1].router_instance_attr[0].instance_id_attr['101'].inst_service_attr['ipv6'].map_cache_attr['20.1.1.0/24'].itr_mc_map_request = True

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     SiteAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].site_attr['xtr1']
        lisp1.device_attr[dev1].router_instance_attr[0].site_attr['xtr2'].ms_site_auth_key = 'cisco123'

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     SiteAttributes
        #       InstanceIdAttributes
        #         EidRecordAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].site_attr['xtr1'].site_inst_id_attr['101'].eid_record_attr['88.88.88.0/24']
        lisp1.device_attr[dev1].router_instance_attr[0].site_attr['xtr1'].site_inst_id_attr['102'].eid_record_attr['89.89.89.0/24'].ms_eid_accept_more_specifics = True

        # DeviceAttributes
        #   RouterInstanceAttributes
        #     ExtranetAttributes
        lisp1.device_attr[dev1].router_instance_attr[0].extranet_attr['ext1'].extranet_inst_id_attr['101'].eid_record_provider_attr['5.5.5.0/24'].ms_extranet_provider_bidir = True
        lisp1.device_attr[dev1].router_instance_attr[0].extranet_attr['ext1'].extranet_inst_id_attr['101'].eid_record_subscriber_attr['6.6.6.0/24'].ms_extranet_subscriber_bidir = True
        lisp1.device_attr[dev1].router_instance_attr[0].extranet_attr['ext2'].extranet_inst_id_attr['102'].eid_record_subscriber_attr['7.7.7.0/24']
        lisp1.device_attr[dev1].router_instance_attr[0].extranet_attr['ext2'].extranet_inst_id_attr['102'].eid_record_subscriber_attr['8.8.8.0/24'].ms_extranet_subscriber_bidir = True

        # Add LISP to the device
        dev1.add_feature(lisp1)

        # Build config
        cfgs = lisp1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1',
                ' no lisp mobility liveness test',
                ' lisp mobility wired',
                ' lisp mobility wired_v6',
                ' exit',
                'router lisp 0',
                ' locator-set RLOC1',
                '  IPv4-interface Loopback1 priority 10 weight 30',
                '  exit',
                ' locator-set RLOC2',
                '  IPv4-interface Loopback2',
                '  IPv4-interface Loopback3',
                '  IPv6-interface Loopback4',
                '  exit',
                ' locator-set RLOC3',
                '  exit',
                ' service ipv4',
                '  itr',
                '  etr',
                '  proxy-etr',
                '  encapsulation lisp',
                '  itr map-resolver 13.13.13.13',
                '  itr map-resolver 16.16.16.16',
                '  itr map-resolver 4.4.4.4',
                '  etr map-resolver 5.5.5.5 key roZes123 hash-function sha1',
                '  exit',
                ' service ipv6',
                '  map-server',
                '  map-resolver',
                '  encapsulation vxlan',
                '  etr map-resolver 4.4.4.4 key cisco123',
                '  etr map-resolver 4.4.4.4 proxy-reply',
                '  etr map-resolver 6.6.6.6 key test123 hash-function sha2',
                '  proxy-itr 10.10.10.10',
                '  proxy-itr 20.20.20.20',
                '  exit',
                ' instance-id 101',
                '  dynamic-eid 192',
                '   datbase-mapping 172.168.0.0/24',
                '   datbase-mapping 192.168.0.0/24 locator-set RLOC',
                '   exit',
                '  service ipv4',
                '   eid-table default',
                '   datbase-mapping 172.168.0.0/24',
                '   use-petr 15.15.15.15 instance-id 101 priority 10 weight 20',
                '   use-petr 16.16.16.16 instance-id 101 priority 20 weight 50',
                '   map-cache 10.1.1.0/24',
                '   exit',
                '  service ipv6',
                '   eid-table vrf red',
                '   datbase-mapping 192.168.0.0/24 locator-set RLOC2',
                '   use-petr 13.13.13.13 instance-id 101 priority 30 weight 60',
                '   use-petr 22.22.22.22 instance-id 101 priority 20 weight 30',
                '   map-cache 12.1.1.0/24',
                '   map-cache 20.1.1.0/24 map-request',
                '   exit',
                '  exit',
                ' site xtr1',
                '  eid-record instance-id 101 88.88.88.0/24',
                '  eid-record instance-id 102 89.89.89.0/24 accept-more-specifics',
                '  exit',
                ' site xtr2',
                '  authentication-key cisco123',
                '  exit',
                ' extranet ext1',
                '  eid-record-provider instance-id 101 5.5.5.0/24 bidirectional',
                '  eid-record-subscriber instance-id 101 6.6.6.0/24 bidirectional',
                '  exit',
                ' extranet ext2',
                '  eid-record-subscriber instance-id 102 7.7.7.0/24',
                '  eid-record-subscriber instance-id 102 8.8.8.0/24 bidirectional',
                '  exit',
                ' exit',
            ]))

        # Unconfig
        lisp_uncfg = lisp1.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(lisp_uncfg[dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1',
                ' lisp mobility liveness test',
                ' no lisp mobility wired',
                ' no lisp mobility wired_v6',
                ' exit',
                'no router lisp 0',
            ]))

    def test_lisp_partial_unconfig(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create Interface object
        intf1 = Interface(name='GigabitEthernet2', device=dev1)

        # Create LISP object
        lisp1 = Lisp()

        # DeviceAttributes
        #   InterfaceAttributes
        lisp1.device_attr[dev1].intf_attr[intf1].if_mobility_liveness_test_disabled = True


        # Add LISP to the device
        dev1.add_feature(lisp1)

        # Build config
        cfgs = lisp1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'interface GigabitEthernet2',
                ' no lisp mobility liveness test',
                ' exit',
            ]))

        # Unconfig a specific attribute
        attr_unconfig = lisp1.build_unconfig(apply=False, attributes={
            'device_attr': {
                dev1.name: {
                    'intf_attr': {
                        intf1.name: {
                            'if_mobility_liveness_test_disabled': None
                        },
                    },
                },
            }})

        # Check unconfig string for attribute is built correctly
        self.assertMultiLineEqual(
            str(attr_unconfig[dev1.name]),
            '\n'.join([
                'interface GigabitEthernet2',
                ' lisp mobility liveness test',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()

