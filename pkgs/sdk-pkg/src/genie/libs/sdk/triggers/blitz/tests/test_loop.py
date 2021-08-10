#! /usr/bin/env python
import os
import sys
import yaml
import logging
import tempfile
import unittest
import importlib
from unittest import mock
from unittest.mock import patch

from genie.testbed import load
from genie.conf.base.api import API
from genie.conf.base import Testbed, Device
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.sdk.triggers.blitz.actions import actions
from genie.libs.sdk.triggers.blitz.advanced_actions import loop
from genie.libs.sdk.triggers.blitz.markup import get_variable
from genie.libs.ops.platform.nxos.platform import Platform
from genie.metaparser.util.exceptions import SchemaEmptyParserError


from pyats.easypy import Task
from pyats.easypy.job import Job
from pyats.easypy import runtime
from pyats.aetest.steps import Steps
from pyats.aetest.parameters import ParameterMap
from pyats.easypy.common_funcs import init_runtime
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked



def check_maple_env():
  if not os.environ.get('MAPLE_PATH'):
     return True

  if os.environ['MAPLE_PATH'] not in sys.path:
    sys.path.append(os.environ['MAPLE_PATH'])

  return False

class TestLoop(unittest.TestCase):

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

    loop_with_val = """
            loop_variable_name: var_name
            value: ['show version', 'show vrf']
            actions:
              - execute:
                  alias: execute_id
                  command: "%VARIABLES{var_name}"
                  device: PE1
                  exclude:
                      - extreme
                  include:
                      - host
              - parse:
                  command: "%VARIABLES{var_name}"
                  device: PE1
            """
    loop_over_device = """
            loop_variable_name: dev_name
            value: ['PE1', 'PE2']
            actions:
              - configure:
                  command: feature bgp
                  device: "%VARIABLES{dev_name}"
            """

    loop_with_until = """
            until: "'%VARIABLES{nbc}' == '07.33'"
            maxtime: 5
            actions:
              - parse:
                  command: "show version"
                  save:
                    - variable_name: nbc
                      filter: get_values('bios_version', 0)
                  device: PE1
        """

    loop_with_do_until_1 = """
            do_until: "'%VARIABLES{nbc}' == '07.33'"
            max_time: 5
            actions:
              - parse:
                  command: "show version"
                  save:
                    - variable_name: nbc
                      filter: get_values('bios_version', 0)
                  device: PE1
        """

    loop_with_do_until_2 = """
            do_until: "'%VARIABLES{nbc}' == '06.33'"
            max_time: 2
            actions:
              - parse:
                  command: "show version"
                  save:
                    - variable_name: nbc
                      filter: get_values('bios_version', 0)
                  device: PE1
        """

    loop_with_dict_val = """
            loop_variable_name: var_name
            value: {'PE1':'show version', 'PE2': 'show version'}
            actions:
              - execute:
                  alias: execute_id
                  command: "%VARIABLES{var_name._values}"
                  device: "%VARIABLES{var_name._keys}"
                  exclude:
                      - extreme
                  include:
                      - host
            """
    loop_until = """
            loop_variable_name: var_name
            value: ['cmd', 'amd', 'show vrf']
            loop_until: passed
            actions:
              - execute:
                  command: "%VARIABLES{var_name}"
                  device: PE1
            """

    loop_until_custom_msg = """
            loop_variable_name: var_name
            value: ['cmd', 'amd', 'show vrf']
            custom_substep_message: test_message
            loop_until: passed
            actions:
              - execute:
                  command: "%VARIABLES{var_name}"
                  device: PE1
            """

    loop_until_custom_msg_var = """
            loop_variable_name: var_name
            value: ['cmd', 'amd', 'show vrf']
            loop_until: passed
            custom_substep_message: "message with %VARIABLES{var_name}"
            actions:
              - execute:
                  command: "%VARIABLES{var_name}"
                  device: PE1
            """

    loop_parallel = """
            loop_variable_name: dev_name
            value: ['PE1', 'PE2']
            parallel: True
            actions:
              - execute:
                  command: show version
                  device: "%VARIABLES{dev_name}"
            """
    loop_parallel_error = """
            loop_variable_name: dev_name
            value: ['PE', 'PE2']
            parallel: True
            actions:
              - execute:
                  command: show version
          """

    loop_nested = """
          range: 2
          loop_variable_name: nest_loop
          actions:
              - parse:
                  device: PE2
                  command: show version
              - loop:
                  loop_variable_name: var_name
                  value: ['show vrf', 'show version']
                  actions:
                      - execute:
                            device: PE1
                            command: "%VARIABLES{var_name}"
    """

    loop_range = """
            range: 1,5
            loop_variable_name: range
            actions:
                - execute:
                    device: PE1
                    command: show version
                - print:
                    item:
                      value: "%VARIABLES{range}"
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
      self.mock_testbed_devices()
      Blitz.parameters = ParameterMap()
      Blitz.uid = 'test.dev'
      Blitz.parameters['testbed'] = self.testbed

      self.blitz_obj = Blitz()
      self.uid = self.blitz_obj.uid
      self.blitz_obj.parent = self
      self.blitz_obj.parent.parameters = mock.Mock()

      self.dev = Device( name='PE1', os='iosxe')
      self.dev.custom = {'abstraction': {'order': ['os']}}
      self.blitz_obj.parameters['test_sections'] = [{'section1': [{'execute': {'command': 'cmd', 'device': 'PE1'}}]}]
      sections = self.blitz_obj._discover()
      self.kwargs = {'self': self.blitz_obj,
                     'testbed': self.testbed,
                     'section': sections[0].__testcls__(sections[0]),
                     'name': ''}

    def mock_testbed_devices(self):

      side_effects = {'configure': ['\n', 'end'],
                      'execute': ['host execute output', 'oop', 'oot', 'name'],
                      'parse': [self.parser_output, 'any output']}

      for dev in self.testbed.devices:
        for action in side_effects.keys():
            setattr(self.testbed.devices[dev], action, mock.Mock())
            setattr(getattr(self.testbed.devices[dev], action), 'side_effect', side_effects[action])

    def test_loop_init(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_with_val)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      expected = {
         "action":"loop",
         "step_result":Failed,
         "substeps":[
            {
               "device":"PE1",
               "continue_":True,
               "action":"execute",
               "description":"",
               "step_result":Passed,
               "alias":"execute_id",
               "saved_vars":{
                  "execute_id":"passed"
               }
            },
            {
               "device":"PE1",
               "continue_":True,
               "action":"parse",
               "description":"",
               "step_result":Passed,
               "alias":None,
               "saved_vars":{

               }
            },
            {
               "device":"PE1",
               "continue_":True,
               "action":"execute",
               "description":"",
               "step_result":Failed,
               "alias":"execute_id",
               "saved_vars":{
                  "execute_id":"failed"
               }
            },
            {
               "device":"PE1",
               "continue_":True,
               "action":"parse",
               "description":"",
               "step_result":Passed,
               "alias":None,
               "saved_vars":{

               }
            }
         ],
         "advanced_action":True,
         "loop_until":None
      }

      self.assertEqual(out, expected)
      self.assertEqual(steps.result, Failed)
      self.assertEqual(steps.details[2].result, Passed)

    def test_loop_over_device(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_over_device)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      expected =  {
         "action":"loop",
         "step_result":Passed,
         "substeps":[
            {
               "device":"PE1",
               "continue_":True,
               "action":"configure",
               "description":"",
               "step_result":Passed,
               "alias":None,
               "saved_vars":{

               }
            },
            {
               "device":"PE2",
               "continue_":True,
               "action":"configure",
               "description":"",
               "step_result":Passed,
               "alias":None,
               "saved_vars":{

               }
            }
         ],
         "advanced_action":True,
         "loop_until":None
      }

      self.assertEqual(out, expected)
      self.assertEqual(steps.result, out['step_result'])

    def test_until_condition_false(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_with_until)
      self.blitz_obj.parameters.setdefault('save_variable_name', {})
      self.blitz_obj.parameters['save_variable_name']['nbc'] = '06.33'
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      expected =[
                  {'device': 'PE1',
                   'continue_': True,
                    'action': 'parse',
                    'description': '',
                    'step_result': Passed,
                    'alias': None,
                    'saved_vars': {
                       'nbc': '07.33'
                      },
                    'filters': "get_values('bios_version', 0)"
                  }
              ]

      func = self.testbed.devices['PE1'].parse
      func.assert_called_once()
      self.assertEqual(out['substeps'], expected)
    def test_until_condition_true(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_with_until)
      self.blitz_obj.parameters.setdefault('save_variable_name', {})
      self.blitz_obj.parameters['save_variable_name']['nbc'] = '07.33'
      self.kwargs.update({'self': self.blitz_obj,
                          'steps': steps,
                          'action_item': data})

      out = loop(**self.kwargs)

      func = self.testbed.devices['PE1'].parse
      func.assert_not_called()
      self.assertEqual(out['substeps'], [])

    def test_do_until_condition_true(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_with_do_until_1)
      self.blitz_obj.parameters.setdefault('save_variable_name', {})
      self.blitz_obj.parameters['save_variable_name']['nbc'] = '07.33'
      self.kwargs.update({'self': self.blitz_obj,
                          'steps': steps,
                          'action_item': data})

      out = loop(**self.kwargs)
      expected ={
         "action":"loop",
         "step_result": Passed,
         "substeps":[
            {
               "device":"PE1",
               "continue_":True,
               "action":"parse",
               "description":"",
               "step_result": Passed,
               "alias":None,
               "saved_vars":{
                  "nbc":"07.33"
               },
               "filters":"get_values('bios_version', 0)"
            }
         ],
         "advanced_action":True,
         "loop_until":None
      }

      func = self.testbed.devices['PE1'].parse
      func.assert_called_once()
      self.assertEqual(out, expected)

    # def test_do_until_condition_false(self):

    #   steps = Steps()
    #   data = yaml.safe_load(self.loop_with_do_until_2)
    #   self.blitz_obj.parameters.setdefault('save_variable_name', {})
    #   self.blitz_obj.parameters['save_variable_name']['nbc'] = '07.33'
    #   self.kwargs.update({'self': self.blitz_obj,
    #                       'steps': steps,
    #                       'action_item': data})

    #   out = loop(**self.kwargs)
    #   # TODO - The saved_vars on the second action should be like below,
    #   # But it saves nbc: any_output Investigate
    #   expected = {
    #      "substeps":[
    #         {
    #            "device":"PE1",
    #            "continue_":True,
    #            "action":"parse",
    #            "description":"",
    #            "step_result":Passed,
    #            "alias":None,
    #            "saved_vars":{
    #               "nbc":"07.33"
    #            },
    #            "filters":"get_values('bios_version', 0)"
    #         },
    #         {
    #            "device":"PE1",
    #            "continue_":True,
    #            "action":"parse",
    #            "description":"",
    #            "step_result":Passed,
    #            "alias":None,
    #            "saved_vars":{},
    #            "filters":"get_values('bios_version', 0)"
    #         }
    #      ]
    #   }

    #   self.assertEqual(out, expected)

    def test_loop_with_dict_val(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_with_dict_val)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      self.assertEqual(len(out['substeps']), 2)
      self.assertEqual(out['substeps'][0]['device'], 'PE1')
      self.assertEqual(out['substeps'][1]['device'], 'PE2')

    def test_loop_everyseconds(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_with_dict_val)
      self.kwargs.update({'steps': steps, 'action_item': data})

      out = loop(**self.kwargs)
      self.assertEqual(len(out['substeps']), 2)
      self.assertEqual(out['substeps'][0]['device'], 'PE1')
      self.assertEqual(out['substeps'][1]['device'], 'PE2')

    def test_loop_with_loop_until(self):

      self.testbed.devices['PE1'].side_effect = [Exception, Exception, 'oop']
      steps = Steps()
      data = yaml.safe_load(self.loop_until)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      self.assertEqual(out['substeps'], [])
      self.assertEqual(steps.result, Passed)

    def test_loop_until_custom_substep_message(self):

      self.testbed.devices['PE1'].side_effect = [Exception, Exception, 'oop']
      steps = Steps()
      data = yaml.safe_load(self.loop_until_custom_msg)
      self.assertEqual(data['custom_substep_message'], 'test_message')
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      self.assertEqual(out['substeps'], [])
      self.assertEqual(steps.result, Passed)

    def test_loop_with_parallel(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_parallel)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_loop_with_parallel_errored(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_parallel_error)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      self.assertEqual(steps.result, Errored)

    def test_nested_loop(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_nested)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_loop_range(self):

      steps = Steps()
      data = yaml.safe_load(self.loop_range)
      self.kwargs.update({'steps': steps, 'action_item': data})
      out = loop(**self.kwargs)
      self.assertEqual(steps.result, Passed)


if __name__ == '__main__':
    unittest.main()