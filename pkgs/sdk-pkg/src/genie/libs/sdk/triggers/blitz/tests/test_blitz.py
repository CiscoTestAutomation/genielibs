#! /usr/bin/env python
import os
import yaml
import tempfile
import unittest

from unittest import mock

from genie.testbed import load
from genie.conf.base import Device
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.sdk.triggers.blitz.actions import actions

from pyats.easypy import Task
from pyats.easypy.job import Job
from pyats.easypy import runtime
from pyats.aetest.steps import Steps
from pyats.datastructures import AttrDict
from pyats.aetest.parameters import ParameterMap
from pyats.aetest.signals import AEtestFailedSignal
from pyats.easypy.common_funcs import init_runtime
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked
from genie.libs.sdk.triggers.blitz.markup import get_variable




class MockDevice(object):
    def __init__(self, testbed, name, os):
        self.testbed = testbed
        self.name = name
        self.os = os


class TestBlitz(unittest.TestCase):

    actions_dict = {'execute': 'sample output',
                    'parse': {'a':'b'},
                    'learn': {'a':'b'},
                    'api': 1500}
    yaml1 = '''
        test:
          groups: ['test']
          description: Modifying the testcase description
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
              - section:
                  - description: "section description"
                  - execute:
                      save:
                        - filter: (?P<host>host).*
                          regex: True
                      device: PE1
                      command: show version
    '''
    yaml2 = '''
        test:
          groups: ['test']
          description: Modifying the testcase description
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
              - section:
                  - description: "section description"
                  - parse:
                      device: PE1
                      alias: parse1
                      description: Mocked action description
                      save:
                        - variable_name: name1
                          filter: contains('hardware')
                      command: show version
    '''
    yaml3 = '''
        test:
          groups: ['test']
          description: Modifying the testcase description
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
              - section1:
                  - continue: False
                  - execute:
                      device: PE1
                      command: show version
                      include:
                        - [0-9]
                  - execute:
                      device: PE1
                      command: show vrf
              - section2:
                  - description: "section description"
                  - execute:

                      device: PE1
                      command: show version
    '''
    yaml4 = '''
        test:
          groups: ['test']
          description: Modifying the testcase description
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
              - section1:
                  - execute:
                      continue: False
                      device: PE1
                      command: show version
                      include:
                        - [0-9]
                  - execute:
                      device: PE1
                      command: show vrf
    '''

    yaml5 = '''
        test:
          groups: ['test']
          description: Modifying the testcase description
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
              - section:
                  - execute:
                      save:
                        - variable_name: execute_output
                          regex_findall: ([a-z]+)
                      device: PE1
                      command: show version
    '''

    yaml6 = '''
            test:
              groups: ['test']
              description: Modifying the testcase description
              source:
                  pkg: genie.libs.sdk
                  class: triggers.blitz.blitz.Blitz
              devices: ['PE1']
              test_sections:
                  - section:
                      - description: "section description"
                      - execute:
                          device: PE1
                          command: show version
                          save:
                              - variable_name: execute_action_output
                                as_dict:
                                  rt_2_if2:
                                    rt_22: "%VARIABLES{action_output}"         
        '''



    bad_yaml1 = '''
        test:
          groups: ['test']
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
              - section:
                  - bad_action:
                      device: PE1
                      command: show version
    '''
    bad_yaml2 = '''
        test:
          groups: ['test']
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:

              - section1:
                  - invalid_action

    '''

    bad_yaml3 = '''
        test:
          groups: ['test']
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
                  - section2:
                    - empty_kwargs:
                  '''
    bad_yaml4 = '''
        test:
          groups: ['test']
          source:
              pkg: genie.libs.sdk
              class: triggers.blitz.blitz.Blitz
          devices: ['PE1']
          test_sections:
                  - section3:
                    - parse:
                        device: PE3
                        command: show version
    '''

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

        self._initiate_blitz_cls(self.yaml1)

    def test_init(self):

        self.assertEqual(self.blitz_cls().uid, 'test.PE1')
        self.assertEqual(self.blitz_cls().description, 'Modifying the testcase description')


    def test_dispatcher_1(self):

        blitz_discoverer = self.blitz_cls()._discover()
        for section in blitz_discoverer:

            new_section = section.__testcls__(section)
            steps = Steps()
            blitz_obj = self.blitz_cls()
            self.uid = blitz_obj.uid
            blitz_obj.parent = self
            blitz_obj.parent.parameters = mock.Mock()

            output = blitz_obj.dispatcher(steps,
                                                 self.testbed,
                                                 new_section,
                                                 section.parameters['data'])

            self.assertEqual(output, { 'action': 'execute',
                                                 'alias': None,
                                                 'continue_': True,
                                                 'description': '',
                                                 'device': 'PE1',
                                                 'saved_vars': {'host': 'host'},
                                                 'filters': '(?P<host>host).*',
                                                 'step_result': Passed})

            self.assertEqual(new_section.description, "section description")

    def test_dispatcher_2(self):

        self._initiate_blitz_cls(self.yaml2)
        blitz_discoverer = self.blitz_cls()._discover()

        for section in blitz_discoverer:

            new_section = section.__testcls__(section)
            steps = Steps()
            blitz_obj = self.blitz_cls()
            self.uid = blitz_obj.uid
            blitz_obj.parent = self
            blitz_obj.parent.parameters = mock.Mock()

            output = blitz_obj.dispatcher(steps,
                                          self.testbed,
                                          new_section,
                                          section.parameters['data'])

            desc = section.parameters['data'][1]['parse']['description']
            self.assertEqual(output['description'], desc)
            self.assertIn('parse1', blitz_obj.parameters['save_variable_name'])
            self.assertIsInstance(
                blitz_obj.parameters['save_variable_name']
                ['section.parameters'], AttrDict)
            self.assertIn('name1', output['saved_vars'])

    # TODO might have an issue, in real script it does stop
    # probably because of dummy steps investigate
    def test_dispatcher_section_continue_false(self):
        pass
        # self._initiate_blitz_cls(self.yaml3)
        # blitz_discoverer = self.blitz_cls()._discover()
        # for section in blitz_discoverer:
        #   new_section = section.__testcls__(section)
        #   steps = Steps()
        #   blitz_obj = self.blitz_cls()
        #   new_section.result = Failed
        #   with self.assertRaises(AEtestFailedSignal):
        #       blitz_obj.dispatcher(steps,
        #                            self.testbed,
        #                            new_section,
        #                            section.parameters['data'])

    def test_bad_action(self):
        self._initiate_blitz_cls(self.bad_yaml1)
        blitz_discoverer = self.blitz_cls()._discover()
        for section in blitz_discoverer:
            new_section = section.__testcls__(section)
            steps = Steps()

            with self.assertRaises(Exception):
                self.blitz_cls().dispatcher(steps,
                                            self.testbed,
                                            new_section,
                                            section.parameters['data'])

    def test_invalid_action(self):
        self._initiate_blitz_cls(self.bad_yaml2)
        blitz_discoverer = self.blitz_cls()._discover()
        for section in blitz_discoverer:
            new_section = section.__testcls__(section)
            steps = Steps()

            with self.assertRaises(Exception):
                self.blitz_cls().dispatcher(steps,
                                            self.testbed,
                                            new_section,
                                            section.parameters['data'])

    def test_save_findall(self):
        self._initiate_blitz_cls(self.yaml5)
        blitz_discoverer = self.blitz_cls()._discover()
        for section in blitz_discoverer:

            new_section = section.__testcls__(section)
            steps = Steps()
            blitz_obj = self.blitz_cls()
            self.uid = blitz_obj.uid
            blitz_obj.parent = self
            blitz_obj.parent.parameters = mock.Mock()

            output = blitz_obj.dispatcher(steps,
                                          self.testbed,
                                          new_section,
                                          section.parameters['data'])

            self.assertEqual(output, {
                              'action': 'execute',
                              'device': 'PE1',
                              'alias': None,
                              'continue_': True,
                              'description': '',
                              'saved_vars': {
                                'execute_output': [
                                  'host', 'execute', 'output'
                                ]
                              },
                              'step_result': Passed
                            })

    def test_save_regex_var(self):
        self._initiate_blitz_cls(self.yaml1)
        blitz_discoverer = self.blitz_cls()._discover()
        for section in blitz_discoverer:

            new_section = section.__testcls__(section)
            steps = Steps()
            blitz_obj = self.blitz_cls()
            self.uid = blitz_obj.uid
            blitz_obj.parent = self
            blitz_obj.parent.parameters = mock.Mock()

            output = blitz_obj.dispatcher(steps,
                                          self.testbed,
                                          new_section,
                                          section.parameters['data'])

            self.assertEqual(output['saved_vars'], {'host': 'host'})
            self.assertEqual(output['filters'], '(?P<host>host).*')

    def test_invalid_device(self):
        self._initiate_blitz_cls(self.bad_yaml4)
        blitz_discoverer = self.blitz_cls()._discover()
        for section in blitz_discoverer:
            new_section = section.__testcls__(section)
            steps = Steps()

            with self.assertRaises(Exception):
                self.blitz_cls().dispatcher(steps,
                                            self.testbed,
                                            new_section,
                                            section.parameters['data'])

    def _initiate_blitz_cls(self, yaml_file):

        dir_name = os.path.dirname(os.path.abspath(__file__))
        self.blitz_cls = Blitz
        self.testbed = load(os.path.join(dir_name, 'mock_testbeds/testbed.yaml'))

        self.blitz_cls.parameters = ParameterMap()
        self.blitz_cls.parameters['testbed'] = self.testbed
        self._mock_testbed_devs()
        self.datafile = yaml.safe_load(yaml_file)

        for key, value in self.datafile.items():
            self.blitz_cls.uid = "{}.{}".format(key, value['devices'][0])
            self.blitz_cls.parameters['test_sections'] = value['test_sections']
            if value.get('description'):
                self.blitz_cls.description = value['description']

    def _mock_testbed_devs(self):

        side_effects = {'configure': ['\n'],
                        'execute': ['host execute output', 'oop', 'oot', 'name'],
                        'parse': [{'a': '1', 'hardware': 'hardware_name'}]}

        actions = ['configure', 'execute', 'parse']
        for dev in self.testbed.devices:
            for action in actions:
                setattr(self.testbed.devices[dev], action, mock.Mock())
                setattr(getattr(self.testbed.devices[dev], action), 'side_effect', side_effects[action])

    def test_custom_start_step_messsage_with_variable(self):
        #saved variable
        Blitz.parameters['save_variable_name'] = {'command': 'sh version'}
        self.blitz_obj = Blitz()
        self.blitz_obj.parameters['test_sections'] = [{'section1': [{'action': {'command': 'a'}}]}]
        sections = self.blitz_obj._discover()
        self.section = sections[0].__testcls__(sections[0])

        self.kwargs = {
            'self': self.blitz_obj,
            'section': self.section,
            'custom_start_step_message': 'test command: %VARIABLES{command}'
        }

        #To get the saved variable
        replaced_kwargs = get_variable(**self.kwargs)
        self.assertEqual(replaced_kwargs['custom_start_step_message'], 'test command: sh version')

    def test_save_as_dict(self):
        self._initiate_blitz_cls(self.yaml6)
        blitz_discoverer = self.blitz_cls()._discover()
        for section in blitz_discoverer:
            new_section = section.__testcls__(section)
            steps = Steps()
            blitz_obj = self.blitz_cls()
            self.uid = blitz_obj.uid
            blitz_obj.parent = self
            blitz_obj.parent.parameters = mock.Mock()

            output = blitz_obj.dispatcher(steps,
                                          self.testbed,
                                          new_section,
                                          section.parameters['data'])
            self.assertEqual(output['saved_vars']['execute_action_output'], {'rt_2_if2': {'rt_22': 'host execute output'}})

if __name__ == '__main__':
    unittest.main()
