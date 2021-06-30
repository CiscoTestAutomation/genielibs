#! /usr/bin/env python
import os
import yaml
import tempfile
import unittest
from unittest import mock
from unittest.mock import patch

from genie.testbed import load
from genie.conf.base import Device
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.sdk.triggers.blitz.actions import actions
from genie.libs.sdk.triggers.blitz.advanced_actions import run_condition

from pyats.easypy import Task
from pyats.easypy.job import Job
from pyats.easypy import runtime
from pyats.aetest.steps import Steps
from pyats.aetest.parameters import ParameterMap
from pyats.easypy.common_funcs import init_runtime
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked


class TestCondition(unittest.TestCase):

    parser_output = {
        'platform': {
            'name': 'Nexus',
            'os': 'NX-OS',
            'software': {
                'bios_version': '07.33',
                'system_version': '9.3(3) [build 9.3(3)IDI9(0.509)]',
                'bios_compile_time': '08/04/2015',
                'system_image_file':
                'bootflash:///system-image-N93_3-00613722415136',
                'system_compile_time':
                '10/22/2019 10:00:00 [10/22/2019 16:57:31]'
            },
            'hardware': {
                'model': 'Nexus9000 C9396PX',
                'chassis': 'Nexus9000 C9396PX',
                'slots': 'None',
                'rp': 'None',
                'cpu': 'Intel(R) Core(TM) i3- CPU @ 2.50GHz',
                'memory': '16399900 kB',
                'processor_board_id': 'SAL1914CNL6',
                'device_name': 'N93_3',
                'bootflash': '51496280 kB'
            },
            'kernel_uptime': {
                'days': 61,
                'hours': 22,
                'minutes': 8,
                'seconds': 40
            },
            'reason': 'Reset Requested by CLI command reload',
            'system_version': '9.3(3)'
        }
    }

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

    condition_1 = """
          if : "%VARIABLES{execute_id} == id1"
          function: failed
          actions:
              - execute:
                    alias: exec_1
                    device: PE1
                    command: cmd
              - execute:
                    alias: exec_2
                    device: PE2
                    command: another
              - configure:
                    device: PE1
                    command: feature bgp
              - execute:
                    device: PE1
                    command: aa
    """

    condition_2 = """
          if : "%VARIABLES{execute_id} == id2"
          function: failed
          actions:
              - execute:
                    alias: exec_1
                    device: PE1
                    command: cmd
              - execute:
                    alias: exec_2
                    device: PE2
                    command: another
              - configure:
                    device: PE1
                    command: feature bgp
              - execute:
                    device: PE1
                    command: aa
    """

    condition_3 = """
          if : "%VARIABLES{execute_id} == id1"
          function: passed
          actions:
              - parallel:
                - execute:
                      alias: exec_1
                      device: PE1
                      command: cmd
                - execute:
                      alias: exec_2
                      device: PE2
                      command: another
                - configure:
                      device: PE1
                      command: feature bgp
                - execute:
                      device: PE1
                      command: aa
    """

    condition_4 = """

          if : "%VARIABLES{execute_id} == id1"
          actions:
            - parallel:
                - execute:
                      alias: exec_1
                      device: PE1
                      command: cmd
                - execute:
                      alias: exec_2
                      device: PE2
                      command: another
                - configure:
                      device: PE1
                      command: feature bgp
                - execute:
                      device: PE1
                      command: aa
    """

    condition_5 = """

          if : "%VARIABLES{execute_id} == id1"
          actions:
            - execute:
                  alias: exec_1
                  device: PE1
                  command: cmd
            - execute:
                  alias: exec_2
                  device: PE2
                  command: another
            - configure:
                  device: PE1
                  command: feature bgp
            - execute:
                  device: PE1
                  command: aa
    """

    condition_6 = """
          if : "%VARIABLES{nonexist}"
          actions:
            - execute:
                  alias: exec_1
                  device: PE1
                  command: cmd
            - execute:
                  alias: exec_2
                  device: PE2
                  command: another
            - configure:
                  device: PE1
                  command: feature bgp
            - execute:
                  device: PE1
                  command: aa
    """

    condition_7 = """
          if : "%VARIABLES{nonexist} == None"
          actions:
            - execute:
                  alias: exec_1
                  device: PE1
                  command: cmd
            - execute:
                  alias: exec_2
                  device: PE2
                  command: another
            - configure:
                  device: PE1
                  command: feature bgp
            - execute:
                  device: PE1
                  command: aa
    """

    def setUp(self):

        dir_name = os.path.dirname(os.path.abspath(__file__))

        f, self.jobfile = tempfile.mkstemp()
        init_runtime(runtime)
        runtime.configuration.load()
        runtime.job = Job(jobfile=self.jobfile,
                          runtime=runtime,
                          **runtime.configuration.components.job)

        mgr = runtime.tasks
        task = mgr.Task(testscript=os.path.join(
            dir_name, 'mock_yamls/trigger_datafile.yaml'),
                        taskid='awesome')

        self.testbed = load(
            os.path.join(dir_name, 'mock_testbeds/testbed.yaml'))
        self.mock_testbed_devices()
        Blitz.parameters = ParameterMap()
        Blitz.uid = 'test.dev'
        Blitz.parameters['testbed'] = self.testbed

        self.blitz_obj = Blitz()
        self.uid = self.blitz_obj.uid
        self.blitz_obj.parent = self
        self.blitz_obj.parent.parameters = mock.Mock()

        self.dev = Device(name='PE1', os='iosxe')
        self.dev.custom = {'abstraction': {'order': ['os']}}
        self.blitz_obj.parameters['test_sections'] = [{
            'section1': [{
                'execute': {
                    'command': 'cmd',
                    'device': 'PE1'
                }
            }]
        }]
        sections = self.blitz_obj._discover()
        self.kwargs = {
            'self': self.blitz_obj,
            'testbed': self.testbed,
            'section': sections[0].__testcls__(sections[0]),
            'name': ''
        }

    def mock_testbed_devices(self):

        side_effects = {
            'configure': ['\n', 'end'],
            'execute': ['host execute output', 'oop', 'oot', 'name'],
            'parse': [self.parser_output, 'any output']
        }

        for dev in self.testbed.devices:
            for action in side_effects:
                setattr(self.testbed.devices[dev], action, mock.Mock())
                setattr(getattr(self.testbed.devices[dev], action),
                        'side_effect', side_effects[action])

    # TODO maybe change the way condition is applied
    # need discussion
    def test_condition_pass(self):
        pass

    #   steps = Steps()
    #   data = yaml.safe_load(self.condition_1)
    #   self.kwargs.update({'steps': steps, 'action_item': data})
    #   self.blitz_obj.parameters['save_variable_name'] = {}
    #   self.blitz_obj.parameters['save_variable_name']['execute_id'] = 'id1'
    #   out = control(**self.kwargs)

    def test_condition_fail(self):

        steps = Steps()
        data = yaml.safe_load(self.condition_2)
        self.kwargs.update({'steps': steps, 'action_item': data})
        self.blitz_obj.parameters['save_variable_name'] = {'execute_id': 'id1'}
        run_condition(**self.kwargs)
        self.assertEqual(steps.result, Passed)

        func1 = self.testbed.devices['PE1'].configure
        func1.assert_called_once()
        func2 = self.testbed.devices['PE1'].execute
        self.assertEqual(func2.call_count, 2)
        func3 = self.testbed.devices['PE2'].execute
        func3.assert_called_once()

    def test_condition_parallel(self):

        steps = Steps()
        data = yaml.safe_load(self.condition_3)
        self.kwargs.update({'steps': steps, 'action_item': data})
        self.blitz_obj.parameters['save_variable_name'] = {'execute_id': 'id1'}
        run_condition(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_condition_no_function_pass(self):

        steps = Steps()
        data = yaml.safe_load(self.condition_5)
        self.kwargs.update({'steps': steps, 'action_item': data})
        self.blitz_obj.parameters['save_variable_name'] = {'execute_id': 'id1'}
        run_condition(**self.kwargs)
        self.assertEqual(steps.result, Passed)

    def test_condition_no_function_fail(self):

        steps = Steps()
        data = yaml.safe_load(self.condition_5)
        self.kwargs.update({'steps': steps, 'action_item': data})
        self.blitz_obj.parameters['save_variable_name'] = {'execute_id': 'id9'}
        out = run_condition(**self.kwargs)
        self.assertEqual(out['substeps'], [])
        self.assertEqual(out['run_condition_skipped'], True)

    def test_condition_no_function_parallel(self):

        steps = Steps()
        data = yaml.safe_load(self.condition_4)
        self.kwargs.update({'steps': steps, 'action_item': data})
        self.blitz_obj.parameters['save_variable_name'] = {'execute_id': 'id1'}
        out = run_condition(**self.kwargs)
        self.assertNotEqual(out['substeps'], [])
        self.assertEqual(out['run_condition_skipped'], False)

    def test_condition_no_operator(self):

        steps = Steps()
        data = yaml.safe_load(self.condition_6)
        self.kwargs.update({'steps': steps, 'action_item': data})
        self.blitz_obj.parameters['save_variable_name'] = {}
        out = run_condition(**self.kwargs)
        self.assertEqual(out['substeps'], [])
        self.assertEqual(out['run_condition_skipped'], True)

    def test_condition_eq_none(self):

        steps = Steps()
        data = yaml.safe_load(self.condition_7)
        self.kwargs.update({'steps': steps, 'action_item': data})
        self.blitz_obj.parameters['save_variable_name'] = {}
        out = run_condition(**self.kwargs)
        self.assertNotEqual(out['substeps'], [])
        self.assertEqual(out['run_condition_skipped'], False)


if __name__ == '__main__':
    unittest.main()
