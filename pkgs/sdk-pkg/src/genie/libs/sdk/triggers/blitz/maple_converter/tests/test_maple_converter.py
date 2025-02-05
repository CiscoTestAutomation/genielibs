#! /usr/bin/env python
import os
import unittest
import ruamel.yaml
from unittest.mock import Mock
from unittest.mock import patch

from genie.libs.sdk.triggers.blitz.maple_converter.utils import pre_testcase_checks, \
                                                                pre_section_checks
from genie.libs.sdk.triggers.blitz.maple_converter.maple_converter import Converter
from genie.libs.sdk.triggers.blitz.maple_converter.legacy_dme_converter import LegacyDmeConverter

def check_maple_env():
   if not os.environ.get('MAPLE_PATH'):
      return True
   
   return False

class TestMapleConverter(unittest.TestCase):

    def setUp(self):

        dir_name = os.path.abspath(
                                   os.path.join(os.path.dirname( __file__ ), '../..', 'tests'))
        self.script = os.path.join(dir_name, 'mock_yamls/maple_yaml.yaml')
        self.testbed = os.path.join(dir_name, 'mock_testbeds/testbed.yaml')
        self.converter = Converter(self.script, testbed=self.testbed)

    @unittest.skipIf(check_maple_env(), "MAPLE_PATH is not set")
    def test_init(self):

      trigger_uids = self.converter.convert()

      expected = ['confirm_and_search',
                  'plugin_call',
                  'helloworld_dme_test',
                  'helloworld_loop_simple',
                  'helloworld_single_iterable_loop',
                  'bfd_test_static',
                  'bfd_test_static_no_step',
                  'log_collection_test']

      self.assertEqual(trigger_uids, expected)

    def test_log_collection(self):

        maple = """ 
        log:
            sections: apply
            states: passed, failed
            devices: PE1,PE2
            server: scp,scp,/ws/mziabari-ott/development,management
            # media: bootflash
            commands: |
                show version
                show interface
        """

        maple_dict = ruamel.yaml.safe_load(maple)
        out = pre_testcase_checks(maple_dict, None, None, None)

        blitz_equal = {
                "processors":{
                 "post":{
                    "post_execute_command":{
                       "method":"genie.libs.sdk.libs.abstracted_libs.post_execute_command",
                       "parameters":{
                          "zipped_folder":False,
                          "save_to_file":"per_command",
                          "valid_section_results":[
                             "passed",
                             " failed"
                          ],
                          "server_to_store":{
                             "server_in_testbed":"scp",
                             "protocol":"scp",
                             "remote_path":"/ws/mziabari-ott/development"
                          },
                          "devices":{
                             "PE1":{
                                "cmds":[
                                   {
                                      "cmd":"show version"
                                   },
                                   {
                                      "cmd":"show interface"
                                   }
                                ]
                             },
                             "PE2":{
                                "cmds":[
                                   {
                                      "cmd":"show version"
                                   },
                                   {
                                      "cmd":"show interface"
                                   }
                                ]
                             }
                          }
                       }
                    }
                 }
              },
            }
        self.assertEqual(out['blitz_pre_tc_data'], blitz_equal)

    def test_flow_control(self):

        maple = """ 
                    {
                        "action": "skip",
                        "condition": "'XX(front_port)XX' == 'version'"
                    }             
        """

        out = pre_section_checks('flowcontrol', maple, [], None)

        blitz_equal = [{
                  "section_control":{
                     "if":"'%VARIABLES{front_port}' == 'version'",
                     "function":"skipped"
                  }
               }]
        self.assertEqual(out[0], blitz_equal)
    
    def test_loop(self):
        pass

    def test_apply_unapply_show_command(self):

        maple = """ 
        devices:
            device{testbed.custom.devices.deviceA}:
                type: cli
                commands: |
                    conf t
                    feature bfd
        """
        maple_dict = ruamel.yaml.safe_load(maple)
        kwargs = {'apply_unapply_data': maple_dict,
                  'blitz_action_list': [],
                  'action_continue': None,
                  'maple_action': 'apply',
                  'section': 'step_1',
                  'maple_testcase_name': 'test'}

        out = self.converter.apply_unapply_converter(**kwargs)
        blitz_equal = [{
                "configure":{
                   "device":"device{testbed.custom.devices.deviceA}",
                   "command":"conf t\nfeature bfd\n",
                   "save":[
                      {
                         "variable_name":"test_step_1_apply",
                         "append":True
                      }
                   ],
                   "maple":True,
                   "continue":False
                }
            }]
        self.assertEqual(out[0], blitz_equal)

    def test_apply_unapply_plugin(self):

        maple = """ 
        devices:
            N93_3:
                type: dmerest
                commands: |
                    #@# command:{
                        "method":"processdme",
                        "options":[
                            {"method":"POST"},
                            {"url":"http://acjain-laas:8001/api/node/mo/sys/ldp.json"},
                            {"payload":"dme_post.json"},
                            {"ignore_error":"True"}
                        ]} 
                    #@# 
        """
        maple_dict = ruamel.yaml.safe_load(maple)
        kwargs = {'apply_unapply_data': maple_dict,
                  'blitz_action_list': [],
                  'action_continue': None,
                  'maple_action': 'apply',
                  'section': 'step_1',
                  'maple_testcase_name': 'test'}

        out = self.converter.apply_unapply_converter(**kwargs)
        blitz_equal = [
               {
                  "maple":{
                     "maple_plugin_input":"{\"type\": \"dmerest\", \"commands\": \"command:{\\n    \\\"method\\\":\\\"processdme\\\",\\n    \\\"options\\\":[\\n        {\\\"method\\\":\\\"POST\\\"},\\n        {\\\"url\\\":\\\"http://acjain-laas:8001/api/node/mo/sys/ldp.json\\\"},\\n        {\\\"payload\\\":\\\"dme_post.json\\\"},\\n        {\\\"ignore_error\\\":\\\"True\\\"}\\n    ]}\"}",
                     "device":"N93_3",
                     "maple_action":"apply",
                     "continue":False
                  }
               }
            ]
        self.assertEqual(out[0], blitz_equal)

    def test_apply_unapply_cmds(self):

        maple = """ 
        devices:
            device{testbed.custom.devices.deviceA}:
                type: cli
                commands: |
                    #@# cmds=sleep:22 #@#   
        """
        maple_dict = ruamel.yaml.safe_load(maple)
        kwargs = {'apply_unapply_data': maple_dict,
                  'blitz_action_list': [],
                  'action_continue': None,
                  'maple_action': 'apply',
                  'section': 'step_1',
                  'maple_testcase_name': 'test'}

        out = self.converter.apply_unapply_converter(**kwargs)
        blitz_equal = [
           {
              "maple":{
                 "maple_plugin_input":"{\"type\": \"cli\", \"commands\": \"command:{\\n                    \\\"method\\\":\\\"sleep\\\",\\n                    \\\"options\\\":[\\n                    {\\\"duration\\\":\\\"22\\\"}\\n       ]}\"}",
                 "device":"device{testbed.custom.devices.deviceA}",
                 "maple_action":"apply",
                 "continue":False
              }
           }
        ]
        self.assertEqual(out[0], blitz_equal)

    def test_apply_unapply_mixed_commands(self):

        maple = """ 
        devices:
            device{testbed.custom.devices.deviceA}:
                type: cli
                commands: |
                    conf t
                    feature bfd
                    #@# cmds=waitfor:::show vlan,,Up,,9 #@#
                    #@# cmds=switchback: #@#
                    #@# cmds=switchto:N93_3 #@#  
                    #@# cmds=novpc:22 #@#    
        """
        maple_dict = ruamel.yaml.safe_load(maple)
        kwargs = {'apply_unapply_data': maple_dict,
                  'blitz_action_list': [],
                  'action_continue': None,
                  'maple_action': 'apply',
                  'section': 'step_1',
                  'maple_testcase_name': 'test'}

        out = self.converter.apply_unapply_converter(**kwargs)

        blitz_equal = [
               {
                  "configure":{
                     "device":"device{testbed.custom.devices.deviceA}",
                     "command":"conf t\nfeature bfd\n",
                     "save":[
                        {
                           "variable_name":"test_step_1_apply",
                           "append":True
                        }
                     ],
                     "maple":True,
                     "continue":False
                  }
               },
               {
                  "maple":{
                     "maple_plugin_input":"{\"type\": \"cli\", \"commands\": \"command:{\\n                    \\\"method\\\":\\\"waitfor\\\",\\n                    \\\"options\\\":[\\n                    {\\\"command\\\":\\\"show vlan\\\"},\\n                    {\\\"match\\\":\\\"Up\\\"},\\n                    {\\\"timeout\\\":\\\"9\\\"}\\n       ]}\"}",
                     "device":"device{testbed.custom.devices.deviceA}",
                     "maple_action":"apply",
                     "continue":False
                  }
               },
               {
                  "maple":{
                     "maple_plugin_input":"{\"type\": \"cli\", \"commands\": \"command:{\\n                    \\\"method\\\":\\\"switchback\\\"\\n       }\"}",
                     "device":"device{testbed.custom.devices.deviceA}",
                     "maple_action":"apply",
                     "continue":False
                  }
               },
               {
                  "maple":{
                     "maple_plugin_input":"{\"type\": \"cli\", \"commands\": \"command:{\\n                    \\\"method\\\":\\\"switchto\\\",\\n                    \\\"options\\\":[\\n                    {\\\"value\\\":\\\"N93_3\\\"}\\n       ]}\"}",
                     "device":"device{testbed.custom.devices.deviceA}",
                     "maple_action":"apply",
                     "continue":False
                  }
               },
               {
                  "maple":{
                     "maple_plugin_input":"{\"type\": \"cli\", \"commands\": \"command:{\\n                    \\\"method\\\":\\\"novpc\\\",\\n                    \\\"options\\\":[\\n                    {\\\"duration\\\":\\\"22\\\"}\\n       ]}\"}",
                     "device":"device{testbed.custom.devices.deviceA}",
                     "maple_action":"apply",
                     "continue":False
                  }
               }
            ]
        self.assertEqual(out[0], blitz_equal)

    def test_confirm_show_command(self):

        maple = """ 
        devices:
               N93_3:
                   rule-1:
                       type: cli
                       commands: |
                           show vdc
        """
        maple_dict = ruamel.yaml.safe_load(maple)
        kwargs = {'confirm_data': maple_dict,
                  'blitz_action_list': [],
                  'action_continue': None,
                  'section': 'step_1'}

        out = self.converter.confirm_converter(**kwargs)
        blitz_equal = [{'execute': {'command': 'show vdc', 'continue': False, 'device': 'N93_3'}}]
        self.assertEqual(out, blitz_equal)

    def test_confirm_show_command_match_unmatch(self):

        maple = """ 
        devices:
               N93_3:
                   rule-1:
                       type: cli
                       commands: |
                           show vdc
                           show version
                       match: |
                           \\d
                           \\w
        """
        maple_dict = ruamel.yaml.safe_load(maple)
        kwargs = {'confirm_data': maple_dict,
                  'blitz_action_list': [],
                  'action_continue': None,
                  'section': 'step_1'}

        out = self.converter.confirm_converter(**kwargs)
        blitz_equal = [
           {
              "execute":{
                 "device":"N93_3",
                 "command":"show vdc",
                 "save":[
                    {
                       "variable_name":"step_1_rule-1_match_unmatch",
                       "append":True
                    }
                 ],
                 "continue":False
              }
           },
           {
              "execute":{
                 "device":"N93_3",
                 "command":"show version",
                 "save":[
                    {
                       "variable_name":"step_1_rule-1_match_unmatch",
                       "append":True
                    }
                 ],
                 "continue":False
              },
              "maple_search":{
                 "search_string":"%VARIABLES{step_1_rule-1_match_unmatch}",
                 "device":"N93_3",
                 "include":[
                    "\\d",
                    "\\w"
                 ]
              }
           }
        ]
        self.assertEqual(out, blitz_equal)

    def test_confirm_plugin(self):

        maple = """ 
        devices:
            N93_3:
                rule-1:
                    type: dmerest
                    commands: |
                        #@# command:{
                            "method":"processdme",
                            "options":[
                                {"method":"GET"},
                                {"url":"http://acjain-laas:8001/api/node/mo/sys/ldp.json"}
                            ]} 
                        #@#
        """
        maple_dict = ruamel.yaml.safe_load(maple)
        kwargs = {'confirm_data': maple_dict,
                  'blitz_action_list': [],
                  'action_continue': None,
                  'section': 'step_1'}
        blitz_equal = [
               {
                  "maple":{
                     "maple_plugin_input":"{\"rule-1\": {\"type\": \"dmerest\", \"commands\": \"command:{\\n    \\\"method\\\":\\\"processdme\\\",\\n    \\\"options\\\":[\\n        {\\\"method\\\":\\\"GET\\\"},\\n        {\\\"url\\\":\\\"http://acjain-laas:8001/api/node/mo/sys/ldp.json\\\"}\\n    ]}\"}}",
                     "device":"N93_3",
                     "maple_action":"confirm",
                     "continue":False
                  }
               }
            ]

        out = self.converter.confirm_converter(**kwargs)
        self.assertEqual(out, blitz_equal)

   # TODO enhance maple plugins for dme so it takes string json as value
   # And not only json files, Right now it only takes files which makes
   # us to create an extra file dynamically to contains json data
    def test_legacy_dme(self):
        pass 

if __name__ == '__main__':
    unittest.main()