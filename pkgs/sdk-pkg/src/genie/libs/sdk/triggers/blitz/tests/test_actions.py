#! /usr/bin/env python
import os
import tempfile
import unittest
import importlib
from unittest.mock import Mock
from unittest.mock import patch

from genie.libs import sdk
from genie.testbed import load
from genie.conf.base.api import API
from genie.conf.base import Testbed, Device
from genie.harness.script import TestScript
from genie.harness.standalone import run_genie_sdk
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.ops.platform.nxos.platform import Platform
from genie.libs.sdk.libs.abstracted_libs.restore import Restore
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.triggers.blitz.actions import compare, rest, sleep, \
                                                  restore_config_snapshot, \
                                                  bash_console, genie_sdk, \
                                                  api, learn, bash_console,\
                                                  parse, execute, configure,\
                                                  print_, configure_replace,\
                                                  save_config_snapshot, diff,\
                                                  configure_dual

from genie.libs.sdk.triggers.blitz.actions_helper import _send_command,\
                                                         _prompt_handler, \
                                                         _condition_validator, \
                                                         _output_query_template



from unicon import Connection

from pyats.aetest.steps import Steps
from pyats.aetest.parameters import ParameterMap
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked


class TestActions(unittest.TestCase):

    parser_output = {'platform': {'name': 'Nexus',
               'os': 'NX-OS',
               'software': {'bios_version': '07.33',
                'system_version': '9.3(3) [build 9.3(3)IDI9(0.509)]',
                'bios_compile_time': '08/04/2015',
                'system_image_file': 'bootflash:///system-image-N93_3-00613722415136',
                'system_compile_time': '10/22/2019 10:00:00 [10/22/2019 16:57:31]'},
               'hardware': {'model': 'Nexus9000 C9396PX',
                'chassis': 'Nexus9000 C9396PX',
                'slots': 'None',
                'rp': 'None',
                'cpu': 'Intel(R) Core(TM) i3- CPU @ 2.50GHz',
                'memory': '16399900 kB',
                'processor_board_id': 'SAL1914CNL6',
                'device_name': 'N93_3',
                'bootflash': '51496280 kB'},
               'kernel_uptime': {'days': 61, 'hours': 22, 'minutes': 8, 'seconds': 40},
               'reason': 'Reset Requested by CLI command reload',
               'system_version': '9.3(3)'}}

    execute_output = """
        2020-11-24 12:25:43,769: %UNICON-INFO: +++ N93_3: executing command 'show version' +++
        show version
        Cisco Nexus Operating System (NX-OS) Software
        TAC support: http://www.cisco.com/tac
        Copyright (C) 2002-2019, Cisco and/or its affiliates.
        All rights reserved.
        The copyrights to certain works contained in this software are
        owned by other third parties and used and distributed under their own
        licenses, such as open source.  This software is provided "as is," and unless
        otherwise stated, there is no warranty, express or implied, including but not
        limited to warranties of merchantability and fitness for a particular purpose.
        Certain components of this software are licensed under
        the GNU General Public License (GPL) version 2.0 or
        GNU General Public License (GPL) version 3.0  or the GNU
        Lesser General Public License (LGPL) Version 2.1 or
        Lesser General Public License (LGPL) Version 2.0.
        A copy of each such license is available at
        http://www.opensource.org/licenses/gpl-2.0.php and
        http://opensource.org/licenses/gpl-3.0.html and
        http://www.opensource.org/licenses/lgpl-2.1.php and
        http://www.gnu.org/licenses/old-licenses/library.txt.
        Software
          BIOS: version 07.33
         NXOS: version 9.3(3) [build 9.3(3)IDI9(0.509)]
          BIOS compile time:  08/04/2015
          NXOS image file is: bootflash:///system-image-N93_3-00613722415136
          NXOS compile time:  10/22/2019 10:00:00 [10/22/2019 16:57:31]
        Hardware
          cisco Nexus9000 C9396PX Chassis
          Intel(R) Core(TM) i3- CPU @ 2.50GHz with 16399900 kB of memory.
          Processor Board ID SAL1914CNL6
          Device name: N93_3
          bootflash:   51496280 kB
        Kernel uptime is 61 day(s), 22 hour(s), 33 minute(s), 56 second(s)
        Last reset at 930930 usecs after Wed Sep 23 13:59:45 2020
          Reason: Reset Requested by CLI command reload
          System version: 9.3(3)
          Service:
        plugin
          Core Plugin, Ethernet Plugin
        Active Package(s):
    """

    learn_config_out = {'version 9.3(3) Bios:version 07.33': {},
       'switchname N93_3': {},
       'install feature-set mpls': {},
       'vdc N93_3 id 1': {'allow feature-set mpls': {},
        'limit-resource vlan minimum 16 maximum 4094': {},
        'limit-resource vrf minimum 2 maximum 4096': {},
        'limit-resource port-channel minimum 0 maximum 256': {},
        'limit-resource u4route-mem minimum 248 maximum 248': {},
        'limit-resource u6route-mem minimum 96 maximum 96': {},
        'limit-resource m4route-mem minimum 58 maximum 58': {},
        'limit-resource m6route-mem minimum 8 maximum 8': {}},
       'feature-set mpls': {},
       'feature telnet': {},
       'feature nxapi': {},
       'feature bash-shell': {},
       'cfs eth distribute': {},
       'feature ospf': {},
       'feature bgp': {},
       'feature ospfv3': {},
       'feature pim': {},
       'feature msdp': {},
       'feature eigrp': {},
       'feature rip': {},
       'feature isis': {},
       'feature restconf': {},
       'feature lacp': {},
       'feature lldp': {},
       'feature bfd': {},
       'clock timezone EDT -4 0': {},
       'feature openflow': {},
       'no password strength-check': {},
       'username admin password 5 $5$Yw0w8GI3$Rh2oBoUrsAgV4.x61a9by6PwppEzgL7rxQFZsizlGl7  role network-admin': {},
       'username adminbackup password 5 !  role network-operator': {},
       'username adminbackup passphrase  lifetime 99999 warntime 14 gracetime 3': {},
       'username lab password 5 $5$BVTTHCU7$j81UEWnkPmiq3s4AxAVqljTPt6bQe/s.d5pXm1PY/v.  role network-admin': {},
       'username lab passphrase  lifetime 99999 warntime 14 gracetime 3': {},
       'no ip domain-lookup': {},
       'ip access-list restconf-acl': {},
       'copp profile strict': {},
       'snmp-server user lab network-admin auth md5 0xa783b1816f5c3d2d881087c98778e010 priv 0xa783b1816f5c3d2d881087c98778e010 localizedkey': {},
       'snmp-server user admin network-admin auth md5 0x8358936bc6e5ecec1ce2f4f9f3dd480e priv 0x8358936bc6e5ecec1ce2f4f9f3dd480e localizedkey': {},
       'rmon event 1 log trap public description FATAL(1) owner PMON@FATAL': {},
       'rmon event 2 log trap public description CRITICAL(2) owner PMON@CRITICAL': {},
       'rmon event 3 log trap public description ERROR(3) owner PMON@ERROR': {},
       'rmon event 4 log trap public description WARNING(4) owner PMON@WARNING': {},
       'rmon event 5 log trap public description INFORMATION(5) owner PMON@INFO': {},
       'ipv6 route 2:2:2::/64 13:1:1::2': {},
       'ip pim rp-address 13.10.1.1 group-list 228.0.0.0/24 bidir': {},
       'ip pim rp-address 100.10.1.1 group-list 225.0.0.0/8': {},
       'ip pim bsr rp-candidate loopback12 group-list 227.0.0.0/8': {},
       'ip pim send-rp-announce loopback11 group-list 226.0.0.0/8': {},
       'ip pim ssm range 232.0.0.0/8': {},
       'ip pim auto-rp forward listen': {},
       'ip pim bsr forward listen': {},
       'no ip igmp snooping': {},
       'ip msdp originator-id loopback14': {},
       'ip msdp peer 14.10.1.2 connect-source loopback14': {},
       'no ipv6 mld snooping': {},
       'vlan 1,10-11,100': {},
       'ip prefix-list PREFIX seq 10 permit 0.0.0.0/0 le 32': {},
       'ip prefix-list PREFIX_STATIC_RP seq 5 permit 225.1.1.0/24': {},
       'route-map RMAP permit 10': {'match ip address prefix-list PREFIX': {}},
       'route-map STATIC_RP permit 10': {'match ip address prefix-list PREFIX_STATIC_RP': {}},
       'vrf context management': {'ip route 0.0.0.0/0 10.1.2.1': {}},
       'vrf context vni_10100': {},
       'hardware access-list tcam region ifacl 0': {},
       'hardware access-list tcam region mcast_bidir 256': {},
       'hardware forwarding unicast trace': {},
       'openflow': {},
       'vlan configuration 10': {'ipv6 mld snooping static-group ff1e::11:1 interface Ethernet1/30': {}},
       'vlan configuration 11': {'ipv6 mld snooping mrouter interface Ethernet1/32': {},
        'ipv6 mld snooping static-group ff1e::11 interface Ethernet1/32': {}},
       'nxapi http port 80': {},
       'interface port-channel201': {},
       'interface Ethernet1/1': {},
       'interface Ethernet1/2': {'shutdown': {}},
       'interface Ethernet1/3': {'shutdown': {}},
       'interface Ethernet1/4': {},
       'interface Ethernet1/5': {},
       'interface Ethernet1/6': {},
       'interface Ethernet1/7': {'no switchport': {}, 'no shutdown': {}},
       'interface Ethernet1/7.1': {'encapsulation dot1q 300': {},
        'ip address 201.0.6.1/24': {},
        'ipv6 address 201::6:1/112': {},
        'ip router ospf 1 area 0.0.0.0': {},
        'ipv6 router ospfv3 1 area 0.0.0.0': {},
        'ip pim sparse-mode': {},
        'no shutdown': {}},
       'interface Ethernet1/7.2': {'encapsulation dot1q 301': {},
        'ip address 201.1.6.1/24': {},
        'ipv6 address 201:1::6:1/112': {},
        'ip router isis 1': {},
        'ipv6 router isis 1': {},
        'no shutdown': {}},
       'interface Ethernet1/7.4': {'encapsulation dot1q 304': {},
        'ip address 201.4.6.1/24': {},
        'ipv6 address 201:4::6:1/112': {},
        'ipv6 router eigrp 1': {},
        'ip router eigrp 1': {},
        'no shutdown': {}},
       'interface Ethernet1/8': {'no switchport': {}, 'no shutdown': {}},
       'interface Ethernet1/9': {},
       'interface Ethernet1/10': {},
       'interface Ethernet1/11': {},
       'interface Ethernet1/12': {},
       'interface Ethernet1/13': {},
       'interface Ethernet1/14': {},
       'interface Ethernet1/15': {'no switchport': {}, 'no shutdown': {}},
       'interface Ethernet1/15.1': {'encapsulation dot1q 300': {},
        'ip address 201.0.11.1/24': {},
        'ipv6 address 201::11:1/112': {},
        'ip router ospf 1 area 0.0.0.0': {},
        'ipv6 router ospfv3 1 area 0.0.0.0': {},
        'ip pim sparse-mode': {},
        'no shutdown': {}},
       'interface Ethernet1/15.2': {'encapsulation dot1q 301': {},
        'ip address 201.1.11.1/24': {},
        'ipv6 address 201:1::11:1/112': {},
        'ip router isis 1': {},
        'ipv6 router isis 1': {},
        'no shutdown': {}},
       'interface Ethernet1/15.4': {'encapsulation dot1q 304': {},
        'ip address 201.4.11.1/24': {},
        'ipv6 address 201:4::11:1/112': {},
        'ipv6 router eigrp 1': {},
        'ip router eigrp 1': {},
        'no shutdown': {}},
       'interface Ethernet1/16': {},
       'interface Ethernet1/17': {},
       'interface Ethernet1/18': {},
       'interface Ethernet1/19': {'no switchport': {}},
       'interface Ethernet1/20': {'no switchport': {}, 'no shutdown': {}},
       'interface Ethernet1/21': {'no switchport': {}, 'no shutdown': {}},
       'interface Ethernet1/22': {},
       'interface Ethernet1/23': {},
       'interface Ethernet1/24': {},
       'interface Ethernet1/25': {},
       'interface Ethernet1/26': {},
       'interface Ethernet1/27': {},
       'interface Ethernet1/28': {},
       'interface Ethernet1/29': {},
       'interface Ethernet1/30': {},
       'interface Ethernet1/31': {},
       'interface Ethernet1/32': {'switchport mode trunk': {}},
       'interface Ethernet1/33': {},
       'interface Ethernet1/34': {},
       'interface Ethernet1/35': {},
       'interface Ethernet1/36': {},
       'interface Ethernet1/37': {},
       'interface Ethernet1/38': {},
       'interface Ethernet1/39': {},
       'interface Ethernet1/40': {},
       'interface Ethernet1/41': {},
       'interface Ethernet1/42': {},
       'interface Ethernet1/43': {},
       'interface Ethernet1/44': {},
       'interface Ethernet1/45': {},
       'interface Ethernet1/46': {},
       'interface Ethernet1/47': {},
       'interface Ethernet1/48': {},
       'interface Ethernet2/1': {},
       'interface Ethernet2/2': {},
       'interface Ethernet2/3': {'shutdown': {}},
       'interface Ethernet2/4': {},
       'interface Ethernet2/5': {},
       'interface Ethernet2/6': {},
       'interface Ethernet2/7': {'shutdown': {}},
       'interface Ethernet2/8': {},
       'interface Ethernet2/9': {},
       'interface Ethernet2/10': {},
       'interface Ethernet2/11': {},
       'interface Ethernet2/12': {},
       'interface mgmt0': {'vrf member management': {},
        'ip address 10.1.2.63/24': {}},
       'interface loopback0': {'shutdown': {}},
       'interface loopback1': {},
       'interface loopback10': {'ip address 100.10.1.1/24': {},
        'ipv6 address 100:10::1:1/112': {},
        'ip router ospf 1 area 0.0.0.0': {},
        'ipv6 router ospfv3 1 area 0.0.0.0': {},
        'ip pim sparse-mode': {}},
       'interface loopback11': {'ip address 11.10.1.1/24': {},
        'ipv6 address 11:10::1:1/112': {},
        'ip router ospf 1 area 0.0.0.0': {},
        'ipv6 router ospfv3 1 area 0.0.0.0': {},
        'ip pim sparse-mode': {}},
       'interface loopback12': {'ip address 12.10.1.1/24': {},
        'ipv6 address 12:10::1:1/112': {},
        'ip router ospf 1 area 0.0.0.0': {},
        'ipv6 router ospfv3 1 area 0.0.0.0': {},
        'ip pim sparse-mode': {}},
       'interface loopback13': {'ip address 13.10.1.1/24': {},
        'ipv6 address 13:10::1:1/112': {},
        'ip router ospf 1 area 0.0.0.0': {},
        'ipv6 router ospfv3 1 area 0.0.0.0': {},
        'ip pim sparse-mode': {}},
       'interface loopback14': {'description MSDP PEER': {},
        'ip address 14.10.1.1/24': {},
        'ip router ospf 1 area 0.0.0.0': {},
        'ip pim sparse-mode': {}},
       'line console': {'exec-timeout 0': {}, 'terminal width  511': {}},
       'line vty': {'exec-timeout 0': {}},
       'email': {},
       'boot nxos bootflash:/system-image-N93_3-00613722415136': {},
       'router eigrp 1': {'redistribute ospf 1 route-map RMAP': {}},
       'router ospf 1': {'router-id 110.1.1.1': {}},
       'router ospfv3 1': {},
       'router isis 1': {'net 49.0001.0000.0000.0005.00': {}},
       'personality': {},
       'no logging console': {}}

    def setUp(self):

        dir_name = os.path.dirname(os.path.abspath(__file__))

        self.testbed = load(os.path.join(dir_name, 'mock_testbeds/testbed.yaml'))
        Blitz.parameters = ParameterMap()
        Blitz.uid = 'test.dev'
        Blitz.parameters['testbed'] = self.testbed
        self.blitz_obj = Blitz()
        self.dev = Device( name='PE1', os='iosxe')
        self.dev.custom = {'abstraction': {'order': ['os']}}
        self.blitz_obj.parameters['test_sections'] = [{'section1': [{'action': {'command': 'a'}}]}]
        sections = self.blitz_obj._discover()
        self.kwargs = {'self': self.blitz_obj,
                       'section': sections[0],
                       'name': ''}


    def test_configure(self):

        self.dev.configure = Mock(side_effect=['passing cmd'])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'conf t'})

        configure(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_configure_with_exception(self):

        self.dev.configure = Mock(side_effect = Exception)
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'conf t'})

        output = configure(**self.kwargs)
        self.assertEqual(output, None)
        self.assertEqual(steps.result, Failed)

    def test_configure_expected_failure(self):

        self.dev.configure = Mock(side_effect = Exception)
        steps = Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'conf t',
                            'expected_failure': True})

        configure(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_configure_reply(self):

        self.dev.configure = Mock(side_effect=['passing cmd'])
        steps = Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'conf t',
                            'expected_failure': True,
                            'reply': [{'pattern': '.*',
                                       'action': 'sendline(y)'}]})

        configure(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_configure_dual_pass(self):

        self.dev.configure_dual = Mock(side_effect=['passing cmd'])
        steps = Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'action': 'configure_dual',
                            'command': 'conf t\ncommit'})

        configure_dual(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_configure_dual_failure(self):

        self.dev.configure_dual = Mock(side_effect=Exception)
        steps = Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'action': 'configure_dual',
                            'command': 'conf t\ncommit'
                            })

        configure_dual(**self.kwargs)
        self.assertEqual(steps.result, Failed)

    def test_parse(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd'})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_parse_with_arguments(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'arguments': {'output': 'sample device output'}})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_parse_empty_parser(self):

        self.dev.parse = Mock(side_effect = SchemaEmptyParserError(data=''))
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd'})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_parse_empty_parser_with_include(self):

        self.dev.parse = Mock(side_effect = SchemaEmptyParserError(data=''))
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'include': ["contains('software')"
                               ".get_values('system_image_file', 0)"]})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Failed)

    def test_parse_include_pass(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'include': ["contains('software')"
                               ".get_values('system_image_file', 0)"]})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_parse_include_fail(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'include': ["contains('sas')"
                               ".get_values('system_image_file', 0)"]})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Failed)

    def test_parse_exclude_pass(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'exclude':["contains('softwaress')"
                               ".get_values('system_image_file', 0)"]})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_parse_exclude_fail(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'exclude':["contains('software')"
                               ".get_values('system_image_file', 0)"]})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Failed)

    def test_parse_expected_failure_fail(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'expected_failure': True})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Failed)

    def test_parse_expected_failure_pass(self):

        self.dev.parse = Mock(side_effect = [self.parser_output])
        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'command': 'cmd',
                            'include':["contains('softwaress')"
                                     ".get_values('system_image_file', 0)"],
                            'expected_failure':True})

        parse(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_execute(self):

      self.dev.execute = Mock(side_effect = [self.execute_output])
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'command': 'cmd'})

      execute(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_execute_fail(self):

      self.dev.execute = Mock(side_effect = Exception)
      steps = Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'command': 'cmd'})

      execute(**self.kwargs)
      self.assertEqual(steps.result, Failed)

    def test_execute_include_pass(self):

      self.dev.execute = Mock(side_effect = [self.execute_output])
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'command': 'cmd',
                          'include': ['\d']})

      execute(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_execute_include_fail(self):

      self.dev.execute = Mock(side_effect=[self.execute_output])
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'command': 'cmd',
                          'include': ['90909099']})

      output = execute(**self.kwargs)
      self.assertEqual(steps.result, Failed)

    def test_execute_exclude(self):

      self.dev.execute = Mock(side_effect = [self.execute_output])
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'command': 'cmd',
                          'exclude': ['TESTSTSTS']})

      execute(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_execute_expected_failure_fail(self):

      self.dev.execute = Mock(side_effect = [self.execute_output])
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'command': 'cmd',
                          'expected_failure': True})

      execute(**self.kwargs)
      self.assertEqual(steps.result, Failed)

    def test_execute_expected_failure_pass(self):

      self.dev.execute = Mock(side_effect = Exception)
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'command': 'cmd',
                          'expected_failure': True})

      execute(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_learn(self):

      self.dev.learn = Mock(return_value = Platform(self.dev))
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'feature': 'platform'})

      learn(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_learn_config(self):

      self.dev.learn = Mock(return_value = self.learn_config_out)
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'feature': 'config'})

      learn(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_api_with_args(self):

      self.dev.api = Mock()
      self.dev.testbed = self.testbed
      self.dev.api.function.return_value = 'api output'
      arguments = {'a': 1, 'b': [1,2,34], 'device': 'PE1'}
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'function': 'function',
                          'arguments': arguments})

      api(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_api_with_empty_args(self):

      self.dev.api = Mock()
      self.dev.testbed = self.testbed
      self.dev.api.function.return_value = 'api output'
      arguments = {}
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'function': 'function',
                          'arguments': arguments})

      api(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_api_wrong_device(self):

      self.dev.api = Mock()
      self.dev.testbed = self.testbed
      self.dev.api.function.return_value = 'api output'
      arguments = {'a': 1, 'b': [1,2,34], 'device': 'R3_NX'}
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'function': 'function',
                          'arguments': arguments})

      api(**self.kwargs)
      self.assertEqual(steps.result, Errored)

    def test_api_no_device_common_api(self):

      arguments = {'testbed': self.testbed}
      steps =  Steps()
      self.kwargs.update({'steps': steps,
                          'function': 'get_devices',
                          'common_api': True,
                          'arguments': arguments})

      api(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_api_device_in_args_fail(self):

      self.dev.api = Mock()
      self.dev.testbed = self.testbed
      self.dev.api.function.return_value = 'api output'
      arguments = {'a': 1, 'b': [1,2,34], 'device': 'R3_NX'}
      steps =  Steps()
      self.kwargs.update({'steps': steps,
                          'function': 'function',
                          'arguments': arguments})

      api(**self.kwargs)
      self.assertEqual(steps.result, Errored)

    def test_api_no_device_in_args(self):

      self.dev.api = Mock()
      self.dev.testbed = self.testbed
      self.dev.api.function.return_value = 'api output'
      arguments = {'a': 1, 'b': [1,2,34]}
      steps =  Steps()
      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'function': 'function',
                          'arguments': arguments})

      api(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_api_expected_failure(self):

      self.dev.api = Mock()
      self.dev.testbed = self.testbed
      side_effects = [AttributeError, TypeError, Exception]
      self.dev.api.function.side_effect = side_effects
      arguments = {'a': 1, 'b': [1,2,34], 'device': 'PE1'}

      for _ in side_effects:

        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'function': 'function',
                            'arguments': arguments,
                            'expected_failure': True})

        arguments['device'] = 'PE1'
        api(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_api_fail(self):

      self.dev.api = Mock()
      self.dev.testbed = self.testbed
      side_effects = [AttributeError, TypeError, Exception]
      self.dev.api.function.side_effect = side_effects
      arguments = {'a': 1, 'b': [1,2,34], 'device': 'PE1'}

      for exception in side_effects:

        steps =  Steps()
        self.kwargs.update({'device': self.dev,
                            'steps': steps,
                            'function': 'function',
                            'arguments': arguments})

        arguments['device'] = 'PE1'
        api(**self.kwargs)
        if exception == Exception:
          self.assertEqual(steps.result, Failed)
        else:
          self.assertEqual(steps.result, Errored)

    def test_bash_console(self):

      dev = Connection(hostname='Router',
                       os='iosxr',
                       start = ['mock_device_cli --os iosxr --state enable1'],
                       username='root',
                       tacacs_password='lab')

      dev.name = 'anything'
      dev.custom = {}
      commands = ['cd ../common/', 'cd ../disk0']
      steps = Steps()
      self.kwargs.update({'device': dev,
                          'steps': steps,
                          'commands': commands})

      output = bash_console(**self.kwargs)
      self.assertEqual(steps.result, Passed)
      self.assertEqual(output, {'cd ../common/': 'new_state: bash_dir_console',
                                'cd ../disk0': 'new_state: bash_console'})

    def test_rest_pass(self):

      steps = Steps()
      self.dev.rest = Mock()
      self.dev.rest.post.side_effect = [{'imdata': []}]

      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'method': 'post',
                          'dn': '/api/mo/sys/bgp/inst/dom-default/af-ipv4-mvpn.json',
                          'payload': {}
                          })

      out = rest(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_rest_expected_failure(self):

      steps = Steps()
      self.dev.rest = Mock()
      self.dev.rest.post.side_effect = Exception

      self.kwargs.update({'device': self.dev,
                          'steps': steps,
                          'method': 'post',
                          'dn': '/api/mo/sys/bgp/inst/dom-default/af-ipv4-mvpn.json',
                          'payload': {},
                          'expected_failure': True
                          })

      out = rest(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_diff_pass(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'pre': {'a': 1, 'b':3},
                          'post': {'a': 1, 'b':3}})
      diff(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_diff_fail(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'pre': {'a': 1, 'b':3},
                          'post': {'a': 1, 'b':13},
                          'fail_different': True})
      diff(**self.kwargs)
      self.assertEqual(steps.result, Failed)

    def test_diff_exclude(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'pre': {'a': 1, 'b':3},
                          'post': {'a': 1, 'b':13},
                          'fail_different': True,
                          'exclude': ['b']})
      diff(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_configure_replace(self):

      self.kwargs.update({'config': "bootflash:/golden_config",
                          'steps': Steps(),
                          'device': self.dev
      })

      with patch(
                 "genie.libs.sdk.libs.abstracted_libs.restore.Restore.restore_configuration"
                 ) as func:

        configure_replace(**self.kwargs)
        func.assert_called_once()

    def test_save_config_snapshot_1(self):

      test_module = importlib.import_module('genie.harness.genie_testscript')
      script = TestScript(test_module)
      setattr(script, 'default_file_system', {'PE1', 'bootflash:/'})
      self.blitz_obj.parent = script
      steps = Steps()

      self.kwargs.update({'steps': steps,
                          'device': self.dev})

      with patch(
           "genie.libs.sdk.libs.abstracted_libs.restore.Restore.save_configuration"
           ) as func:

        save_config_snapshot(**self.kwargs)
        func.assert_called_once()
        self.assertEqual(steps.result, Passed)

    @patch("genie.libs.sdk.libs.abstracted_libs.iosxe.subsection.get_default_dir",
                return_value='bootflash:/')
    def test_save_config_snapshot_2(self, mock):

      test_module = importlib.import_module('genie.harness.genie_testscript')
      script = TestScript(test_module)
      setattr(script, 'default_file_system', {})
      self.blitz_obj.parent = script
      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'device': self.dev})

      with patch(
           "genie.libs.sdk.libs.abstracted_libs.restore.Restore.save_configuration"
           ) as func:

        save_config_snapshot(**self.kwargs)
        func.assert_called_once()
        self.assertEqual(steps.result, Passed)

    def test_restore_config_snapshot_error_1(self):

      test_module = importlib.import_module('genie.harness.genie_testscript')
      script = TestScript(test_module)
      setattr(script, 'default_file_system', {'PE1', 'bootflash:/'})
      self.blitz_obj.parent = script
      steps = Steps()

      with steps.start("Starting action", continue_=True) as step:

        self.kwargs.update({'steps': step,
                            'device': self.dev})
        restore_config_snapshot(**self.kwargs)

      self.assertEqual(steps.result, Errored)

    def test_restore_config_snapshot_error_2(self):

      test_module = importlib.import_module('genie.harness.genie_testscript')
      script = TestScript(test_module)
      self.blitz_obj.parent = script

      self.blitz_obj.restore = {
                                self.dev: sdk.libs.abstracted_libs.restore.Restore(
                                device=self.dev)}
      self.blitz_obj.restore[self.dev].snapshot_deleted = True
      steps = Steps()

      with steps.start("Starting action", continue_=True) as step:

        self.kwargs.update({'steps': step,
                            'device': self.dev})
        restore_config_snapshot(**self.kwargs)

      self.assertEqual(steps.result, Errored)

    def test_restore_config_snapshot_pass(self):

      test_module = importlib.import_module('genie.harness.genie_testscript')
      script = TestScript(test_module)
      self.blitz_obj.parent = script

      self.blitz_obj.restore = {
                                self.dev: sdk.libs.abstracted_libs.restore.Restore(
                                device=self.dev)}
      self.blitz_obj.restore[self.dev].snapshot_deleted = False
      self.blitz_obj.restore[self.dev].restore_configuration = Mock()
      self.blitz_obj.restore[self.dev].restore_configuration.side_effect = [None]
      steps = Steps()

      with steps.start("Starting action", continue_=True) as step:

        self.kwargs.update({'steps': step,
                            'device': self.dev})
        restore_config_snapshot(**self.kwargs)

      self.assertEqual(steps.result, Passed)

    def test_restore_config_snapshot_fail(self):

      test_module = importlib.import_module('genie.harness.genie_testscript')
      script = TestScript(test_module)
      self.blitz_obj.parent = script

      self.blitz_obj.restore = {
                                self.dev: sdk.libs.abstracted_libs.restore.Restore(
                                device=self.dev)}
      self.blitz_obj.restore[self.dev].snapshot_deleted = False
      self.blitz_obj.restore[self.dev].restore_configuration = Mock()
      self.blitz_obj.restore[self.dev].restore_configuration.side_effect = Exception
      steps = Steps()

      with steps.start("Starting action", continue_=True) as step:
        self.kwargs.update({'steps': step,
                            'device': self.dev})

        restore_config_snapshot(**self.kwargs)

      self.assertEqual(steps.result, Failed)

    def test_run_genie_sdk(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'TriggerSleep':{'devices':['PE1']}})

      with patch("genie.libs.sdk.triggers.blitz.actions.run_genie_sdk") as func:
        genie_sdk(**self.kwargs)
        func.assert_called_once()
        self.assertEqual(steps.result, Passed)

    def test_dq_query_include_pass(self):

      steps = Steps()
      kwargs = {'output': self.parser_output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["contains('software', regex=True)",
                            "get_values('system_version')"],
                'exclude': None,
                'continue_': True,
                'action': 'learn',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)

      for substep in steps.details:
        self.assertEqual(substep.result, Passed)

    def test_dq_query_include_fail(self):

      steps = Steps()
      kwargs = {'output': self.parser_output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["contains('software', regex=True)",
                            "get_values('s_verasadsad')",
                            "contains('hardware')"],
                'exclude': None,
                'continue_': True,
                'action': 'learn',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)

      self.assertEqual(steps.result, Failed)
      self.assertEqual(steps.details[0].result, Passed)
      self.assertEqual(steps.details[2].result, Passed)

    def test_string_query_1(self):

      steps = Steps()
      kwargs = {'output': 1500,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': [">= 1250"],
                'exclude': ["1789"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Passed)

    def test_string_query_2(self):

      steps = Steps()
      kwargs = {'output': 1150,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': [">= 1250"],
                'exclude': None,
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Failed)

    def test_string_query_3(self):

      steps = Steps()
      kwargs = {'output': 1150,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["<= 1250",],
                'exclude': None,
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Passed)

    def test_string_query_4(self):

      steps = Steps()
      kwargs = {'output': 1500,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["<= 1499"],
                'exclude': ["1789"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Failed)

    def test_string_query_with_range_1(self):

      steps = Steps()
      kwargs = {'output': 1500,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': [">= 870 && <= 1687"],
                'exclude': ["1499"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Passed)

    def test_string_query_with_range_exception_1(self):

      steps = Steps()
      kwargs = {'output': 1500,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["> 870 &&"],
                'exclude': ["1499"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      with self.assertRaises(Exception):
        _output_query_template(**kwargs)

    def test_string_query_with_range_exception_2(self):

      steps = Steps()
      kwargs = {'output': 1500,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': [ "<= 870 && < 909"],
                'exclude': ["1499"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      with self.assertRaises(Exception):
        _output_query_template(**kwargs)

    def test_string_query_with_range_exception_3(self):

      steps = Steps()
      kwargs = {'output': 1500,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["> 789 && < 788"],
                'exclude': ["1499"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      with self.assertRaises(Exception):
        _output_query_template(**kwargs)

    def test_string_query_with_range_2(self):

      steps = Steps()
      kwargs = {'output': 1500,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': [">= 870 && <= 1400"],
                'exclude': ["1499"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Failed)

    def test_string_query_with_dict_output(self):
        pass
      # TODO Investigate if with dict it does work. I am certain that it used to work
      # include = [{'we': 'are', 'testing': 'if', 'dict': ['input', 'works']}]
      # steps = Steps()
      # output = include

      # _output_query_template(self.blitz_obj,
      #                        output,
      #                        steps,
      #                        self.dev,
      #                        "command",
      #                        include,
      #                        exclude,
      #                        max_time,
      #                        check_interval,
      #                        continue_,
      #                        action)

      # self.assertEqual(steps.result, Passed)

    def test_string_query_with_list_output(self):

      steps = Steps()
      kwargs = {'output': [],
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': [['also', 'list', 'inputs']],
                'exclude': [['also', 'list', 'inputs']],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Failed)
      self.assertEqual(steps.details[1].result, Passed)

    def test_string_query_list_output_include_1(self):

      steps = Steps()
      output = [{'a': 1},
                {'d': {'c': 'name1'}},
                [1, 2, 34],
                {'e': ['a', 'b', 'c']}]

      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["{'d': {'c': 'name1'}}", "[1, 2, 34]"],
                'exclude': ["['also', 'list', 'inputs']"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Passed)

    def test_string_query_list_output_include_2(self):

      steps = Steps()
      output = [{'a': 1},
                {'d': {'c': 'name1'}},
                [1, 2, 34],
                {'e': ['a', 'b', 'c']}]

      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ['t'],
                'exclude': ["['also', 'list', 'inputs']"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Failed)

    def test_string_query_list_output_include_3(self):

      steps = Steps()
      output = ['string1', 'string2 and', 'bootflash:\\']
      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ['string1', 'bootflash.*'],
                'exclude': ["['also', 'list', 'inputs']"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Passed)

    def test_string_query_list_output_exclude_1(self):

      steps = Steps()
      output = ['string1', 'string2 and', 'bootflash:\\']
      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': None,
                'exclude': ['string1', 'bootflash.*'],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Failed)

    def test_string_query_list_output_exclude_2(self):

      steps = Steps()
      output = [{'a': 1},
                {'d': {'c': 'name1'}},
                [1, 2, 34],
                {'e': ['a', 'b', 'c']}]

      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': None,
                'exclude': ["{'a': 1}"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Failed)

    def test_string_query_list_output_exclude_3(self):

      steps = Steps()
      output = [{'a': 1},
                {'d': {'c': 'name1'}},
                [1, 2, 34],
                {'e': ['a', 'b', 'c']}]

      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': None,
                'exclude': ["{'a': 32}"],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Passed)

    def test_string_query_list_output_exclude_4(self):

      steps = Steps()
      output = output = ['string', 'string and', 'bootflash:\\']
      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': None,
                'exclude': ['\d'],
                'continue_': True,
                'action': 'api',
                'max_time': None,
                'check_interval': None}

      _output_query_template(**kwargs)
      self.assertEqual(steps.result, Passed)

    @patch("genie.libs.sdk.triggers.blitz.actions_helper._send_command")
    def test_query_resend_cmd_pass(self, mock_send_command):

      steps = Steps()
      output = {'platform': {'name': 'Nexus',
                           'os': 'NX-OS'}}
      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["contains('software', regex=True)"],
                'exclude': None,
                'continue_': True,
                'action': 'parse',
                'max_time': 23,
                'check_interval': 3}

      mock_send_command.side_effect = [output, output, self.parser_output]

      output = _output_query_template(**kwargs)
      self.assertEqual(output, self.parser_output)
      self.assertEqual(steps.result, Passed)

    @patch("genie.libs.sdk.triggers.blitz.actions_helper._send_command")
    def test_query_resend_cmd_fail(self, mock_send_command):

      steps = Steps()
      output = {'platform': {'name': 'Nexus',
                           'os': 'NX-OS'}}
      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': ["contains('software', regex=True)"],
                'exclude': None,
                'continue_': True,
                'action': 'parse',
                'max_time': 8,
                'check_interval': 5}

      mock_send_command.side_effect = [output, output, output]

      output = _output_query_template(**kwargs)
      self.assertEqual(output, output)
      self.assertEqual(steps.result, Failed)

    @patch("genie.libs.sdk.triggers.blitz.actions_helper._send_command")
    def test_str_query_resend_cmd(self, mock_send_command):

      steps = Steps()
      output = "This is a sample output with T$p in iit"
      kwargs = {'output': output,
                'steps': steps,
                'device': self.dev,
                'command': 'command',
                'include': None,
                'exclude':["T\$p"],
                'continue_': True,
                'action': 'execute',
                'max_time': 14,
                'check_interval': 3}

      mock_send_command.side_effect = [output, output, self.execute_output]

      output = _output_query_template(**kwargs)
      self.assertEqual(output, self.execute_output)
      self.assertEqual(steps.result, Passed)

    def test_compare(self):
      steps = Steps()
      items = [
         "738746 > 1000",
         "'w' == 'w' and ('ac' == 'ac' or (2 == 2 and 3 != 3 ))",
         "3 == 3 and 2 !=1 ",
         "3 == 3 and 2 ==1 ",
         "'default' == 'default' and '2.2.2.2/32' == '2.2.2.2/32' and '3' == '3' and ('10.0.0.2' == '10.0.0.2' or '10.0.0.2' == '10.0.1.2' or '10.0.0.2' == '10.0.2.2') and 'static' == 'static' and ('10.0.1.2' == '10.0.1.2' or '10.0.1.2' == '10.0.0.2' or '10.0.1.2' == '10.0.2.2') and 'static' == 'static' and ('10.0.2.2' == '10.0.2.2' or '10.0.2.2' == '10.0.0.2' or '10.0.2.2' == '10.0.1.2') and 'static' == 'static'",
         "'default' == 'default' and '2.2.2.2/32' == '2.2.2.2/32' and '3' == '3' and ('10.0.0.2' == '10.0.0.2' or '10.0.0.2' == '10.0.1.2' or '10.0.0.2' == '10.0.2.2') and 'ospf-1' == 'ospf-1' and ('Eth1/1' == 'Eth1/1' or 'Eth1/1' == 'Eth1/4' or 'Eth1/1' == 'Eth1/16') and 'intra' == 'intra' and ('10.0.1.2' == '10.0.0.2' or '10.0.1.2' == '10.0.1.2' or '10.0.1.2' == '10.0.2.2') and 'ospf-1' == 'ospf-1' and ('Eth1/4' == 'Eth1/1' or 'Eth1/4' == 'Eth1/4' or 'Eth1/4' == 'Eth1/16') and 'intra' == 'intra' and ('10.0.2.2' == '10.0.2.2' or '10.0.2.2' == '10.0.0.2' or '10.0.2.2' == '10.0.1.2') and 'ospf-1' == 'ospf-1' and ('Eth1/16' == 'Eth1/1' or 'Eth1/16' == 'Eth1/4' or 'Eth1/16' == 'Eth1/16') and 'intra' == 'intra'",
         "'default' == 'default' and '2.2.2.2/32' == '2.2.2.2/32' and '3' == '3' and ('10.0.0.2' == '10.0.0.2' or '10.0.0.2' == '10.0.1.2' or '10.0.0.2' == '10.0.2.2') and 'isis-1' == 'isis-1' and ('Eth1/1' == 'Eth1/1' or 'Eth1/1' == 'Eth1/4' or 'Eth1/1' == 'Eth1/16') and 'L2' == 'L2' and ('10.0.1.2' == '10.0.1.2' or '10.0.1.2' == '10.0.0.2' or '10.0.1.2' == '10.0.2.2') and 'isis-1' == 'isis-1' and ('Eth1/4' == 'Eth1/4' or 'Eth1/4' == 'Eth1/1' or 'Eth1/4' == 'Eth1/16') and 'L2' == 'L2' and ('10.0.2.2' == '10.0.2.2' or '10.0.2.2' == '10.0.0.2' or '10.0.2.2' == '10.0.1.2') and 'isis-1' == 'isis-1' and ('Eth1/16' == 'Eth1/16' or 'Eth1/16' == 'Eth1/4' or 'Eth1/16' == 'Eth1/1') and 'L2' == 'L2'",
         "'default' == 'default' and '2.2.2.2/32' == '2.2.2.2/32' and '3' == '3' and ('10.0.2.2' == '10.0.1.2' or '10.0.2.2' == '10.0.0.2' or '10.0.2.2' == '10.0.2.2') and 'bgp-1' == 'bgp-1' and '2' == '2' and 'external' == 'external' and ('10.0.1.2' == '10.0.0.2' or '10.0.1.2' == '10.0.1.2' or '10.0.1.2' == '10.0.2.2') and 'bgp-1' == 'bgp-1' and '2' == '2' and 'external' == 'external' and ('10.0.0.2' == '10.0.2.2' or '10.0.0.2' == '10.0.1.2' or '10.0.0.2' == '10.0.0.2') and 'bgp-1' == 'bgp-1' and '2' == '2' and 'external' == 'external'",
         "'default' == 'default' and '10.0.0.0/8' == '10.0.0.0/8' and '20.20.8.2/32' == '20.20.8.2/32' and 'static' == 'static' and '20.20.8.2' == '20.20.8.2'",
         "'default' == 'default' and '2.2.2.2/32' == '2.2.2.2/32' and '3' == '3' and ('10.0.0.2' == '10.0.0.2' and '10.0.0.2' == '10.0.1.2' and '10.0.0.2' == '10.0.2.2') and 'ospf-1' == 'ospf-1' and ('Eth1/1' == 'Eth1/1' or 'Eth1/1' == 'Eth1/4' or 'Eth1/1' == 'Eth1/16') and 'intra' == 'intra' and ('10.0.1.2' == '10.0.0.2' or '10.0.1.2' == '10.0.1.2' or '10.0.1.2' == '10.0.2.2') and 'ospf-1' == 'ospf-1' and ('Eth1/4' == 'Eth1/1' or 'Eth1/4' == 'Eth1/4' or 'Eth1/4' == 'Eth1/16') and 'intra' == 'intra' and ('10.0.2.2' == '10.0.2.2' or '10.0.2.2' == '10.0.0.2' or '10.0.2.2' == '10.0.1.2') and 'ospf-1' == 'ospf-1' and ('Eth1/16' == 'Eth1/1' or 'Eth1/16' == 'Eth1/4' or 'Eth1/16' == 'Eth1/16') and 'intra' == 'intra'"
     ]
      list_of_results = [Passed, Passed, Passed,
                        Failed,Passed, Passed, Passed,
                        Passed, Passed, Failed]

      self.kwargs.update({'items': items,
                          'steps': steps})
      compare(**self.kwargs)

      for index, val in enumerate(list_of_results):
        self.assertEqual(steps.details[index].result, val)

    def test_compare_no_items(self):
      steps = Steps()

      with steps.start("Starting action", continue_=True) as step:

        self.kwargs.update({'steps': step, 'items': []})
        compare(**self.kwargs)
        self.assertEqual(step.result, Failed)

    def test_sleep(self):

      steps = Steps()

      with steps.start("Starting action") as step:

        self.kwargs.update({'steps': steps, 'sleep_time': 5})
        sleep(**self.kwargs)
        self.assertEqual(step.result, Passed)

    def test_print(self):

      steps = Steps()
      print_dict = {'name1': {'value': 'print any', 'type': 'banner'},
                    'name2': {'value': 'print any without banner'},
                    'steps': steps}

      with steps.start("Starting action") as step:

        self.kwargs.update(print_dict)
        print_(**self.kwargs)
        self.assertEqual(step.result, Passed)


if __name__ == '__main__':
    unittest.main()
