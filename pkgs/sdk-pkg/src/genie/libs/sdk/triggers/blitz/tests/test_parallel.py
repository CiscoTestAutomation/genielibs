#! /usr/bin/env python
import os
import yaml
import tempfile
import unittest
import importlib
from unittest import mock
from unittest.mock import patch

from genie.testbed import load
from genie.conf.base import Testbed, Device
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.sdk.triggers.blitz.actions import actions
from genie.libs.ops.platform.nxos.platform import Platform
from genie.libs.sdk.triggers.blitz.advanced_actions import parallel
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from pyats.easypy import Task
from pyats.easypy.job import Job
from pyats.easypy import runtime
from pyats.aetest.steps import Steps
from pyats.aetest.parameters import ParameterMap
from pyats.easypy.tests.common_funcs import init_runtime
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked


class TestParallel(unittest.TestCase):

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

    yaml1 = """ 
            - configure:
                command: feature bgp
                device: PE1
                save:
                  - variable_name: conf1
                description: expected_failure is True passed as a result
            - execute:
                alias: execute_id
                command: show version
                device: PE1
                exclude:
                    - extreme
                include:
                    - host
            - parse:
                command: command
                device: PE1
                include:
                    - contains('software')
                    - get_values('hardware', 0)
            """

    yaml2 = """ 
            - configure:
                command: feature bgp
                device: PE1
                save:
                  - variable_name: conf1
                description: expected_failure is True passed as a result
            - execute:
                alias: execute_id
                command: show version
                device: PE1
                include:
                    - extreme
            """
    yaml3 = """ 
            - run_condition:
                if : "%VARIABLES{execute_id} == passed"
                function: failed
                actions:
                    - loop:
                        loop_variable_name: var_name
                        value: ['show vrf', 'show version']
                        loop_until: failed
                        actions:
                          - execute:
                                alias: exec_1
                                device: PE1
                                command: "%VARIABLES{var_name}"
                          - execute:
                                alias: exec_2
                                device: PE2
                                command: "%VARIABLES{var_name}"
                    - loop:
                         loop_variable_name: var_name
                         value: ['show vrf', 'show version']
                         actions:
                           - configure:
                                 device: PE1
                                 command: feature bgp
                           - execute:
                                 device: PE1
                                 command: "%VARIABLES{var_name}"
            - loop:
                loop_variable_name: dev_name
                value: ['PE1','PE2']
                loop_until: passed
                actions:
                    - parse:
                          alias: parse_lopp_w
                          save:
                            - variable_name: parse32
                              filter: contains('hardware')
                          device: "%VARIABLES{dev_name}"
                          command: show version
                    - execute:
                          alias: id
                          device: "%VARIABLES{dev_name}"
                          command: show vrf
            - loop:
                loop_variable_name: dev_name
                value: ['PE1','PE2']
                actions:
                    - execute:
                          device: "%VARIABLES{dev_name}"
                          command: show version
                    - execute:
                          device: "%VARIABLES{dev_name}"
                          command: show version
            - parse:
                alias: parse_id
                command: command
                device: PE1
                include:
                    - contains('software')
                    - get_values('hardware', 0)
            """

    def setUp(self):

      dir_name = os.path.dirname(os.path.abspath(__file__))

      f, self.jobfile = tempfile.mkstemp()
      init_runtime(runtime)
      runtime.configuration.load()
      runtime.job = Job(jobfile = self.jobfile,
                        runtime = runtime,
                        **runtime.configuration.components.job)

      mgr = runtime.tasks
      task = mgr.Task(testscript = os.path.join(dir_name, 'mock_yamls/trigger_datafile.yaml'),
                      taskid = 'awesome')

      self.testbed = load(os.path.join(dir_name, 'mock_testbeds/testbed.yaml'))
      self.mock_testbed_devs()
      Blitz.parameters = ParameterMap()
      Blitz.uid = 'test.dev'
      Blitz.parameters['testbed'] = self.testbed

      self.blitz_obj = Blitz()

      self.blitz_obj.parameters['test_sections'] = [
                               {'section1': [{'parallel': [{'action': {'arg1':'cmd'}}]}]}
                               ]
      sections = self.blitz_obj._discover()
      
      self.kwargs = {'self': self.blitz_obj,
                     'testbed': self.testbed,
                     'section': sections[0].__testcls__(sections[0]),
                     'name': ''}

    def mock_testbed_devs(self):

      side_effects = {'configure': ['\n'],
                'execute': ['host execute output', 'oop', 'oot', 'name'],
                'parse': [self.parser_output]}

      for dev in self.testbed.devices:
        for action in side_effects.keys():
            setattr(self.testbed.devices[dev], action, mock.Mock())
            setattr(getattr(self.testbed.devices[dev], action),
                            'side_effect', side_effects[action])

    def test_parallel_actions_pass(self):

      steps = Steps()
      data = yaml.safe_load(self.yaml1)
      self.kwargs.update({'data': data, 'steps': steps})
      parallel(**self.kwargs)
      self.assertIn('execute_id', self.blitz_obj.parameters['save_variable_name'])
      self.assertEqual(steps.result, Passed)
      self.assertEqual(self.blitz_obj.parameters['save_variable_name']['execute_id'], 'passed')

    def test_parallel_actions_fail(self):

      steps = Steps()
      data = yaml.safe_load(self.yaml2)
      self.kwargs.update({'data': data, 'steps': steps})
      parallel(**self.kwargs)
      self.assertEqual(steps.result, Failed)
      self.assertEqual(self.blitz_obj.parameters['save_variable_name']['execute_id'], 'failed')

    def test_parallel_loops(self):

      steps = Steps()
      data = yaml.safe_load(self.yaml3)
      self.blitz_obj.parameters['save_variable_name'] = {}
      self.blitz_obj.parameters['save_variable_name']['execute_id'] = 'passed'
      self.kwargs.update({'self': self.blitz_obj, 
                          'data': data, 
                          'steps': steps})
      
      # TODO alias and saved_vars wont get stored when under loop/run_condition 
      # self.assertIn('exec_1', self.blitz_obj.parameters['save_variable_name'])
      parallel(**self.kwargs)
      self.assertIn('parse_id', self.blitz_obj.parameters['save_variable_name']) 
      self.assertEqual(steps.result, Failed)
      self.assertEqual(steps.details[0].name, 'Executing actions in parallel')
      self.assertEqual(steps.details[1].name, 
                       'Condition %VARIABLES{execute_id} == passed is met and '
                       'the step result is failed')
      self.assertEqual(steps.details[1].result, Failed)

if __name__ == '__main__':
    unittest.main()
