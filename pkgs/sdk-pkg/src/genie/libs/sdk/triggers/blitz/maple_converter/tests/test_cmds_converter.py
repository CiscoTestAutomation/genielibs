#! /usr/bin/env python
import os
import sys
import unittest
import ruamel.yaml
from unittest.mock import Mock
from unittest.mock import patch
from genie.libs.sdk.triggers.blitz.maple_converter.cmds_converter import CmdsConverter


def check_maple_env():
   if not os.environ.get('MAPLE_PATH'):
      return True
   
   return False

class TestCmdsConverter(unittest.TestCase):

   dialog_cmd = 'cmds=dialog:::show tech-support routing ip unicast >'\
                ' urib_v4.ts~{"dialog-list":[["Do you want to overwrite","y"]]}~0~120'

   killprocess_cmd_1 = 'cmds=killprocess:bootflash,debug-img,l3vm'
   killprocess_cmd_2 = 'cmds=killprocess:ulib'

   copy_cmd = 'cmds=copy:123.100.101.79,scp,management,root'\
              ',roZes,bootflash,/ws/skasimut-ott/images/n7700'\
              '-s2-dk9.8.0.1.bin,n7700-s2-dk9.8.0.1.bin,true'

   issu_cmd_1 = 'cmds=issu:bootflash,n7000-s2-kickstart.8.2.0.SK.0.83.'\
                'upg.gbin,n7000-s2-dk9.8.2.0.SK.0.83.upg.gbin,900'

   issu_cmd_2 = 'cmds=issu:bootflash,nxos.7.0.3.IHD8.0.430.bin,900'
   waitfor_cmd = 'cmds=waitfor:::show vlan,,Up,,9'
   runonmodule_cmd = 'cmds=runonmodule:::5,show module,9'
   switch_to_cmd = 'cmds=switchto:vdc'
   sleep_cmd = 'cmds=sleep:10'

   reload_cmd_1 = 'cmds=reload_module:1'
   reload_cmd_2 = 'cmds=reload_vdc:VDC1'
   reload_cmd_3 = 'cmds=reload:360'
   reload_cmd_4 = 'cmds=reload:10, True, 100, True'

   patterns_cmd = '''
            cmds=patterns:::
         [show version,,BIOS:\s+version\s+XX(bios)XX([0-9A-Za-z()./]+).*]
         [show version,,bootflash:\s+XX(bootflash)XX([0-9A-Za-z()./]+)\s+XX(measure)XX(\w+).*]
         [show vrf,,default\s+XX(default)XX([0-9/]+)\s+XX(up_down)XX(Up|Down).*]
         '''

   eval_cmd = "cmds=eval:::'XX(adminSt)XX' == 'enabled'"

   groups_cmd_pattern = '''
               cmds=groups:::
            [ping6 77:77:77::2 vrf vrf_2_7_8 count 5,,\d+ packets transmitted, \d+ packets received, ([0-9.]+)% packet loss]
                        '''

   groups_cmd_matcher = 'cmds=groups:::1.1 > 1000'

   ixia_startprotocols_cmd = 'cmds=startprotocols:'
   ixia_trafficstats_cmd = 'cmds=trafficstats:10'
   ixia_load_config_cmd = 'cmds=loadconfig:/ws/vinavisw-ott/nx/maple/'\
                           'MPLS/SRTE-I/SRTE-Traffic/SRTE9.ixncfg'


   def test_cmds_dialog_translate(self):
      
      cmds = CmdsConverter(self.dialog_cmd, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()

      expected ={'plugin': ' command:{\n'
           '                    "method":"dialog",\n'
           '                    "options":[\n'
           '                    {"cmd":"show tech-support routing ip unicast > '
           'urib_v4.ts"},\n'
           '                    {"dialog-list":{"dialog-list":[["Do you want '
           'to overwrite","y"]]}},\n'
           '                    {"sleep":"0"},\n'
           '                    {"timeout":"120"}\n'
           '       ]}\n'
           '                '}
      
      self.assertEqual(out, expected)

   def test_cmds_killprocess_translate_1(self):
      
      cmds = CmdsConverter(self.killprocess_cmd_1, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()

      expected = {'plugin': ' command:{\n'
           '                    "method":"killprocess",\n'
           '                    "options":[\n'
           '                    {"media":"bootflash"},\n'
           '                    {"debug_plugin":"debug-img"},\n'
           '                    {"process_name":"l3vm"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_cmds_killprocess_translate_2(self):

      cmds = CmdsConverter(self.killprocess_cmd_2, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()

      expected = {'plugin': ' command:{\n'
           '                    "method":"killprocess",\n'
           '                    "options":[\n'
           '                    {"process_name":"ulib"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_cmds_copy_translate(self):
      
      cmds = CmdsConverter(self.copy_cmd, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"copy",\n'
           '                    "options":[\n'
           '                    {"server":"123.100.101.79"},\n'
           '                    {"source":"scp"},\n'
           '                    {"vrf":"management"},\n'
           '                    {"username":"root"},\n'
           '                    {"password":"roZes"},\n'
           '                    {"media":"bootflash"},\n'
           '                    '
           '{"source_file":"/ws/skasimut-ott/images/n7700-s2-dk9.8.0.1.bin"},\n'
           '                    {"dest_file":"n7700-s2-dk9.8.0.1.bin"},\n'
           '                    {"compact_copy":"true"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_issu_translate_1(self):

      cmds = CmdsConverter(self.issu_cmd_1, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"issu",\n'
           '                    "options":[\n'
           '                    {"media":"bootflash"},\n'
           '                    '
           '{"kickstart":"n7000-s2-kickstart.8.2.0.SK.0.83.upg.gbin"},\n'
           '                    '
           '{"system":"n7000-s2-dk9.8.2.0.SK.0.83.upg.gbin"},\n'
           '                    {"sleep":"900"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_issu_translate_2(self):

      cmds = CmdsConverter(self.issu_cmd_2, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"issu",\n'
           '                    "options":[\n'
           '                    {"media":"bootflash"},\n'
           '                    {"nxos":"nxos.7.0.3.IHD8.0.430.bin"},\n'
           '                    {"sleep":"900"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_waitfor_translate(self):

      cmds = CmdsConverter(self.waitfor_cmd, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"waitfor",\n'
           '                    "options":[\n'
           '                    {"command":"show vlan"},\n'
           '                    {"match":"Up"},\n'
           '                    {"timeout":"9"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_runonmodule_translate(self):

      cmds = CmdsConverter(self.runonmodule_cmd, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"runonmodule",\n'
           '                    "options":[\n'
           '                    {"module":"5"},\n'
           '                    {"command":"show module"},\n'
           '                    {"timeout":"9"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_switchto_translate(self):

      cmds = CmdsConverter(self.switch_to_cmd, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"switchto",\n'
           '                    "options":[\n'
           '                    {"value":"vdc"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_sleep_translate(self):

      cmds = CmdsConverter(self.sleep_cmd, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"sleep",\n'
           '                    "options":[\n'
           '                    {"duration":"10"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_reload_module_translate(self):

      cmds = CmdsConverter(self.reload_cmd_1, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"reload_module",\n'
           '                    "options":[\n'
           '                    {"command":"reload_module"},\n'
           '                    {"value":"1"}\n'
           '                    ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_reload_vdc_translate(self):

      cmds = CmdsConverter(self.reload_cmd_2, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"reload_vdc",\n'
           '                    "options":[\n'
           '                    {"command":"reload_vdc"},\n'
           '                    {"value":"VDC1"}\n'
           '                    ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_reload_translate_1(self):

      cmds = CmdsConverter(self.reload_cmd_3, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"reload",\n'
           '                    "options":[\n'
           '                    {"command":"reload"},\n'
           '                    {"sleep":"360"}\n'
           '                    ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_reload_translate_2(self):

      cmds = CmdsConverter(self.reload_cmd_4, 'cli')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"reload",\n'
           '                    "options":[\n'
           '                    {"command":"reload"},\n'
           '                    {"sleep":"10"},\n'
           '                    {"no_copy_rs":" True"},\n'
           '                    {"timeout":" 100"},\n'
           '                    {"is_ascii":" True"}\n'
           '                    ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_ixia_startprotocols(self):

      cmds = CmdsConverter(self.ixia_startprotocols_cmd, 'tgen-config')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"ixia",\n'
           '                    "options":[\n'
           '                    {"command":"startprotocols"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_ixia_trafficstats(self):

      cmds = CmdsConverter(self.ixia_trafficstats_cmd, 'tgen-config')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"ixia",\n'
           '                    "options":[\n'
           '                    {"command":"gettrafficstats"},\n'
           '                    {"sleep":"10"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)

   def test_ixia_loadconfig(self):

      cmds = CmdsConverter(self.ixia_trafficstats_cmd, 'tgen-config')
      out = cmds.cmds_to_maple_plugin_converter()
      expected = {'plugin': ' command:{\n'
           '                    "method":"ixia",\n'
           '                    "options":[\n'
           '                    {"command":"gettrafficstats"},\n'
           '                    {"sleep":"10"}\n'
           '       ]}\n'
           '                '}

      self.assertEqual(out, expected)
   
   def test_cmds_patterns(self):

      cmds = CmdsConverter(self.patterns_cmd, 'matcher')
      cmd_pattern = cmds.cmds_to_maple_plugin_converter()
      out = cmds.cmds_patterns_to_blitz_action_converter(cmd_pattern['data'], 'N93_3')

      expected = {'specifically_patterns': [{'execute': {'command': 'show version',
                                                         'device': 'N93_3',
                                                         'save': [{'filter': 'BIOS:\\s+version\\s+(?P<bios>[0-9A-Za-z()./]+).*',
                                                                   'regex': True},
                                                                  {'filter': 'bootflash:\\s+(?P<bootflash>[0-9A-Za-z()./]+)\\s+(?P<measure>\\w+).*',
                                                                   'regex': True}]}},
                                             {'execute': {'command': 'show vrf',
                                                          'device': 'N93_3',
                                                          'save': [{'filter': 'default\\s+(?P<default>[0-9/]+)\\s+(?P<up_down>Up|Down).*',
                                                                    'regex': True}]}}]}

      self.assertEqual(out, expected)

   def test_cmds_eval(self):

      cmds = CmdsConverter(self.eval_cmd, 'cli')
      cmd_pattern = cmds.cmds_to_maple_plugin_converter()
      out = cmds.cmds_eval_to_blitz_action_converter(cmd_pattern['data'])
      expected = {'compare': {'items': ["'%VARIABLES{adminSt}' == 'enabled'"]}}
      self.assertEqual(out, expected)

   def test_groups_pattern(self):

      cmds = CmdsConverter(self.groups_cmd_pattern, 'matcher')
      cmd_pattern = cmds.cmds_to_maple_plugin_converter()
      out = cmds.cmds_groups_command_to_blitz_action_converter(cmd_pattern['data'], 'N93_3')

      expected = {'specifically_patterns': [{'execute': {'command': '            [ping6 '
                                                   '77:77:77::2 vrf vrf_2_7_8 '
                                                   'count 5',
                                             'device': 'N93_3',
                                             'save': [{'filter': '\\d+ packets '
                                                                 'transmitted, \\d+ '
                                                                 'packets received, '
                                                                 '(?P<name1_1>[0-9.]+)% '
                                                                 'packet loss',
                                                       'regex': True}]}}]}

      self.assertEqual(out, expected)

   def test_groups_matcher(self):

      cmds = CmdsConverter(self.groups_cmd_matcher, 'matcher')
      cmd_pattern = cmds.cmds_to_maple_plugin_converter()
      out = cmds.cmds_groups_match_to_blitz_action(cmd_pattern['data'])
      expected = {'compare': {'items': ['%VARIABLES{name1_1} > 1000']}}

      self.assertEqual(out, expected)




if __name__ == '__main__':
    unittest.main()