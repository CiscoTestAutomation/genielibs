#!/usr/bin/env python

import unittest
from unittest.mock import Mock
import re

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.ldp import Ldp
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.access_list import AccessList
from genie.libs.conf.base.neighbor import IPv4LsrNeighbor, IPv6Neighbor, IPLsrNeighborSubAttributes



class test_ldp(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        tb = Genie.testbed = Testbed()
        self.dev1 = Device(testbed=tb, name='PE1', os='iosxr')
        self.dev2 = Device(testbed=tb, name='PE2', os='iosxr')
        self.i1 = Interface(name='GigabitEthernet0/0/0/1', device=self.dev1)
        self.i2 = Interface(name='GigabitEthernet0/0/0/2', device=self.dev2)
        self.i3 = Interface(name='GigabitEthernet0/0/0/3', device=self.dev1)
        self.i4 = Interface(name='GigabitEthernet0/0/0/4', device=self.dev2)
        self.i5 = Interface(name='GigabitEthernet0/0/0/5', device=self.dev1)
        self.i6 = Interface(name='GigabitEthernet0/0/0/6', device=self.dev2)
        self.i7 = Interface(name='GigabitEthernet0/0/0/7', device=self.dev1)
        self.i8 = Interface(name='GigabitEthernet0/0/0/8', device=self.dev2)
        self.link = Link(name='1_2_1')
        self.link.connect_interface(interface=self.i1)
        self.link.connect_interface(interface=self.i2)
        self.link2 = Link(name='1_2_2')
        self.link2.connect_interface(interface=self.i3)
        self.link2.connect_interface(interface=self.i4)
        self.link3 = Link(name='1_2_3')
        self.link3.connect_interface(interface=self.i5)
        self.link3.connect_interface(interface=self.i6)
        self.link4 = Link(name='1_2_4')
        self.link4.connect_interface(interface=self.i7)
        self.link4.connect_interface(interface=self.i8)
        self.assertSetEqual(
            set(self.link.find_interfaces()),
            set([self.i1, self.i2]))
        self.assertSetEqual(
            set(self.dev1.find_interfaces()),
            set([self.i1, self.i3, self.i5, self.i7]))
        self.assertSetEqual(
            set(self.dev2.find_interfaces()),
            set([self.i2, self.i4, self.i6, self.i8]))

    def test_01_interface_only(self):

        ldp = Ldp()
        self.assertSetEqual(set(ldp.devices), set([]))
        self.assertSetEqual(set(ldp.links), set([]))

        if 0:
            # TODO print("before")
            # TODO print(ldp.devices)
            # TODO print(ldp.links)
            # TODO print(ldp.interfaces)
            pass

        self.link.add_feature(ldp)
        self.link2.add_feature(ldp)
        self.link3.add_feature(ldp)
        self.link4.add_feature(ldp)
        self.assertCountEqual(ldp.devices, [self.dev1, self.dev2])
        self.assertSetEqual(set(ldp.links), set([self.link, self.link2, self.link3, self.link4]))
        self.assertSetEqual(set(ldp.interfaces), set([self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8]))

        if 1:
            # TODO print("after")
            # TODO print(ldp.links)
            # TODO print(ldp.devices)
            # TODO print(ldp.interfaces)
            pass

        # ==Test interface-only config==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/0/1')
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/0/3')
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/0/5')
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/0/7')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/0/2')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/0/4')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/0/6')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/0/8')

    def test_1_top_level(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)

        # ==Test top-level config==
        ldp.capabilities_cisco_iosxr = False
        ldp.default_vrf_impl_ipv4 = False
        ldp.ds_tlv = False
        ldp.hello_holdtime = 100
        ldp.hello_interval = 200
        ldp.instance_tlv = False
        ldp.quickstart = False
        ldp.targeted_hello_holdtime = 10
        ldp.targeted_hello_interval = 15
        ldp.entropy_label = True
        ldp.gr = True
        ldp.gr_fwdstate_holdtime = 60
        ldp.gr_maintain_acl = acl3
        ldp.gr_reconnect_timeout = 60
        ldp.igp_sync_delay_on_proc_restart = 300
        ldp.igp_sync_delay_on_session_up = 200
        ldp.log_gr = True
        ldp.log_hello_adj = True
        ldp.log_neighbor = True
        ldp.log_nsr = True
        ldp.log_sess_prot = True
        ldp.ltrace_buffer_multiplier = 3
        ldp.dualstack_tlv_compliance = True
        ldp.dualstack_transport_max_wait = 30
        ldp.dualstack_transport_prefer_ipv4 = True
        ldp.nsr = True
        ldp.password_type = 'clear'
        ldp.password = 'password1'
        ldp.device_attr['PE2'].password_type = 'encrypted'
        ldp.device_attr['PE2'].password = '060506324F41'
        ldp.session_backoff_init = 10
        ldp.device_attr['PE1'].session_backoff_init = 20
        ldp.session_backoff_max = 150
        ldp.device_attr['PE2'].session_backoff_max = 250
        ldp.session_holdtime = 333
        ldp.device_attr['PE1'].session_holdtime = 444
        ldp.session_protection = True
        ldp.session_protection_dur = 222
        ldp.device_attr['PE2'].session_protection_dur = 333
        ldp.session_protection_for_acl = acl1
        ldp.signalling_dscp = 16

        out = ldp.build_config(apply=False)
        if 1:
            self.assertCountEqual(out.keys(), ['PE1', 'PE2'])
            self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
                'mpls ldp',
                ' capabilities cisco ios-xr disable',
                ' default-vrf implicit-ipv4 disable',
                ' discovery',
                '  ds-tlv disable',
                '  hello holdtime 100',
                '  hello interval 200',
                '  instance-tlv disable',
                '  quick-start disable',
                '  targeted-hello holdtime 10',
                '  targeted-hello interval 15',
                '  exit',
                ' entropy-label',
                ' graceful-restart',
                ' graceful-restart forwarding-state-holdtime 60',
                ' graceful-restart reconnect-timeout 60',
                ' igp sync delay on-proc-restart 300',
                ' igp sync delay on-session-up 200',
                ' nsr',
                ' session backoff 20 150',
                ' session holdtime 444',
                ' session protection for acl1 duration 222',
                ' signalling dscp 16',
                ' log',
                '  graceful-restart',
                '  hello-adjacency',
                '  neighbor',
                '  nsr',
                '  session-protection',
                '  exit',
                ' ltrace-buffer multiplier 3',
                ' graceful-restart helper-peer maintain-on-local-reset for acl3',
                ' address-family ipv4',
                '  exit',
                ' interface GigabitEthernet0/0/0/1',
                '  address-family ipv4',
                '   exit',
                '  exit',
                ' neighbor',
                '  dual-stack tlv-compliance',
                '  dual-stack transport-connection max-wait 30',
                '  dual-stack transport-connection prefer ipv4',
                '  password clear password1',
                '  exit',
                ' exit', 
            ]))

            self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
                'mpls ldp',
                ' capabilities cisco ios-xr disable',
                ' default-vrf implicit-ipv4 disable',
                ' discovery',
                '  ds-tlv disable',
                '  hello holdtime 100',
                '  hello interval 200',
                '  instance-tlv disable',
                '  quick-start disable',
                '  targeted-hello holdtime 10',
                '  targeted-hello interval 15',
                '  exit',
                ' entropy-label',
                ' graceful-restart',
                ' graceful-restart forwarding-state-holdtime 60',
                ' graceful-restart reconnect-timeout 60',
                ' igp sync delay on-proc-restart 300',
                ' igp sync delay on-session-up 200',
                ' nsr',
                ' session backoff 10 250',
                ' session holdtime 333',
                ' session protection for acl1 duration 333',
                ' signalling dscp 16',
                ' log',
                '  graceful-restart',
                '  hello-adjacency',
                '  neighbor',
                '  nsr',
                '  session-protection',
                '  exit',
                ' ltrace-buffer multiplier 3',
                ' graceful-restart helper-peer maintain-on-local-reset for acl3',
                ' address-family ipv4',
                '  exit',
                ' interface GigabitEthernet0/0/0/2',
                '  address-family ipv4',
                '   exit',
                '  exit',
                ' neighbor',
                '  dual-stack tlv-compliance',
                '  dual-stack transport-connection max-wait 30',
                '  dual-stack transport-connection prefer ipv4',
                '  password encrypted 060506324F41',
                '  exit',
                ' exit', 
            ]))

        if 1:
            # set the per-attr variables that are inherited by VRF
            ldp.device_attr['PE1'].vrf_attr['default'].router_id = '1.1.1.1'
            ldp.device_attr['PE2'].vrf_attr['default'].router_id = '2.2.2.2'
            ldp.device_attr['PE1'].vrf_attr['default'].session_dod_acl = acl11
            ldp.device_attr['PE2'].vrf_attr['default'].session_dod_acl = acl22

            out = ldp.build_config(apply=False)
            self.assertRegex(str(out['PE1']), 'router-id 1.1.1.1')
            self.assertRegex(str(out['PE1']), 'session downstream-on-demand with acl11')

            self.assertRegex(str(out['PE2']), 'router-id 2.2.2.2')
            self.assertRegex(str(out['PE2']), 'session downstream-on-demand with acl22')

        # Check unconfig - <nsr> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__nsr')
        if 1:
            self.assertRegex(str(out['PE1']), 'no nsr')
            self.assertRegex(str(out['PE2']), 'no nsr')

        # Check unconfig - <gr> config filter=
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__gr')
        if 1:
            self.assertRegex(str(out['PE1']), 'no graceful-restart')
            self.assertRegex(str(out['PE2']), 'no graceful-restart')

    def test_2_per_vrf(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)
        vrf = Vrf(name='vrf1')
        ldp.add_force_vrf(vrf)
        vrf2 = Vrf(name='vrf2')
        ldp.add_force_vrf(vrf2)
        ldp.device_attr['PE1'].router_id = '1.1.1.1'
        ldp.device_attr['PE2'].router_id = '2.2.2.2'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].router_id = '11.11.11.11'
        ldp.device_attr['PE2'].vrf_attr['vrf1'].router_id = '22.22.22.22'
        ldp.device_attr['PE1'].session_dod_acl = acl1
        ldp.device_attr['PE2'].session_dod_acl = acl2
        ldp.device_attr['PE1'].vrf_attr['vrf1'].session_dod_acl = acl1111
        ldp.device_attr['PE2'].vrf_attr['vrf1'].session_dod_acl = acl2222
        ldp.device_attr['PE1'].vrf_attr['vrf1'].password_type = 'clear'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].password = 'password1'
        ldp.device_attr['PE2'].vrf_attr['vrf1'].password_type = 'encrypted'
        ldp.device_attr['PE2'].vrf_attr['vrf1'].password = '060506324F41'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].gr_maintain_acl = acl33
        ldp.device_attr['PE1'].vrf_attr['vrf2'].session_dod_acl = acl3333
        ldp.device_attr['PE2'].vrf_attr['vrf2'].session_dod_acl = acl4444
        ldp.device_attr['PE1'].vrf_attr['vrf2'].password_type = 'clear'
        ldp.device_attr['PE1'].vrf_attr['vrf2'].password = 'password1'
        ldp.device_attr['PE2'].vrf_attr['vrf2'].password_type = 'encrypted'
        ldp.device_attr['PE2'].vrf_attr['vrf2'].password = '060506334F41'
        ldp.device_attr['PE1'].vrf_attr['vrf2'].gr_maintain_acl = acl44

        # Test per vrf config
        
        # Check vrf config - full config
        out = ldp.build_config(apply=False)
        self.assertRegex(str(out['PE1']), '(?s)vrf1.*router-id 11.11.11.11')
        self.assertRegex(str(out['PE1']), 'router-id 1.1.1.1')
        self.assertRegex(str(out['PE2']), '(?s)vrf1.*router-id 22.22.22.22')
        self.assertRegex(str(out['PE2']), 'router-id 2.2.2.2')
        self.assertRegex(str(out['PE1']), '(?s)vrf1.*session downstream-on-demand with acl1111')
        self.assertRegex(str(out['PE2']), '(?s)vrf1.*session downstream-on-demand with acl2222')
        self.assertRegex(str(out['PE1']), '(?s)vrf1.*neighbor.*password clear password1')
        self.assertRegex(str(out['PE2']), '(?s)vrf1.*neighbor.*password encrypted 060506324F41')
        self.assertRegex(str(out['PE1']), '(?s)vrf1.*graceful-restart helper-peer maintain-on-local-reset for acl33')
        self.assertRegex(str(out['PE1']), '(?s)vrf2.*session downstream-on-demand with acl3333')
        self.assertRegex(str(out['PE2']), '(?s)vrf2.*session downstream-on-demand with acl4444')
        self.assertRegex(str(out['PE1']), '(?s)vrf2.*neighbor.*password clear password1')
        self.assertRegex(str(out['PE2']), '(?s)vrf2.*neighbor.*password encrypted 060506334F41')
        self.assertRegex(str(out['PE1']), '(?s)vrf2.*graceful-restart helper-peer maintain-on-local-reset for acl44')


        # Test VRF unconfig
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr')
        self.assertRegex(str(out['PE1']), 'no vrf vrf1')
        self.assertRegex(str(out['PE1']), 'no vrf vrf2')
        self.assertRegex(str(out['PE2']), 'no vrf vrf1')
        self.assertRegex(str(out['PE2']), 'no vrf vrf2')

        # Check vrf config - vrf config filter all-inclusive 
        out2 = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr')
        self.assertRegex(str(out2['PE1']), '(?s)vrf1.*router-id 11.11.11.11')
        self.assertRegex(str(out2['PE2']), '(?s)vrf1.*router-id 22.22.22.22')
        self.assertRegex(str(out2['PE1']), '(?s)vrf1.*session downstream-on-demand with acl1111')
        self.assertRegex(str(out2['PE2']), '(?s)vrf1.*session downstream-on-demand with acl2222')
        self.assertRegex(str(out2['PE1']), '(?s)vrf1.*neighbor.*password clear password1')
        self.assertRegex(str(out2['PE2']), '(?s)vrf1.*neighbor.*password encrypted 060506324F41')
        self.assertRegex(str(out2['PE1']), '(?s)vrf1.*graceful-restart helper-peer maintain-on-local-reset for acl33')
        self.assertRegex(str(out2['PE1']), '(?s)vrf2.*session downstream-on-demand with acl3333')
        self.assertRegex(str(out2['PE2']), '(?s)vrf2.*session downstream-on-demand with acl4444')
        self.assertRegex(str(out2['PE1']), '(?s)vrf2.*neighbor.*password clear password1')
        self.assertRegex(str(out2['PE2']), '(?s)vrf2.*neighbor.*password encrypted 060506334F41')
        self.assertRegex(str(out2['PE1']), '(?s)vrf2.*graceful-restart helper-peer maintain-on-local-reset for acl44')
        # interface output will be built as it comes from vrf default
        self.assertRegex(str(out2['PE1']), '(?s)interface Gig')
                

        # Check vrf config - device <PE1> config filter
        out3 = ldp.build_config(apply=False, attributes='device_attr__PE1')
        self.assertTrue('PE1' in out3)
        self.assertFalse('PE2' in out3)
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*router-id 11.11.11.11')
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*session downstream-on-demand with acl1111')
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*neighbor.*password clear password1')
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*graceful-restart helper-peer maintain-on-local-reset for acl33')
        self.assertRegex(str(out3['PE1']), '(?s)vrf2.*session downstream-on-demand with acl3333')
        self.assertRegex(str(out3['PE1']), '(?s)vrf2.*neighbor.*password clear password1')
        self.assertRegex(str(out3['PE1']), '(?s)vrf2.*graceful-restart helper-peer maintain-on-local-reset for acl44')
        self.assertRegex(str(out3['PE1']), '(?s)interface Gig')
        out3.keys()

        # Check vrf config - vrf <vrf1> config filter
        out3 = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__vrf1')
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*router-id 11.11.11.11')
        self.assertRegex(str(out3['PE2']), '(?s)vrf1.*router-id 22.22.22.22')
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*session downstream-on-demand with acl1111')
        self.assertRegex(str(out3['PE2']), '(?s)vrf1.*session downstream-on-demand with acl2222')
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*neighbor.*password clear password1')
        self.assertRegex(str(out3['PE2']), '(?s)vrf1.*neighbor.*password encrypted 060506324F41')
        self.assertRegex(str(out3['PE1']), '(?s)vrf1.*graceful-restart helper-peer maintain-on-local-reset for acl33')
        # vrf2 output should not be built
        self.assertNotRegex(str(out3['PE1']), '(?s)vrf2.*session downstream-on-demand with acl3333')
        self.assertNotRegex(str(out3['PE2']), '(?s)vrf2.*session downstream-on-demand with acl4444')
        self.assertNotRegex(str(out3['PE1']), '(?s)vrf2.*neighbor.*password clear password1')
        self.assertNotRegex(str(out3['PE2']), '(?s)vrf2.*neighbor.*password encrypted 060506334F41')
        self.assertNotRegex(str(out3['PE1']), '(?s)vrf2.*graceful-restart helper-peer maintain-on-local-reset for acl44')
        # interface output from default vrf should not be built
        self.assertNotRegex(str(out3['PE1']), '(?s)interface Gig')

        # Check vrf unconfig - vrf <vrf1> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__vrf1')
        self.assertRegex(str(out['PE1']), 'no vrf vrf1')
        self.assertNotRegex(str(out['PE1']), 'no vrf vrf2')
        self.assertRegex(str(out['PE2']), 'no vrf vrf1')
        self.assertNotRegex(str(out['PE2']), 'no vrf vrf2')

        # Check vrf unconfig - vrf <vrf1> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__router_id')
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*no router-id')
            self.assertRegex(str(out['PE2']), '(?s)vrf1.*no router-id')

        # Check vrf unconfig - vrf <vrf1> config filter after adding router-id to vrf2
        ldp.device_attr['PE1'].vrf_attr['vrf2'].router_id = '11.11.11.11'
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__router_id')
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*no router-id')
            self.assertRegex(str(out['PE1']), '(?s)vrf2.*no router-id')
            self.assertRegex(str(out['PE2']), '(?s)vrf1.*no router-id')

        # Check vrf config - vrf <vrf2> config filter
        out3 = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__vrf2')
        # TODO print("\nPE1 config\n" + str(out3['PE1']))
        # TODO print("\nPE2 config\n" + str(out3['PE2']))
        self.assertNotRegex(str(out3['PE1']), '(?s)vrf1.*router-id 11.11.11.11')
        self.assertNotRegex(str(out3['PE2']), '(?s)vrf1.*router-id 22.22.22.22')
        self.assertNotRegex(str(out3['PE1']), '(?s)vrf1.*session downstream-on-demand with acl1111')
        self.assertNotRegex(str(out3['PE2']), '(?s)vrf1.*session downstream-on-demand with acl2222')
        self.assertNotRegex(str(out3['PE1']), '(?s)vrf1.*neighbor.*password clear password1')
        self.assertNotRegex(str(out3['PE2']), '(?s)vrf1.*neighbor.*password encrypted 060506324F41')
        self.assertNotRegex(str(out3['PE1']), '(?s)vrf1.*graceful-restart helper-peer maintain-on-local-reset for acl33')
        # vrf2 output should not be built
        self.assertRegex(str(out3['PE1']), '(?s)vrf2.*session downstream-on-demand with acl3333')
        self.assertRegex(str(out3['PE2']), '(?s)vrf2.*session downstream-on-demand with acl4444')
        self.assertRegex(str(out3['PE1']), '(?s)vrf2.*neighbor.*password clear password1')
        self.assertRegex(str(out3['PE2']), '(?s)vrf2.*neighbor.*password encrypted 060506334F41')
        self.assertRegex(str(out3['PE1']), '(?s)vrf2.*graceful-restart helper-peer maintain-on-local-reset for acl44')
        # interface output should not be built
        self.assertNotRegex(str(out3['PE1']), '(?s)interface Gig.*address-family')

    def test_3_per_intf(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)
        self.link4.add_feature(ldp)

        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].igp_sync_delay_on_session_up = 250
        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].disc_hello_dualstack_tlv = AddressFamily.ipv4
        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].hello_holdtime = 50
        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].hello_interval = 60
        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].quickstart = False

        ldp.hello_interval = 88
        ldp.device_attr['PE2'].hello_holdtime = 99
        ldp.device_attr['PE2'].interface_attr['GigabitEthernet0/0/0/8'].disc_hello_dualstack_tlv = AddressFamily.ipv6
        ldp.device_attr['PE2'].interface_attr['GigabitEthernet0/0/0/8'].igp_sync_delay_on_session_up = False


        # ==Test per interface config===
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*igp sync delay on-session-up 250')
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery hello dual-stack-tlv ipv4')
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery hello holdtime 50')
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery hello interval 60')
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery quick-start disable')
            self.assertRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/8.*igp sync delay on-session-up disable')
            self.assertRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/8.*discovery hello dual-stack-tlv ipv6')
            # hello interval and hello holdtime are NOT inherited
            self.assertNotRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/2.*discovery hello holdtime 99')
            self.assertNotRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/2.*discovery hello interval 88')

        # Check intf config - intf <GigabitEthernet0/0/0/8> config filter
        # (needs vrf as it is under default VRF)
        out = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__*__interface_attr__GigabitEthernet0/0/0/8')
        if 1:
            self.assertNotRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*igp sync delay on-session-up 250')
            self.assertNotRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery hello dual-stack-tlv ipv4')
            self.assertNotRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery hello holdtime 50')
            self.assertNotRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery hello interval 60')
            self.assertNotRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*discovery quick-start disable')
            self.assertRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/8.*igp sync delay on-session-up disable')
            self.assertRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/8.*discovery hello dual-stack-tlv ipv6')
            self.assertNotRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/2.*discovery hello holdtime 99')
            self.assertNotRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/2.*discovery hello interval 88')

        # Check intf unconfig - intf <GigabitEthernet0/0/0/8> config filter
        # (needs vrf as it is under default VRF)
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__interface_attr__GigabitEthernet0/0/0/8')
        if 1:
            self.assertRegex(str(out['PE2']), 'no interface GigabitEthernet0/0/0/8')
            self.assertNotRegex(str(out['PE1']), 'interface GigabitEthernet0/0/0/1')
            self.assertNotRegex(str(out['PE2']), 'interface GigabitEthernet0/0/0/2')

        # Check intf unconfig - intf <GigabitEthernet0/0/0/8> attr <disc_hello_dualstack_tlv> config filter
        # (needs vrf as it is under default VRF)
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__interface_attr__GigabitEthernet0/0/0/8__disc_hello_dualstack_tlv')
        if 1:
            self.assertRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/8.*no discovery hello dual-stack-tlv')
            self.assertNotRegex(str(out['PE1']), 'interface GigabitEthernet0/0/0/1')
            self.assertNotRegex(str(out['PE2']), 'interface GigabitEthernet0/0/0/2')

    def test_4_per_af(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)
        ldp.address_families = set([AddressFamily.ipv4])
        ldp.address_families = set([AddressFamily.ipv4, AddressFamily.ipv6])

        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].targeted_hello_accept_from_acl = acl6

        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].transport_address = '1.2.3.4'
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].transport_address = '1:2::3'
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].advertise = False
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].advertise = False
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].advertise_expnull_to_acl = acl4
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].advertise_expnull = True
        #TODO - how does this work?
        #ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].advertise_interfaces = 'GigabitEthernet0/0/0/3'
        #ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].advertise_interfaces = 'GigabitEthernet0/0/0/3'
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].default_route = True
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].allocate_for_host_routes = True
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].allocate_for_acl = acl5
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].impnull_override_for_acl = acl1
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].impnull_override_for_acl = acl2
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].target_hello_accept = True
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].target_hello_accept_from_acl = acl7
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].redist_bgp = True
        #ldp.device_attr['PE1'].address_family_attr['ipv6'].redist_bgp_advto_acl = acl9
        #ldp.device_attr['PE1'].address_family_attr['ipv6'].redist_bgp_as = '100.200'
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].te_autotunnel_mesh_group_id = 'all'
        #ldp.device_attr['PE1'].address_family_attr['ipv6'].te_autotunnel_mesh_group_id = '100'


        # ==Test per address-family config==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*discovery transport-address 1.2.3.4')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv6.*discovery transport-address 1:2::3')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*advertise.*disable')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*advertise.*disable')
            #self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*advertise.*interface GigabitEthernet0/0/0/1')
            #self.assertRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*advertise.*interface GigabitEthernet0/0/0/3')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*advertise.*explicit-null to acl4')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*advertise.*explicit-null')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*default-route')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*allocate for host-routes')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*allocate for acl5')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*implicit-null-override for acl1')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*implicit-null-override for acl2')

        # Check af config - af <ipv4> config filter
        out = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__*__address_family_attr__ipv4')
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*discovery transport-address 1.2.3.4')
            self.assertNotRegex(str(out['PE1']), '(?s)address-family ipv6.*discovery transport-address 1:2::3')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*advertise.*disable')
            self.assertNotRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*advertise.*disable')
            #self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*advertise.*interface GigabitEthernet0/0/0/1')
            #self.assertNotRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*advertise.*interface GigabitEthernet0/0/0/2')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*advertise.*explicit-null to acl4')
            self.assertNotRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*advertise.*explicit-null')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*default-route')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*allocate for host-routes')
            self.assertNotRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*allocate for acl5')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*label.*local.*implicit-null-override for acl1')
            self.assertNotRegex(str(out['PE1']), '(?s)address-family ipv6.*label.*local.*implicit-null-override for acl2')

        # Check af unconfig - af <ipv4> unconfig filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__address_family_attr__ipv4')
        if 1:
            self.assertRegex(str(out['PE1']), 'no address-family ipv4')
            self.assertNotRegex(str(out['PE1']), 'no address-family ipv6')

        # Check af unconfig - af <ipv4> <transport_address> unconfig filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__address_family_attr__ipv4__transport_address')
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4.*no discovery transport-address')

    def test_5_per_interface_per_af(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)
        ldp.address_families = set([AddressFamily.ipv4, AddressFamily.ipv6])

        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].address_family_attr['ipv4'].igp_autoconfig = False

        # ipv6 config is rejected, comment this out
        #ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].address_family_attr['ipv6'].mldp.enabled = False
        #ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].address_family_attr['ipv6'].igp = True

        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].address_family_attr['ipv4'].transport_address = '2.3.4.5'
        ldp.device_attr['PE1'].interface_attr['GigabitEthernet0/0/0/1'].address_family_attr['ipv6'].transport_address = '2:3::5'
        ldp.device_attr['PE2'].interface_attr['GigabitEthernet0/0/0/2'].address_family_attr['ipv4'].transport_address = 'interface'
        ldp.device_attr['PE2'].interface_attr['GigabitEthernet0/0/0/2'].address_family_attr['ipv6'].transport_address = 'interface'

        # ==Test per interface per address-family config===
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*address-family ipv4.*igp auto-config disable')
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*address-family ipv4.*discovery transport-address 2.3.4.5')
            self.assertRegex(str(out['PE1']), '(?s)interface GigabitEthernet0/0/0/1.*address-family ipv6.*discovery transport-address 2:3::5')
            self.assertRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/2.*address-family ipv4.*discovery transport-address interface')
            self.assertRegex(str(out['PE2']), '(?s)interface GigabitEthernet0/0/0/2.*address-family ipv6.*discovery transport-address interface')

    def test_6_per_vrf_per_interface_per_af(self):

        ldp = Ldp()
        self.link.add_feature(ldp)

        vrf = Vrf(name='vrf1')
        self.i1.vrf = vrf
        self.i2.vrf = vrf
        ldp.device_attr['PE1'].vrf_attr['vrf1'].interface_attr['GigabitEthernet0/0/0/1'].address_family_attr['ipv4'].transport_address = '2.3.4.5'
        ldp.device_attr['PE2'].vrf_attr['vrf1'].interface_attr['GigabitEthernet0/0/0/2'].address_family_attr['ipv4'].transport_address = 'interface'

        # ==Test vrf per interface per address-family config==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*interface GigabitEthernet0/0/0/1.*address-family ipv4.*discovery transport-address 2.3.4.5')
            self.assertRegex(str(out['PE2']), '(?s)vrf1.*interface GigabitEthernet0/0/0/2.*address-family ipv4.*discovery transport-address interface')

    def test_7_per_neighbor(self):

        ldp = Ldp()
        self.link.add_feature(ldp)
        nbr1 = IPv4LsrNeighbor('1.2.3.4:0')
        nbr2 = IPv4LsrNeighbor('1.2.3.5:0')
        nbr3 = IPv4LsrNeighbor('1.2.3.6:0')
        

        ldp.device_attr['PE1'].password_type = 'clear'
        ldp.device_attr['PE1'].password = 'password1'
        ldp.device_attr['PE2'].password_type = 'encrypted'
        ldp.device_attr['PE2'].password = '060506324F41'
        ldp.device_attr['PE1'].vrf_attr['default'].neighbors = [nbr1, nbr2, nbr3]
        ldp.device_attr['PE1'].vrf_attr['default'].neighbor_attr[nbr1].disable_password = True
        ldp.device_attr['PE1'].vrf_attr['default'].neighbor_attr[nbr2].password_type = 'clear'
        ldp.device_attr['PE1'].vrf_attr['default'].neighbor_attr[nbr2].password = 'blah'
        ldp.device_attr['PE1'].vrf_attr['default'].neighbor_attr[nbr3].password_type = 'encrypted'
        ldp.device_attr['PE1'].vrf_attr['default'].neighbor_attr[nbr3].password = '060506324F41'

        # ==Test per neighbor config==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), 'neighbor\n.*password clear password1')
            self.assertRegex(str(out['PE2']), 'neighbor\n.*password encrypted 060506324F41')
            self.assertRegex(str(out['PE1']), '1.2.3.4:0 password disable')
            self.assertRegex(str(out['PE1']), '1.2.3.5:0 password clear blah')
            self.assertRegex(str(out['PE1']), '1.2.3.6:0 password encrypted 060506324F41')

        # Check nbr config - nbr <1.2.3.5:0'> config filter
        out = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__*__neighbor_attr__1.2.3.5:0')
        if 1:
            self.assertNotRegex(str(out['PE1']), 'neighbor\n.*password clear password1')
            self.assertNotRegex(str(out['PE2']), 'neighbor\n.*password encrypted 060506324F41')
            self.assertNotRegex(str(out['PE1']), '1.2.3.4:0 password disable')
            self.assertRegex(str(out['PE1']), '1.2.3.5:0 password clear blah')
            self.assertNotRegex(str(out['PE1']), '1.2.3.6:0 password encrypted 060506324F41')

        # Check nbr unconfig - nbr <1.2.3.5:0'> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__neighbor_attr__1.2.3.4:0__disable_password')
        if 1:
            self.assertNotRegex(str(out['PE1']), 'neighbor\n.*password clear password1')
            self.assertNotRegex(str(out['PE2']), 'neighbor\n.*password encrypted 060506324F41')
            self.assertRegex(str(out['PE1']), 'no 1.2.3.4:0 password disable')
            self.assertNotRegex(str(out['PE1']), '1.2.3.5:0 password clear blah')
            self.assertNotRegex(str(out['PE1']), '1.2.3.6:0 password encrypted 060506324F41')

        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__neighbor_attr__1.2.3.5:0__password')
        self.assertRegex(str(out['PE1']), 'no 1.2.3.5:0 password clear blah')
   
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__neighbor_attr__1.2.3.6:0__password')
        self.assertRegex(str(out['PE1']), 'no 1.2.3.6:0 password encrypted 060506324F41')

    def test_8_per_vrf_per_neighbor(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)
        vrf = Vrf(name='vrf1')
        ldp.add_force_vrf(vrf)
        nbr1 = IPv4LsrNeighbor('1.2.3.4:0')
        nbr2 = IPv4LsrNeighbor('1.2.3.5:0')
        nbr3 = IPv4LsrNeighbor('1.2.3.6:0')

        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbors = [nbr1, nbr2, nbr3]
        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbor_attr['1.2.3.4:0'].disable_password = True
        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbor_attr['1.2.3.5:0'].password_type = 'clear'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbor_attr['1.2.3.5:0'].password = 'blah22'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbor_attr['1.2.3.6:0'].password_type = 'encrypted'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbor_attr['1.2.3.6:0'].password = '060506324F41'

        # ==Test per vrf per neighbor config==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)vrf1\n.*neighbor\n.*1.2.3.4:0 password disable')
            self.assertRegex(str(out['PE1']), '(?s)vrf1\n.*neighbor\n.*1.2.3.5:0 password clear blah22')
            self.assertRegex(str(out['PE1']), '(?s)vrf1\n.*neighbor\n.*1.2.3.6:0 password encrypted 060506324F41')

    def test_9_per_af_per_neighbor(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')
        nbr1 = IPv4LsrNeighbor('1.2.3.4:0')
        nbr2 = IPv4LsrNeighbor('1.2.3.5:0')
        nbr3 = IPv4LsrNeighbor('1.2.3.6:0')
        nbr4 = IPv4LsrNeighbor('1.2.3.7:0')
        nbr5 = IPv4LsrNeighbor('1.2.3.8:0')
        nbr6 = IPv6Neighbor('1:2::3')
        nbr7 = IPv6Neighbor('1:2::4')
        nbr8 = IPv6Neighbor('1:2::5')

        ldp = Ldp()
        ldp.address_families = set([AddressFamily.ipv4, AddressFamily.ipv6])
        self.link.add_feature(ldp)

        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbors = [nbr1, nbr2, nbr3, nbr4, nbr5]
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbor_attr['1.2.3.4:0'].targeted = True
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbor_attr['1.2.3.5:0'].targeted = True
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbor_attr['1.2.3.6:0'].targeted = False
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbor_attr['1.2.3.5:0'].advertise_for_acl = acl1
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbor_attr['1.2.3.6:0'].advertise_for_acl = acl2
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbor_attr['1.2.3.7:0'].accept_for_acl = acl1
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv4'].neighbor_attr['1.2.3.8:0'].accept_for_acl = acl2
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].neighbors = [nbr6, nbr7, nbr8]
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].neighbor_attr['1:2::3'].targeted = True
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].neighbor_attr['1:2::4'].targeted = True
        ldp.device_attr['PE1'].vrf_attr['default'].address_family_attr['ipv6'].neighbor_attr['1:2::5'].targeted = False

        # ==Test per af per neighbor config==
        out = ldp.build_config(apply=False)
        #print("\n PE1 CONFIG\n" + str(out['PE1']))
        #print("\n PE2 CONFIG\n" + str(out['PE2']))
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4\n.*neighbor 1.2.3.4 targeted')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4\n.*neighbor 1.2.3.5 targeted')
            self.assertNotRegex(str(out['PE1']), '(?s)address-family ipv4\n.*neighbor 1.2.3.6 targeted')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4\n.*label.*local.*advertise.*to 1.2.3.5:0 for acl1')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4\n.*label.*local.*advertise.*to 1.2.3.6:0 for acl2')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4\n.*label.*remote.*accept.*from 1.2.3.7:0 for acl1')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv4\n.*label.*remote.*accept.*from 1.2.3.8:0 for acl2')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv6\n.*neighbor 1:2::3 targeted')
            self.assertRegex(str(out['PE1']), '(?s)address-family ipv6\n.*neighbor 1:2::4 targeted')
 
    def test_x1_per_vrf_per_af(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)

        vrf = Vrf(name='vrf1')
        ldp.add_force_vrf(vrf)
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].transport_address = '1.2.3.4'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].advertise = False
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].advertise_expnull_to_acl = acl4
        #TODO Skip for now
        #ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].advertise_interfaces = 'GigabitEthernet0/0/0/1'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].allocate_for_host_routes = True
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].default_route = True
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].impnull_override_for_acl = acl1

        # ==Test per vrf per address family config==
        out = ldp.build_config(apply=False)
        #print("\n PE1 CONFIG\n" + str(out['PE1']))
        #print("\n PE2 CONFIG\n" + str(out['PE2']))
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*discovery transport-address 1.2.3.4')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*local.*advertise.*disable')
            #self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*local.*advertise.*interface GigabitEthernet0/0/0/1')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*local.*advertise.*explicit-null to acl4')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*local.*default-route')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*local.*allocate for host-routes')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*local.*implicit-null-override for acl1')

    def test_x2_per_vrf_per_af_per_nbr(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')
        nbr1 = IPv4LsrNeighbor('1.2.3.5:0')
        nbr2 = IPv4LsrNeighbor('1.2.3.6:0')
        nbr3 = IPv4LsrNeighbor('1.2.3.7:0')
        nbr4 = IPv4LsrNeighbor('1.2.3.8:0')

        ldp = Ldp()
        self.link.add_feature(ldp)

        vrf = Vrf(name='vrf1')
        ldp.add_force_vrf(vrf)
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].neighbors = [nbr1, nbr2, nbr3, nbr4]
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].neighbor_attr['1.2.3.5:0'].advertise_for_acl = acl1
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].neighbor_attr['1.2.3.6:0'].advertise_for_acl = acl2
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].neighbor_attr['1.2.3.7:0'].accept_for_acl = acl1
        ldp.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv4'].neighbor_attr['1.2.3.8:0'].accept_for_acl = acl2

        # ==Test per vrf per address family per neighbor config==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4\n.*label.*local.*advertise.*to 1.2.3.5:0 for acl1')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4\n.*label.*local.*advertise.*to 1.2.3.6:0 for acl2')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*remote.*accept.*from 1.2.3.7:0 for acl1')
            self.assertRegex(str(out['PE1']), '(?s)vrf1.*address-family ipv4.*label.*remote.*accept.*from 1.2.3.8:0 for acl2')

    def test_x3_config_from_ldp_job(self):

        acl1 = AccessList(name='acl1')
        acl2 = AccessList(name='acl2')
        acl3 = AccessList(name='acl3')
        acl4 = AccessList(name='acl4')
        acl5 = AccessList(name='acl5')
        acl6 = AccessList(name='acl6')
        acl7 = AccessList(name='acl7')
        acl8 = AccessList(name='acl8')
        acl9 = AccessList(name='acl9')
        acl11 = AccessList(name='acl11')
        acl22 = AccessList(name='acl22')
        acl33 = AccessList(name='acl33')
        acl44 = AccessList(name='acl44')
        acl1111 = AccessList(name='acl1111')
        acl2222 = AccessList(name='acl2222')
        acl3333 = AccessList(name='acl3333')
        acl4444 = AccessList(name='acl4444')

        ldp = Ldp()
        self.link.add_feature(ldp)
        self.link2.add_feature(ldp)
        self.link3.add_feature(ldp)
        self.link4.add_feature(ldp)

        ldp.device_attr['PE1'].router_id = '1.1.1.1'
        ldp.device_attr['PE2'].router_id = '2.2.2.2'
        ldp.nsr = True
        ldp.gr = True
        ldp.session_protection = True

        # ==Test LDP GR config from LDP Tier1 job==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), 'router-id 1.1.1.1')
            self.assertRegex(str(out['PE1']), 'graceful-restart')
            self.assertRegex(str(out['PE1']), 'session protection')
            self.assertRegex(str(out['PE1']), 'nsr')
            self.assertRegex(str(out['PE1']), 'address-family ipv4')
            self.assertRegex(str(out['PE2']), 'address-family ipv4')

            for intf_obj in ldp.device_attr['PE1'].interfaces:
                self.assertRegex(str(out['PE1']), '(?s)interface {name}.*address-family ipv4'.
                                             format(name=intf_obj.name))

            for intf_obj in ldp.device_attr['PE2'].interfaces:
                self.assertRegex(str(out['PE2']), '(?s)interface {name}.*address-family ipv4'.
                                             format(name=intf_obj.name))

        # ==Test LDP GR unconfig from LDP Tier1 job==
        out = ldp.build_unconfig(apply=False)

if __name__ == '__main__':
    unittest.main()

