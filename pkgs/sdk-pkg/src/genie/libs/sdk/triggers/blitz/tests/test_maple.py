#! /usr/bin/env python
import os
import sys
import tempfile
import unittest
import importlib
from unittest.mock import Mock
from unittest.mock import patch

from genie.libs import sdk
from genie.testbed import load
from genie.conf.base import Testbed, Device
from genie.harness.script import TestScript
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.sdk.triggers.blitz.maple import maple, maple_search


from pyats.aetest.steps import Steps
from pyats.aetest.parameters import ParameterMap
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked

def check_maple_env():
  if not os.environ.get('MAPLE_PATH'):
     return True

  if os.environ['MAPLE_PATH'] not in sys.path:
    sys.path.append(os.environ['MAPLE_PATH'])

  return False

@unittest.skipIf(check_maple_env(), "MAPLE_PATH is not set")
class TestMaple(unittest.TestCase):

    plugin_input1 = '{"rule-1": {"type": "cli", "commands": "command:{\\n'\
                    '                    \\"method\\":\\"waitfor\\",\\n  '\
                    '                 \\"options\\":[\\n                 '\
                    '  {\\"command\\":\\"show module\\"},\\n             '\
                    '       {\\"match\\":\\"Up\\"},\\n                   '\
                    '{\\"timeout\\":\\"10\\"}\\n       ]}"}}'
    plugin_input2 =  '{"rule-1": {"type": "matcher", "commands": "matcher:{\\n'\
                     '    \\"package\\":\\"maple.plugins.user.MatcherPlugins\\"'\
                     ',\\n    \\"method\\":\\"populateObjects\\",\\n    '\
                     '\\"command\\":\\"show version\\",\\n    \\"type\\":\\"cli\\"\\n    }"}}'

    plugin_input3 =  '{"rule-1": {"type": "matcher", "commands": "matcher:{\\n'\
                     '    \\"package\\":\\"maple.plugins.user.MatcherPlugins\\"'\
                     ',\\n    \\"method\\":\\"populateObjects\\",\\n    '\
                     '\\"type\\":\\"cli\\"\\n    }"}}'

    plugin_input4 = '{"rule-1": {"type": "cli", "commands": "confirm:{\\n '\
                    '   \\"package\\":\\"maple.plugins.user.ConfirmPlugins\\",\\n'\
                    '    \\"method\\":\\"checkIfPresent\\",\\n    \\"options\\":[\\n'\
                    '        {\\"count\\":\\"1\\"},\\n        {\\"check1\\": \\"192.168.0.4\\"}\\n    ]}"}}'

    plugin_input5 = '{"rule-1": {"type": "cli", "commands": "command:{\\n'\
                    '                    \\"method\\":\\"ixia\\",\\n  '\
                    '                 \\"options\\":[\\n                 '\
                    '  {\\"command\\":\\"connect\\"}]}"}}'

    execute_output = '''
                     Mod Ports             Module-Type                       Model        Status
                    --- ----- -------------------------------------------------------------------
                    1    48   1/10G SFP+ Ethernet Module            N9K-C9396PX           active *
                    2    12   40G Ethernet Expansion Module         N9K-M12PQ             ok
                    Mod  Sw                       Hw    Slot
                    ---  ----------------------- ------ ----
                    1    9.3(3)IDI9(0.509)        2.2    NA
                    2    NA                       1.2    GEM
                    Mod  MAC-Address(es)                      Serial-Num
                    ---  --------------------------------------  ----------
                    1    84-b8-02-f0-83-90 to 84-b8-02-f0-83-c7  SAL1914CNL6
                    2    88-1d-fc-71-de-38 to 88-1d-fc-71-de-43  SAL1928K4EG
                    Mod  Online Diag Status
                    ---  ------------------
                    1    Pass
    '''

    execute_output_1 = """
          Legend:
          (P)=Protected, (F)=FRR active, (*)=more labels in stack.

          IPV4:
          In-Label   Out-Label  FEC name           Out-Interface      Next-Hop
          16005      16005      5.5.5.0/32         Eth1/10            2.3.1.3
          16005      16005      5.5.5.0/32         Eth1/12            2.4.1.4

          Legend:
          (P)=Protected, (F)=FRR active, (*)=more labels in stack.

          IPV4:
          In-Label   Out-Label  FEC name           Out-Interface      Next-Hop
          VRF default
          16002      16002      2.2.2.0/32         Eth1/15            3.5.1.3
          16002      16002      2.2.2.0/32         Eth1/10            4.5.1.4

          Legend:
          (P)=Protected, (F)=FRR active, (*)=more labels in stack.

          IPV4:
          In-Label   Out-Label  FEC name           Out-Interface      Next-Hop
          VRF default
          16002      16002      2.2.2.0/32         Eth1/49            3.6.1.3
          16002      16002      2.2.2.0/32         Eth1/51            4.6.1.4

          Legend:
          (P)=Protected, (F)=FRR active, (*)=more labels in stack.

          IPV4:
          In-Label   Out-Label  FEC name           Out-Interface      Next-Hop
          16006      Pop Label  6.6.6.0/32         Eth1/56            6.8.1.6

          Legend:
          (P)=Protected, (F)=FRR active, (*)=more labels in stack.

          IPV4:
          In-Label   Out-Label  FEC name           Out-Interface      Next-Hop
          16006      Pop Label  6.6.6.0/32         Eth1/8             6.7.1.6
    """

    def setUp(self):

        dir_name = os.path.dirname(os.path.abspath(__file__))
        self.testbed = load(os.path.join(dir_name, 'mock_testbeds/testbed.yaml'))
        Blitz.parameters = ParameterMap()
        Blitz.uid = 'test.dev'
        Blitz.parameters['testbed'] = self.testbed

        self.blitz_obj = Blitz()
        self.uid = self.blitz_obj.uid
        self.blitz_obj.parent = self
        self.blitz_obj.parent.parameters = Mock()

        self.dev = Device( name='PE1', os='iosxe')
        self.dev.custom = {'abstraction': {'order': ['os']}}
        self.blitz_obj.parameters['test_sections'] = [{'section1': [{'action': {'command': 'a'}}]}]
        sections = self.blitz_obj._discover()
        self.kwargs = {'self': self.blitz_obj,
                       'section': sections[0],
                       'name': ''}

    def test_default_package_pass(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'maple_plugin_input': self.plugin_input1,
                          'maple_action': 'confirm'})

      with patch('plugins.system.Commands.waitfor',
                 return_value= {'result': [True],'matchObjs':{'a':'b', 'c':12}}) as func:

        maple(**self.kwargs)
        func.assert_called_once()
        self.assertIn('a', self.blitz_obj.parameters['save_variable_name'])
        self.assertEqual(steps.result, Passed)

    def test_default_package_fail(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'maple_plugin_input': self.plugin_input1,
                          'maple_action': 'confirm'})

      with patch('plugins.system.Commands.waitfor',
                 return_value= {'result': [False],'matchObjs':{'a':'b', 'c':12}}) as func:

        maple(**self.kwargs)
        func.assert_called_once()
        self.assertIn('a', self.blitz_obj.parameters['save_variable_name'])
        self.assertEqual(steps.result, Failed)

    def test_matcher_package_with_output(self):

      steps = Steps()
      self.dev.execute = Mock(return_value='a string out')
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'maple_plugin_input': self.plugin_input2})

      with patch('plugins.user.MatcherPlugins.populateObjects',
                 return_value= {'matchObjs':{'a':'b', 'c':12}}) as func:

        maple(**self.kwargs)
        func.assert_called_once()
        self.assertIn('c', self.blitz_obj.parameters['save_variable_name'])
        self.assertEqual(steps.result, Passed)


    def test_matcher_package_without_output(self):

      steps = Steps()
      self.dev.execute = Mock(side_effect=Exception)
      with steps.start("Starting action", continue_=True) as step:

        self.kwargs.update({'steps': step,
                            'device': self.dev,
                            'maple_plugin_input': self.plugin_input2})
        maple(**self.kwargs)
        self.assertEqual(step.result, Failed)

    def test_matcher_package_bad_command(self):

      steps = Steps()
      with steps.start("Starting action", continue_=True) as step:

        self.kwargs.update({'steps': step,
                            'device': self.dev,
                            'maple_plugin_input': self.plugin_input3})
        maple(**self.kwargs)
        self.assertEqual(step.result, Failed)

    def test_confirm_package(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'maple_plugin_input': self.plugin_input4,
                          'output': self.execute_output})

      with patch('plugins.user.ConfirmPlugins.checkIfPresent',
                 return_value= {'result': True, 'matchObjs':{'a':'b', 'c':12}}) as func:

        maple(**self.kwargs)
        func.assert_called_once()
        self.assertEqual(steps.result, Passed)

    def test_default_package_ixia(self):

      steps = Steps()
      self.dev.type = 'ixia'
      self.kwargs.update({'steps': steps,
                          'device': self.dev,
                          'maple_plugin_input': self.plugin_input5,
                          'maple_action': 'confirm'})

      with patch('plugins.system.Commands.ixia',
                 return_value= {'result': [True],'ixiaObjs':{'a':'b', 'c':12}}) as func:

        maple(**self.kwargs)
        func.assert_called_once()
        self.assertIn('a', self.blitz_obj.parameters['save_variable_name'])
        self.assertEqual(steps.result, Passed)

    def test_maple_search_include_pass(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'search_string': self.execute_output_1,
                          'device': self.dev,
                          'include': ['^(?=.*\b16006\b)(?=.*\bPop Label\b).*$']})

      maple_search(**self.kwargs)
      self.assertEqual(steps.result, Passed)

    def test_maple_search_include_fail(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'search_string': self.execute_output_1,
                          'device': self.dev,
                          'include': ['\s*\bSel-Num\b.*']})

      maple_search(**self.kwargs)
      self.assertEqual(steps.result, Failed)


    def test_maple_search_exclude_fail(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'search_string': self.execute_output_1,
                          'device': self.dev,
                          'exclude': ['^(?=.*\b16006\b)(?=.*\bPop Label\b).*$']})

      maple_search(**self.kwargs)
      self.assertEqual(steps.result, Failed)

    def test_maple_search_exclude_pass(self):

      steps = Steps()
      self.kwargs.update({'steps': steps,
                          'search_string': self.execute_output_1,
                          'device': self.dev,
                          'exclude': ['\s*\bSel-Num\b.*']})

      maple_search(**self.kwargs)
      self.assertEqual(steps.result, Passed)

if __name__ == '__main__':
    unittest.main()
