#!/usr/bin/env python

# python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# xBU-shared genie pacakge
from genie.libs.conf.interface import TunnelTeInterface
from genie.libs.conf.base import MAC, IPv4Interface, IPv6Interface, IPv4Address, IPv6Address
from genie.libs.conf.interface import Layer, L2_type, IPv4Addr, IPv6Addr,NveInterface
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface.nxos import Interface

class test_interface(TestCase):

    def test_vxlan_interface(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        intf1 = Interface(name='Ethernet0/0/1',device=dev1)

        # Defining attributes section
        intf1.evpn_multisite_fabric_tracking = True
        intf1.evpn_multisite_dci_tracking = True
        intf1.fabric_forwarding_mode = 'anycast-gateway'
        intf1.ip_forward = True
        intf1.ipv6_addr_use_link_local_only = True

        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' evpn multisite dci-tracking',
                ' evpn multisite fabric-tracking',
                ' fabric forwarding mode anycast-gateway',
                ' ip forward',
                ' ipv6 address use-link-local-only',
                ' exit',
            ]))

        partial_uncfg = intf1.build_unconfig(apply=False,attributes={"evpn_multisite_fabric_tracking":True,
                                                                     "evpn_multisite_dci_tracking": True,
                                                                     "ip_forward":True})
        self.assertMultiLineEqual(str(partial_uncfg), '\n'.join([
            'interface Ethernet0/0/1',
            ' no evpn multisite dci-tracking',
            ' no evpn multisite fabric-tracking',
            ' no ip forward',
            ' exit',
        ]))

    def test_EthernetInterface(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        dev2 = Device(testbed=testbed, name='P1', os='nxos')
        intf1 = Interface(name='Ethernet0/0/1',device=dev1)
        intf2 = Interface(name='Ethernet0/0/2',device=dev2)

        # Defining attributes section
        intf1.ipv4 = '201.0.12.1'
        intf1.ipv4.netmask = '255.255.255.0'
        intf1.speed = 1000
        intf1.shutdown = False
        # make intf1 as L3 interface
        intf1.switchport_enable = False
        intf1.mtu = 500
        intf1.ipv6 = '2001::12:1'

        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' mtu 500',
                ' no shutdown',
                ' no switchport',
                ' ip address 201.0.12.1 255.255.255.0',
                ' ipv6 address 2001::12:1/128',
                ' speed 1000',
                ' exit',
            ]))

        uncfg = intf1.build_unconfig(apply=False, attributes={'ipv6': True,
                                                              'ipv4': True})
        self.assertMultiLineEqual(
            str(uncfg),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' no ip address',
                ' no ipv6 address',
                ' exit',
            ]))

        partial_uncfg = intf1.build_unconfig(apply=False,attributes="mtu")
        self.assertMultiLineEqual(str(partial_uncfg), '\n'.join([
            'interface Ethernet0/0/1',
            ' no mtu',
            ' exit',
        ]))

        # make intf2 as L2 interface
        intf2.switchport_enable = True
        intf2.switchport_mode = L2_type.TRUNK
        intf2.sw_trunk_allowed_vlan = '200-201'

        cfg2 = intf2.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg2),
            '\n'.join([
                'interface Ethernet0/0/2',
                ' switchport',
                ' switchport mode trunk',
                ' switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

class test_nx_interface(TestCase):

    def test_nve_interface_simple(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        # Apply configuration
        intf1.enabled = False

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface nve1',
                ' shutdown',
                ' exit'
            ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'enabled': {False: None}})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no shutdown',
                ' exit'
            ]))

    def test_nve_interface(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        # Apply configuration
        intf1.nve_host_reachability_protocol = NveInterface.HOST_REACHABILTY_PROTOCOL.bgp
        intf1.nve_adv_virtual_rmac = True
        intf1.nve_src_intf_loopback = 'loopback1'
        intf1.nve_multisite_bgw_intf = 'loopback100'

        intf1.nve_vni = 4096
        intf1.nve_vni_associate_vrf = True
        intf1.nve_vni_suppress_arp = True
        intf1.nve_vni_multisite_ingress_replication = True
        intf1.nve_vni_mcast_group = '233.1.1.1'

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' advertise virtual-rmac',
                ' source-interface loopback1',
                ' multisite border-gateway interface loopback100',
                ' member vni 4096 associate-vrf',
                '  suppress-arp',
                '  multisite ingress-replication',
                '  mcast-group 233.1.1.1',
                '  exit',
                ' exit'
            ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'nve_vni': '4096'})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no member vni 4096',
                ' exit'
            ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'nve_host_reachability_protocol':
                                                                   NveInterface.HOST_REACHABILTY_PROTOCOL.bgp,
                                                               'nve_vni': '4096',
                                                               'nve_vni_suppress_arp': True})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no host-reachability protocol bgp',
                ' member vni 4096',
                '  no suppress-arp',
                '  exit',
                ' exit'
            ]))

    def test_nve_interface_mcast(self):

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_adv_virtual_rmac = True
        intf1.nve_src_intf_loopback = 'loopback1'
        intf1.nve_multisite_bgw_intf = 'loopback100'
        vnis_map= {}
        nve_vni_map = {}
        vnis_map['nve_vni_associate_vrf'] = True
        vnis_map['nve_vni_suppress_arp'] = False
        vnis_map['nve_vni_multisite_ingress_replication_optimized'] = True
        vnis_map['nve_vni_mcast_group'] = '233.1.1.1'
        vnis_map['nve_vni'] = '1001-1100'
        nve_vni_map['1001-1100'] = vnis_map
        intf1.vni_map = nve_vni_map
        intf1.nve_src_intf_holddown = 30
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_ir_proto = 'bgp'
        intf1.nve_global_mcast_group_l3 = '229.0.0.1'

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' global suppress-arp',
                ' global ingress-replication protocol bgp',
                ' global mcast-group 229.0.0.1 L3',
                ' advertise virtual-rmac',
                ' source-interface loopback1',
                ' source-interface hold-down-time 30',
                ' multisite border-gateway interface loopback100',
                ' member vni 1001-1100 associate-vrf',
                '  multisite ingress-replication optimized',
                '  mcast-group 233.1.1.1',
                '  exit',
                ' exit'
            ]))


        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)
        vni_map = {}
        vnis_map = {}
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map

        intf1.vni_map = vni_map

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes = {'vni_map': vnis_map})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no member vni 1001-1100',
                ' exit'
            ]))

        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)
        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_adv_virtual_rmac = True
        intf1.nve_src_intf_loopback = 'loopback1'
        intf1.nve_multisite_bgw_intf = 'loopback100'
        vnis_map = {}
        vni_map = {}
        vnis_map['nve_vni_multisite_ingress_replication_optimized'] = True
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map
        intf1.vni_map = vni_map
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_ir_proto = 'bgp'
        intf1.nve_global_mcast_group_l3 = '229.0.0.1'
        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes= {
                                                                'nve_host_reachability_protocol': 'bgp' ,
                                                                'nve_global_mcast_group_l3': intf1.nve_global_mcast_group_l3 ,
                                                                'nve_global_suppress_arp' : True,
                                                                 'vni_map': vnis_map })



        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no host-reachability protocol bgp',
                ' no global suppress-arp',
                ' no global mcast-group L3',
                ' member vni 1001-1100',
                '  no multisite ingress-replication optimized',
                '  exit',
                ' exit'
            ]))

    # Below function is for L3VNI when Fabric underlay is
    # ASM and DCI underlay is also ASM
    def test_nve_interface_msite_mcast_underlay_l3vni(self):

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_adv_virtual_rmac = True
        intf1.nve_src_intf_loopback = 'loopback1'
        intf1.nve_multisite_bgw_intf = 'loopback100'
        vnis_map= {}
        nve_vni_map = {}
        vnis_map['nve_vni_associate_vrf'] = True
        vnis_map['nve_vni_suppress_arp'] = False
        vnis_map['nve_vni_mcast_group'] = '226.1.1.1'
        vnis_map['nve_vni_multisite_mcast_group'] = '239.1.1.1'
        vnis_map['nve_vni'] = '1001-1100'
        nve_vni_map['1001-1100'] = vnis_map
        intf1.vni_map = nve_vni_map
        intf1.nve_src_intf_holddown = 30
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_ir_proto = 'bgp'
        intf1.nve_global_mcast_group_l3 = '229.0.0.1'

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' global suppress-arp',
                ' global ingress-replication protocol bgp',
                ' global mcast-group 229.0.0.1 L3',
                ' advertise virtual-rmac',
                ' source-interface loopback1',
                ' source-interface hold-down-time 30',
                ' multisite border-gateway interface loopback100',
                ' member vni 1001-1100 associate-vrf',
                '  mcast-group 226.1.1.1',
                '  multisite mcast-group 239.1.1.1',
                '  exit',
                ' exit'
            ]))


        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)
        vni_map = {}
        vnis_map = {}
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map

        intf1.vni_map = vni_map

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes = {'vni_map': vnis_map})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no member vni 1001-1100',
                ' exit'
            ]))

        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)
        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_adv_virtual_rmac = True
        intf1.nve_src_intf_loopback = 'loopback1'
        intf1.nve_multisite_bgw_intf = 'loopback100'
        vnis_map = {}
        vni_map = {}
        vnis_map['nve_vni_multisite_mcast_group'] = '239.1.1.1'
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map
        intf1.vni_map = vni_map
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_ir_proto = 'bgp'
        intf1.nve_global_mcast_group_l3 = '229.0.0.1'
        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes= {
                                                                'nve_host_reachability_protocol': 'bgp' ,
                                                                'nve_global_mcast_group_l3': intf1.nve_global_mcast_group_l3 ,
                                                                'nve_global_suppress_arp' : True,
                                                                 'vni_map': vnis_map })



        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no host-reachability protocol bgp',
                ' no global suppress-arp',
                ' no global mcast-group L3',
                ' member vni 1001-1100',
                '  no multisite mcast-group',
                '  exit',
                ' exit'
            ]))

    def test_nve_interface_ir(self):

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_adv_virtual_rmac = True
        intf1.nve_src_intf_loopback = 'loopback1'
        intf1.nve_multisite_bgw_intf = 'loopback100'
        vni_map= {}
        vnis_map = {}
        vnis_map['nve_vni_suppress_arp'] = False
        vnis_map['nve_vni_ir'] = True
        vnis_map['nve_vni_multisite_ingress_replication'] = True
        vnis_map['nve_vni_ir_proto'] =  'bgp'
        vnis_map['nve_vni_suppress_arp'] = True
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map
        intf1.vni_map = vni_map
        intf1.nve_src_intf_holddown = 30
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_ir_proto = 'bgp'
        intf1.nve_global_mcast_group_l2 = '229.0.0.1'




        # Build config

        cfgs = intf1.build_config(apply=False, attributes = {
                                                            'nve_host_reachability_protocol': 'bgp',
                                                            'nve_global_suppress_arp': True,
                                                            'nve_global_ir_proto' : 'bgp',
                                                            'nve_global_mcast_group_l2': intf1.nve_global_mcast_group_l2 ,
                                                            'nve_adv_virtual_rmac' : True,
                                                            'nve_src_intf_loopback': 'loopback1',
                                                            'nve_src_intf_holddown': 30,
                                                            'nve_multisite_bgw_intf': 'loopback100',
                                                            'vni_map':vnis_map})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' global suppress-arp',
                ' global ingress-replication protocol bgp',
                ' global mcast-group 229.0.0.1 L2',
                ' advertise virtual-rmac',
                ' source-interface loopback1',
                ' source-interface hold-down-time 30',
                ' multisite border-gateway interface loopback100',
                ' member vni 1001-1100',
                '  suppress-arp',
                '  ingress-replication protocol bgp',
                '  multisite ingress-replication',
                '  exit',
                ' exit'
            ]))

        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        vnis_map = {}
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map
        intf1.vni_map = vni_map
        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False,attributes = {'vni_map': vni_map})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no member vni 1001-1100',
                ' exit'
            ]))
        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_mcast_group_l2 = '229.0.0.1'
        intf1.nve_src_intf_holddown = 30
        vni_map= {}
        vnis_map = {}
        vni_map['nve_vni_multisite_ingress_replication'] = True
        vni_map['nve_vni_ir'] = True
        vni_map['nve_vni_ir_proto'] = 'bgp'
        vni_map['nve_vni_suppress_arp'] = True
        vni_map['nve_vni'] = '1001-1100'
        vnis_map['1001-1100'] = vni_map
        intf1.vni_map = vnis_map
       #uncfgs = intf1.build_unconfig(apply=False)

        # Build unconfig
        # uncfgs = intf1.build_unconfig(apply=False)
        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'nve_host_reachability_protocol': 'bgp',
                                                                'nve_src_intf_holddown': 30,
                                                               'global_suppress_arp': True,
                                                               'nve_global_mcast_group_l2': '229.0.0.1',
                                                                'vni_map': vnis_map})


        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                 'interface nve1',
                 ' no host-reachability protocol bgp',
                 ' no global mcast-group L2',
                 ' no source-interface hold-down-time 30',
                 ' member vni 1001-1100',
                 '  no suppress-arp',
                 '  no ingress-replication protocol bgp',
                 '  no multisite ingress-replication',
                 '  exit',
                 ' exit'
            ]))

    # Below function is for L2VNI when Fabric underlay is
    # ASM and DCI underlay is also ASM
    def test_nve_interface_msite_mcast_underlay_l2vni(self):

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_adv_virtual_rmac = True
        intf1.nve_src_intf_loopback = 'loopback1'
        intf1.nve_multisite_bgw_intf = 'loopback100'
        vni_map= {}
        vnis_map = {}
        vnis_map['nve_vni_suppress_arp'] = False
        vnis_map['nve_vni_mcast_group'] = '225.1.1.1'
        vnis_map['nve_vni_multisite_mcast_group'] = '238.1.1.1'
        vnis_map['nve_vni_suppress_arp'] = True
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map
        intf1.vni_map = vni_map
        intf1.nve_src_intf_holddown = 30
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_ir_proto = 'bgp'
        intf1.nve_global_mcast_group_l2 = '229.0.0.1'




        # Build config

        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' global suppress-arp',
                ' global ingress-replication protocol bgp',
                ' global mcast-group 229.0.0.1 L2',
                ' advertise virtual-rmac',
                ' source-interface loopback1',
                ' source-interface hold-down-time 30',
                ' multisite border-gateway interface loopback100',
                ' member vni 1001-1100',
                '  suppress-arp',
                '  mcast-group 225.1.1.1',
                '  multisite mcast-group 238.1.1.1',
                '  exit',
                ' exit'
            ]))

        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(name='nve1', device=dev1)

        vnis_map = {}
        vnis_map['nve_vni'] = '1001-1100'
        vni_map['1001-1100'] = vnis_map
        intf1.vni_map = vni_map
        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False,attributes = {'vni_map': vni_map})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve1',
                ' no member vni 1001-1100',
                ' exit'
            ]))
        # Apply configuration
        intf1.nve_host_reachability_protocol = 'bgp'
        intf1.nve_global_suppress_arp = True
        intf1.nve_global_mcast_group_l2 = '229.0.0.1'
        intf1.nve_src_intf_holddown = 30
        vni_map= {}
        vnis_map = {}
        vni_map['nve_vni_multisite_mcast_group'] = '238.1.1.1'
        vni_map['nve_vni_suppress_arp'] = True
        vni_map['nve_vni'] = '1001-1100'
        vnis_map['1001-1100'] = vni_map
        intf1.vni_map = vnis_map

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'nve_host_reachability_protocol': 'bgp',
                                                               'nve_src_intf_holddown': 30,
                                                               'global_suppress_arp': True,
                                                               'nve_global_mcast_group_l2': '229.0.0.1',
                                                                'vni_map': vnis_map})


        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                 'interface nve1',
                 ' no host-reachability protocol bgp',
                 ' no global mcast-group L2',
                 ' no source-interface hold-down-time 30',
                 ' member vni 1001-1100',
                 '  no suppress-arp',
                 '  no multisite mcast-group',
                 '  exit',
                 ' exit'
            ]))



    def test_single_line_config(self):
        
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='Ethernet3/7', device=dev1, aliases=['PE1_1'])
        intf2 = Interface(name='Ethernet3/9', device=dev1, aliases=['PE1_2'])
        subif1 = Interface(name='Ethernet3/6.10', device=dev1, aliases=['PE1_1'])
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # Apply configuration
        intf1.description = 'test'
        intf1.enabled = False
        # intf1.shutdown = False
        intf1.link_up_down_trap_enable = True
        intf1.mtu = 1492
        intf1.vrf = vrf
        intf1.mac_address = 'aabb.ccdd.eeff'
        intf1.bandwidth = 8192
        intf1.link_status = True
        intf1.load_interval = 33
        intf1.dhcp = True
        intf1.unnumbered_intf_ref = 'Ethernet3/6.10'
        intf1.ipv6_autoconf = True
        intf1.switchport_mode = 'access'
        intf1.medium = 'p2p'
        intf1.delay = 11
        intf1.access_vlan = '19'
        intf1.auto_negotiate = False
        # make intf2 as L2 interface
        intf1.switchport_enable = True

        intf2.enabled = True
        intf2.switchport_enable = True
        intf2.switchport_mode = 'trunk'
        intf2.trunk_add_vlans = '1,2,3'

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet3/7',
                ' medium p2p',
                ' bandwidth 8192',
                ' delay 11',
                ' description test',
                ' mtu 1492',
                ' shutdown',
                ' snmp trap link-status',
                ' vrf member test',
                ' logging event port link-status',
                ' ip address dhcp',
                ' ip unnumbered Ethernet3/6.10',
                ' ipv6 address autoconfig',
                ' switchport',
                ' switchport mode access',
                ' load-interval 33',
                ' mac-address aabb.ccdd.eeff',
                ' switchport access vlan 19',
                ' no speed',
                ' no duplex',
                ' exit'
                ]))

        cfgs = intf2.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet3/9',
                ' no shutdown',
                ' switchport',
                ' switchport mode trunk',
                ' switchport trunk allowed vlan add 1,2,3',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'mtu': True, 'enabled':True})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface Ethernet3/7',
                ' no mtu',
                ' no shutdown',
                ' exit'
                ]))

        uncfgs = intf2.build_unconfig(apply=False, attributes={'trunk_add_vlans': True})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface Ethernet3/9',
                ' switchport trunk allowed vlan remove 1,2,3',
                ' exit'
                ]))

    def test_ipv4_multiple_lines_confg(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='Ethernet3/7', device=dev1, \
            aliases=['PE1_1'])
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # Apply configuration
        intf1.description = 'multiple lines config'

        ipv4a = IPv4Addr(device=dev1)
        ipv4a.ipv4 = IPv4Address('192.168.1.1')
        ipv4a.prefix_length = '24'
        intf1.add_ipv4addr(ipv4a)
        ipv4b = IPv4Addr(device=dev1)
        ipv4b.ipv4 = IPv4Address('192.168.1.2')
        ipv4b.prefix_length = '24'
        ipv4b.ipv4_secondary = True
        ipv4b.redirect = False
        intf1.add_ipv4addr(ipv4b)
        intf1.shutdown = False
        # make intf2 as L3 interface
        intf1.switchport_enable = False

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet3/7',
                ' description multiple lines config',
                ' no shutdown',
                ' no switchport',
                ' ip address 192.168.1.1/24',
                ' no ip redirects',
                ' ip address 192.168.1.2/24 secondary',
                ' no ip redirects',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'switchport_enable': True,
                                                               'description': True,
                                                               'shutdown': True})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface Ethernet3/7',
                ' no description',
                ' shutdown',
                ' switchport',
                ' exit'
                ]))        

    def test_ipv6_multiple_lines_confg(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='Ethernet3/7', device=dev1, \
            aliases=['PE1_1'])
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # Apply configuration
        intf1.description = 'multiple lines config'

        ipv6a = IPv6Addr(device=dev1)
        ipv6a.ipv6 = IPv6Address('2001:db1:1::1')
        ipv6a.ipv6_prefix_length = '64'
        intf1.add_ipv6addr(ipv6a)
        ipv6b = IPv6Addr(device=dev1)
        ipv6b.ipv6 = IPv6Address('2001:db1:2::2')
        ipv6b.ipv6_prefix_length = '64'
        ipv6b.redirect = False
        intf1.add_ipv6addr(ipv6b)
        intf1.shutdown = False
        # make intf2 as L3 interface
        intf1.switchport_enable = False

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet3/7',
                ' description multiple lines config',
                ' no shutdown',
                ' no switchport',
                ' ipv6 address 2001:db1:1::1/64',
                ' no ipv6 redirects',
                ' ipv6 address 2001:db1:2::2/64',
                ' no ipv6 redirects',
                ' exit'
                ]))        

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'default interface Ethernet3/7',
                ]))

    def test_uncfg_interface(self):
        
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='Ethernet3/7', device=dev1)
        intf2 = Interface(name='Vlan100', device=dev1)
        # vrf = Vrf(name='test', testbed=testbed)
        # dev1.add_feature(vrf)
        # make intf2 as L2 interface
        intf2.mtu = 500
        intf1.mtu = 500
        intf2.fabric_forwarding_mode = 'anycast-gateway'

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet3/7',
                ' mtu 500',
                ' exit'
                ]))
        cfgs = intf2.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Vlan100',
                ' mtu 500',
                ' fabric forwarding mode anycast-gateway',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'default interface Ethernet3/7',
                ]))
        uncfgs = intf2.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'no interface Vlan100',
                ]))

    def test_switchport_enable_config(self):
        
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='Ethernet3/7', device=dev1, aliases=['PE1_1'])
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # make intf2 as L2 interface
        intf1.switchport_enable = True

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet3/7',
                ' switchport',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'default interface Ethernet3/7',
                ]))

    def test_port_channel_interface(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='port-channel10', device=dev1)

        # Apply configuration
        intf1.channel_group_mode = 'on'
        intf1.switchport_enable = False         
        intf1.ipv4 = '11.0.1.1/24'
        intf1.shutdown = False
        intf1.switchport_enable = False
        intf1.mtu = 9111
        uut1_int3 = Interface(name='Ethernet0/0/1',device=dev1)
        intf1.add_member(uut1_int3)

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' channel-group 10 mode on',
                ' exit',
                'interface port-channel10',
                ' mtu 9111',
                ' no shutdown',
                ' no switchport',
                ' ip address 11.0.1.1 255.255.255.0',
                ' exit'
                ]))        

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' no channel-group 10 mode on',
                ' exit',
                'no interface port-channel10'
                ]))

    def test_port_channel_interface_l2(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='port-channel10', device=dev1)

        # Apply configuration
        intf1.channel_group_mode = 'active'
        intf1.enabled = True
        intf1.switchport_enable = True
        intf1.switchport_mode = "access"
        intf1.access_vlan = '10'

        uut1_int3 = Interface(name='Ethernet0/0/1',device=dev1)
        intf1.add_member(uut1_int3)

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' channel-group 10 mode active',
                ' exit',
                'interface port-channel10',
                ' no shutdown',
                ' switchport',
                ' switchport mode access',
                ' switchport access vlan 10',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' no channel-group 10 mode active',
                ' exit',
                'no interface port-channel10'
                ]))

    def test_port_channel_interface_trunk_vlans(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        intf1 = Interface(name='port-channel10', device=dev1)

        # Apply configuration
        intf1.channel_group_mode = 'active'
        intf1.enabled = True
        intf1.switchport_enable = True
        intf1.switchport_mode = 'trunk'
        intf1.trunk_vlans = "2-5,11-105,111-205"

        uut1_int3 = Interface(name='Ethernet0/0/1',device=dev1)
        intf1.add_member(uut1_int3)

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' channel-group 10 mode active',
                ' exit',
                'interface port-channel10',
                ' no shutdown',
                ' switchport',
                ' switchport mode trunk',
                ' switchport trunk allowed vlan 2-5,11-105,111-205',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' no channel-group 10 mode active',
                ' exit',
                'no interface port-channel10'
                ]))


    def test_native_vlans(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
         # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(
                    name='Ethernet2/22', 
                    device=dev1,
                    description='Native vlan testing',
                    enabled=True,
                    switchport_mode='trunk',
                    trunk_vlans='101-120,131-140,151-170,200-209',
                    native_vlan='1',
                    switchport_enable=True
                    )

        # Build config
        cfgs = intf1.build_config(apply=False)

        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet2/22',
                ' description Native vlan testing',
                ' no shutdown',
                ' switchport',
                ' switchport mode trunk',
                ' switchport trunk allowed vlan 101-120,131-140,151-170,200-209',
                ' switchport trunk native vlan 1',
                ' exit'
            ]))

    def test_dot1q_tunnel_interface(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='BL1', testbed=testbed, os='nxos')
        intf1 = Interface(
            name='Ethernet2/22',
            device=dev1,
            description='dot1q tunnel testing',
            enabled=True,
            switchport_mode='dot1q-tunnel',
            dot1q_access_vlan='1301',
            switchport_enable=True
        )

        # Build config
        cfgs = intf1.build_config(apply=False)

        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet2/22',
                ' description dot1q tunnel testing',
                ' no shutdown',
                ' switchport',
                ' switchport mode dot1q-tunnel',
                ' switchport access vlan 1301',
                ' exit'
            ]))
            
if __name__ == '__main__':
    unittest.main()

