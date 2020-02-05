#!/usr/bin/env python

'''
IOSXE unit tests for Genie Standby conf using YANG.
'''

# Python
import re
import unittest
from unittest.mock import Mock

# Genie
from genie.conf import Genie
from genie.tests.conf import TestCase
from genie.conf.base import Testbed, Device
from genie.libs.conf.hsrp.hsrp import Hsrp
from genie.libs.conf.interface import Interface

# YDK
from ydk.models.cisco_iosxe_native import Cisco_IOS_XE_native as ned
from ydk.types import DELETE, Empty
from ydk.services import CRUDService
from ydk.services import CodecService
from ydk.providers import CodecServiceProvider

# Patch a netconf provider
from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider
from ydk.providers._provider_plugin import _ClientSPPlugin

class NetconfConnectionInfo(object):
    def __init__(self):
        self.ip = '1.1.1.1'
        self.port = 830
        self.username = 'admin'
        self.password = 'lab'

class test_hsrp(TestCase):

    def setUp(self):

        # Set Genie Tb
        self.testbed = Testbed()
        Genie.testbed = self.testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=self.testbed,
                           os='iosxe', context='yang')
        
        # Interface
        self.intf1 = Interface(name='GigabitEthernet1/0/1', device=self.dev1)
        self.intf1.shutdown = False
        self.intf1.switchport = False
        
        # Hsrp object
        self.hsrp1 = Hsrp()
        
        # Build config
        cfgs = self.intf1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no shutdown',
                ' no switchport',
                ' exit',
            ]))

    def test_yang_config1(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 25
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.preempt_sync_delay = 20
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_word = 'cisco123'
        key.bfd = True
        key.mac_refresh = 11
        key.follow = 'test'

        for dev in self.testbed.devices:
            dev.connections=Mock()
            dev.connections={'netconf':NetconfConnectionInfo()}

        # Build config
        build_cfgs = self.hsrp1.build_config(apply=False)

        compare1 = ""
        for i in build_cfgs['PE1']:
            compare1+=str(i)

        self.assertMultiLineEqual(compare1, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <bfd></bfd>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <mac-refresh>11</mac-refresh>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <word>cisco123</word>\n'
            '          </authentication>\n'
            '          <follow>test</follow>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '              <reload>10</reload>\n'
            '              <sync>20</sync>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

        # Build config
        build_uncfgs = self.hsrp1.build_unconfig(apply=False)

        compare2 = ""
        for i in build_uncfgs['PE1']:
            compare2+=str(i)

        self.assertMultiLineEqual(compare2, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <bfd></bfd>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <mac-refresh>11</mac-refresh>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <word>cisco123</word>\n'
            '          </authentication>\n'
            '          <follow>test</follow>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '              <reload>10</reload>\n'
            '              <sync>20</sync>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

    def test_yang_config2(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 25
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_text = 'cisco123'

        # Build config
        build_cfgs = self.hsrp1.build_config(apply=False)

        compare1 = ""
        for i in build_cfgs['PE1']:
            compare1+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare1, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <word>cisco123</word>\n'
            '          </authentication>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '              <reload>10</reload>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>1</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

        # Build unconfig
        build_uncfgs = self.hsrp1.build_unconfig(apply=False)

        compare2 = ""
        for i in build_uncfgs['PE1']:
            compare2+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare2, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <word>cisco123</word>\n'
            '          </authentication>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '              <reload>10</reload>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>1</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

    def test_yang_config3(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 25
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_md5_keychain = 'abc'

        # Build config
        build_cfgs = self.hsrp1.build_config(apply=False)

        compare1 = ""
        for i in build_cfgs['PE1']:
            compare1+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare1, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <md5>\n'
            '              <key-chain>abc</key-chain>\n'
            '            </md5>\n'
            '          </authentication>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

        # Build unconfig
        build_uncfgs = self.hsrp1.build_unconfig(apply=False)

        compare2 = ""
        for i in build_uncfgs['PE1']:
            compare2+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare2, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <md5>\n'
            '              <key-chain>abc</key-chain>\n'
            '            </md5>\n'
            '          </authentication>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

    def test_yang_config4(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 25
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_md5_keystring = 'xyz'

        # Build config
        build_cfgs = self.hsrp1.build_config(apply=False)

        compare1 = ""
        for i in build_cfgs['PE1']:
            compare1+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare1, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <md5>\n'
            '              <key-string>\n'
            '                <string>xyz</string>\n'
            '              </key-string>\n'
            '            </md5>\n'
            '          </authentication>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '              <reload>10</reload>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>1</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

        # Build unconfig
        build_uncfgs = self.hsrp1.build_unconfig(apply=False)

        compare2 = ""
        for i in build_uncfgs['PE1']:
            compare2+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare2, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '          <reload>10</reload>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <authentication>\n'
            '            <md5>\n'
            '              <key-string>\n'
            '                <string>xyz</string>\n'
            '              </key-string>\n'
            '            </md5>\n'
            '          </authentication>\n'
            '          <ip>\n'
            '            <address>192.168.1.254</address>\n'
            '          </ip>\n'
            '          <preempt>\n'
            '            <delay>\n'
            '              <minimum>5</minimum>\n'
            '              <reload>10</reload>\n'
            '            </delay>\n'
            '          </preempt>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <seconds>1</seconds>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <seconds>3</seconds>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <decrement>20</decrement>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <version>1</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

    def test_yang_config5(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.group_number = 25
        key.priority = 110
        key.preempt = True
        key.bfd = True
        key.use_bia = True
        key.hello_interval_msec = 55
        key.holdtime_msec = 100
        key.track_object = 1
        key.track_shutdown = True
        key.group_name = 'gandalf'
        key.mac_address = 'dead.beef.dead'

        # Build config
        build_cfgs = self.hsrp1.build_config(apply=False)

        compare1 = ""
        for i in build_cfgs['PE1']:
            compare1+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare1, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <bfd></bfd>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <mac-address>dead.beef.dead</mac-address>\n'
            '          <name>gandalf</name>\n'
            '          <preempt/>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <msec>55</msec>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <msec>100</msec>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <shutdown></shutdown>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <use-bia>\n'
            '          <scope>\n'
            '            <interface></interface>\n'
            '          </scope>\n'
            '        </use-bia>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

        # Build unconfig
        build_uncfgs = self.hsrp1.build_unconfig(apply=False)

        compare2 = ""
        for i in build_uncfgs['PE1']:
            compare2+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare2, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <bfd></bfd>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <mac-address>dead.beef.dead</mac-address>\n'
            '          <name>gandalf</name>\n'
            '          <preempt/>\n'
            '          <priority>110</priority>\n'
            '          <timers>\n'
            '            <hello-interval>\n'
            '              <msec>55</msec>\n'
            '            </hello-interval>\n'
            '            <hold-time>\n'
            '              <msec>100</msec>\n'
            '            </hold-time>\n'
            '          </timers>\n'
            '          <track>\n'
            '            <number>1</number>\n'
            '            <shutdown></shutdown>\n'
            '          </track>\n'
            '        </standby-list>\n'
            '        <use-bia>\n'
            '          <scope>\n'
            '            <interface></interface>\n'
            '          </scope>\n'
            '        </use-bia>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))
        

    def test_yang_config6(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.group_number = 25
        key.priority = 110
        key.preempt = True
        key.ipv6_address = 'autoconfig'

        # Build config
        build_cfgs = self.hsrp1.build_config(apply=False)

        compare1 = ""
        for i in build_cfgs['PE1']:
            compare1+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare1, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <ipv6>autoconfig</ipv6>\n'
            '          <preempt/>\n'
            '          <priority>110</priority>\n'
            '        </standby-list>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

        # Build unconfig
        build_uncfgs = self.hsrp1.build_unconfig(apply=False)

        compare2 = ""
        for i in build_uncfgs['PE1']:
            compare2+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare2, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <delay>\n'
            '          <minimum>5</minimum>\n'
            '        </delay>\n'
            '        <standby-list>\n'
            '          <group-number>25</group-number>\n'
            '          <ipv6>autoconfig</ipv6>\n'
            '          <preempt/>\n'
            '          <priority>110</priority>\n'
            '        </standby-list>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))


    def test_yang_config7(self):
        
        # Hsrp object
        self.hsrp1 = Hsrp()

        # Apply configuration
        key1 = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key1.version = 2
        key1.group_number = 10
        key1.priority = 110
        key1.preempt = True
        key1.preempt_reload_delay = 30
        
        # Hsrp object
        self.hsrp2 = Hsrp()

        # Apply configuration
        key2 = self.hsrp2.device_attr[self.dev1].interface_attr[self.intf1]
        key2.group_number = 20
        key2.priority = 120
        key2.preempt = True
        key2.preempt_sync_delay = 60

        # Build config
        cfgs1 = self.hsrp1.build_config(apply=False)
        cfgs2 = self.hsrp2.build_config(apply=False)

        compare = ""
        for i in cfgs1['PE1']:
            compare+=str(i)

        for i in cfgs2['PE1']:
            compare+=str(i)

        # Check config built correctly
        self.assertMultiLineEqual(compare, '\n'.join([
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <standby-list>\n'
            '          <group-number>10</group-number>\n'
            '          <preempt/>\n'
            '          <priority>110</priority>\n'
            '        </standby-list>\n'
            '        <version>2</version>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '  <target>\n'
            '    <running></running>\n'
            '  </target>\n'
            '  <config>\n'
            '    <GigabitEthernet xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
            '      <name></name>\n'
            '      <standby>\n'
            '        <standby-list>\n'
            '          <group-number>20</group-number>\n'
            '          <preempt/>\n'
            '          <priority>120</priority>\n'
            '        </standby-list>\n'
            '      </standby>\n'
            '    </GigabitEthernet>\n'
            '  </config>\n'
            '</edit-config>\n'
            ]))

if __name__ == '__main__':
    unittest.main()


