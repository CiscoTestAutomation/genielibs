import os
import re
import sys
import yaml
import json
import random
import string
import logging
import requests
import xmltodict
import ruamel.yaml

from ats.easypy import runtime
from pyats.topology.loader.markup import TestbedMarkupProcessor

from genie.utils import Dq
from genie.testbed import load

from .utils import (replace_maple_markups,
                    pre_testcase_checks,
                    pre_section_checks,
                    _XX_pattern_matching,
                    verify_maple_env,
                    _command_separator,
                    plugin_to_blitz_action_converter,
                    show_command_to_blitz_action_converter)

from .cmds_converter import CmdsConverter
from .legacy_dme_converter import LegacyDmeConverter
from .legacy_smartman_converter import LegacySmartmanConverter
from .match_unmatch_converter import MatchUnmatchConverter

log = logging.getLogger(__name__)


DATABASE_ID = "DCSG"

class Converter(object):
    def __init__(self, maple_file, new_yaml=None,
                 testbed=None, testcase_control=None,
                 teststep_control=None, tims_testplan_folder=None):

        self.maple_file = maple_file
        self.new_yaml = new_yaml
        self.uids = []
        self.testbed = load(testbed) if testbed else runtime.testbed
        self.testcase_control = testcase_control
        self.teststep_control = teststep_control
        self.tims_testplan_folder = tims_testplan_folder

    def convert(self):

        """
        Function description: Receives the maple yaml file name and convert it into blitz yaml file

        args:

        returned_value:
            A list containing all the blitz trigger uids necessary to be used in the job file
        """

        blitz_dict = {}

        verify_maple_env()

        # File text into string
        with open(self.maple_file, 'r') as tempfile:
            maple_string = tempfile.read()

        # Replace all the maple markups
        maple_string = replace_maple_markups(maple_string, self.testbed)
        # create a dictionary object of the yaml file
        maple_dict = ruamel.yaml.safe_load(maple_string)
        for testcase_name, testcase_data in maple_dict['tests'].items():
            # multiple tests might exists within a maple testcase, and they all need to be extracted one by one
            blitz_dict.update({testcase_name: self.testcase_convertor(testcase_data,testcase_name)})

            # Adding the testcasename to a list
            # The list will be returned to job file so it would used as trigger uids
            self.uids.append(testcase_name)

        with open(self.blitz_file, 'w') as blitz_file_dumped:
            blitz_file_dumped.write(ruamel.yaml.round_trip_dump(blitz_dict))

        return self.uids

    def testcase_convertor(self, maple_testcase_data, maple_testcase_name):

        """Example of a maple testcase:
        tests:
            confirm_and_search:                 <-- testcase_name
                test-steps:                     <-- Everything from here on is testcase_data
                    step-1:                     <-- section name
                        confirm:
                            devices:
                                N93_3:
                                    rule-1:
                                        type: cli
                                        commands: |
                                            show vdc
        ___________________________________________________

        Function_description: Get each testcase within the maple yaml file and perform blitz conversion on it
        args:
            maple_testcase_data: The yaml data of one maple testcase
                                 datatype: dict

            maple_testcase_name: The name of one maple testcase
                                datatype: string

        returned_value:
            type(dict): containing the testcase maple that is converted to blitz
        """

        # Will generate the actual Testcase yaml
        blitz_testcase_data = {}
        # List of all the sections within a testcase
        blitz_sections_list = []

        # extracting various info such as log collection or tims logical id
        # from maple script and add the equivalent to the maple testcase
        pre_tc_dict= pre_testcase_checks(maple_testcase_data,
                                         self.testcase_control,
                                         self.teststep_control,
                                         self.tims_testplan_folder)

        section_continue = pre_tc_dict['section_cont']
        action_continue = pre_tc_dict['action_cont']
        blitz_testcase_data.update(pre_tc_dict['blitz_pre_tc_data'])

        # Each test would be map to one test in blitz and they all need source and class
        blitz_testcase_data.update({'source':
                           {'pkg': 'genie.libs.sdk',
                            'class': 'triggers.blitz.blitz.Blitz'},
                            'test_sections' : blitz_sections_list})

        # Maple steps are technically sections in blitz.
        # In blitz section are build on various actions,
        # Major actions in maple are confirm, apply and unapply,
        # which translates to various actions in blitz.
        if 'test-steps' not in maple_testcase_data:
            if  'confirm' in maple_testcase_data.keys() or\
                'apply' in maple_testcase_data.keys() or\
                'unapply' in maple_testcase_data.keys() :

                maple_testcase_data = {'test-steps': {'step-1':maple_testcase_data}}
            else:
                maple_testcase_data = {'test-steps': maple_testcase_data}

        # A maple testcase can have multiple sections and each section can have
        # up to 3 different action apply, confirm unapply
        for section, action_dict in maple_testcase_data['test-steps'].items():

            '''reminder blitz-format:
                    test_sections:
                        - <section-name>:
                            - <action-name>:
                                <key>: <value>
                                <key>: <value>
            '''

            # defining the list of actions
            blitz_action_list = []

            # if section continue == abort-on-failure
            # this would add the continue: False to the list of blitz actions for this section
            if section_continue == 'abort-on-failure':
                blitz_action_list.append({'continue': False})

            # Adding all the blitz action
            blitz_action_list = self.action_dispatcher(action_dict,
                                                        blitz_action_list,
                                                        action_continue,
                                                        section,
                                                        maple_testcase_name)

            blitz_sections_list.append({section: blitz_action_list})

        return blitz_testcase_data

    def action_dispatcher(self, action_dict, blitz_action_list, action_continue, section, maple_testcase_name):

        ''' Info: Three types of maple_actions exist:

                1 - apply
                2 - unapply
                3 - confirm

        ____________________
        Function description:
                This function simply dispatch maple_actions to the proper converter function
                that does the conversion of actions from maple to their blitz equivalent
        args:
            action_dict: maple actions in a dictionary
                        datatype: dict

            action_continue: the continue value for blitz action
                             datatype: boolean

        returned_value:
                type(list): A list of converted maple_actions to equivalent blitz actions for A section of A testcase
        '''

        # loop flag in case that the section has a loop
        # using this loop later we add the actions
        # underneath the loop keyword in blitz
        loop = False

        # This is the value to store output of an apply action and all of its commands
        # necessary in case a query is running on an apply action output
        val_to_search_apply = None

        # Check whether a maple action is confirm or apply/unapply
        for maple_action, data in action_dict.items():

            # checking for loop or control flow and update the dict
            blitz_action_list, loop = pre_section_checks(maple_action, data, blitz_action_list, loop)

            # dispatching apply/unapply actions to its converters
            if maple_action == 'apply' or maple_action == 'unapply':
                blitz_action_list, val_to_search_apply = self.apply_unapply_converter(
                                                           data,
                                                           blitz_action_list,
                                                           action_continue,
                                                           maple_action,
                                                           section,
                                                           maple_testcase_name,
                                                           loop)
            # dispatching confirm actions to its converters
            if maple_action == 'confirm':
                blitz_action_list = self.confirm_converter(data,
                                                           blitz_action_list,
                                                           action_continue,
                                                           section,
                                                           loop,
                                                           val_to_search_apply)

        return blitz_action_list

    def apply_unapply_converter(self,
                                 apply_unapply_data,
                                 blitz_action_list,
                                 action_continue,
                                 maple_action,
                                 section,
                                 maple_testcase_name,
                                 loop=None):

        ''' Example of the layout of apply action

        test-steps:
            step-1:
                apply: <--- maple_action
                    devices:
                        N93_3: <-- device to run the config on
                            type: cli <-- type of maple_action
                            commands: |  <---- commands that will be configured/applied to the device
                                conf t
                                feature bfd
        ____________________________________________
        Function description:

        args:
            apply_unapply_data:
        '''

        for dev, data in apply_unapply_data['devices'].items():

            # For IXIA legacy option connection was automatic but for plugins its manual
            # Then we need to connect it in plugins and since we translate legacy mode to
            # Plugins I need to add a connect on top of each IXIA legacy command
            if data['type'] == 'tgen-config':

                connect = '#@# cmds=connect: #@#                  \n'
                commands_actually = data['commands']
                data['commands'] = connect + commands_actually

            # dmerest flag
            dmerest = True if data['type'] == 'dmerest' else False

            # Different types of commands (cmds, plugins or show command)
            # might be the input of the apply action, these command needs
            # to separated
            command_type_list =_command_separator(data['commands'], dmerest=dmerest, configure=True)

            val_to_search_apply = "{}_{}_{}".format(maple_testcase_name, section, maple_action)

            for command in command_type_list:
                blitz_action_dict, blitz_action = self.maple_command_to_blitz_action_converter(data['type'],\
                                                        command, dev, maple_action)
                # This is hacky :-(
                # There is sometimes a need to match/umatch the output of a apply/configure action
                # Since match/unmatch would always be done in confirm section, we need to store that value
                # and send to confirm section so in case there is no commands, code performs match/unmatch
                if blitz_action == 'configure':
                    blitz_action_dict[blitz_action].update({'maple': True,
                                                            'save': [
                                                                {'variable_name': val_to_search_apply, 'append': True}
                                                                ]})


                if not action_continue or action_continue != 'continue-on-failure':
                    blitz_action_dict[blitz_action].update({'continue': False})

                # if loop, since
                # there would be technically one action in blitz
                # all the blitz actions should be moved underneath the loop keyword
                # TODO make it a function apply_with_loop
                if loop:
                    self._update_maple_action_with_loop(blitz_action_list, blitz_action_dict)
                else:
                    blitz_action_list.append(blitz_action_dict)

        return blitz_action_list, val_to_search_apply

    def confirm_converter(self,
                           confirm_data,
                           blitz_action_list,
                           action_continue,
                           section,
                           loop=None,
                           val_to_search_apply=None):

        ''' Example of the layout of confirm action

        step-2:
            confirm: <--- Maple action
                devices:
                    N93_3:
                        rule-1: <-- rule_id (To generate multiple confirm actions)
                            type: cli
                            commands: |
                                show vlan
                                show vrf
                                show nxapi
                                #@# cmds=waitfor:::show module,,Up,,10 #@#
        '''

        match_unmatch_flag = False

        # action confirms does have one more level called rule.
        # rules contains commands, and match/unmatch section, and the existance is and or or
        # which means there could be all of the together but there might be only match some times
        for dev, data in confirm_data['devices'].items():
            for rule_id, rule_data in data.items():

                # There might be confirm actions with not commands
                # Uses for cmds=eval which in turn === action compare in blitz
                # OR uses for match/unmatch an apply action
                # val_to_search_apply has use for that
                if 'commands' not in rule_data:
                    blitz_action_dict = {}
                    muc = MatchUnmatchConverter()
                    blitz_action_dict = muc.match_unmatch_dispatcher(
                                               blitz_action_dict, 'compare', rule_data['type'],\
                                               rule_id, device=dev, match=rule_data.get('match'), \
                                               unmatch=rule_data.get('unmatch'), val_to_search_apply=val_to_search_apply)

                    blitz_action_list.append(blitz_action_dict)
                    continue

                # command_separator extract each command from the list of inputted
                # commands and returns them in a list. 3 types of commands exist in a confirm action
                # Normal as ('show_version', 'show interface'),
                # Plugin commands that are python function as ('commandplugins' and 'matcherplugins'),
                # pattern matching commands that as (#cmds=patterns:::)
                command_type_list = _command_separator(rule_data['commands'])
                # function to translate cmds patterns to blitz equivalent
                # then it is arithmetic match
                val_to_search = "{}_{}_match_unmatch".format(section, rule_id)

                for command in command_type_list:

                    # command_translator gets each command, and based on their type (normal command or plugins)
                    # returns the type of action(s) that would be executed in blitz
                    # and the dictionary representation of the action and its arguments
                    blitz_action_dict, action = self.maple_command_to_blitz_action_converter(
                                                        rule_data['type'],
                                                        command,
                                                        dev,
                                                        'confirm',
                                                        rule_id)

                    if rule_data.get('match') or rule_data.get('unmatch'):

                        match_unmatch_flag = True
                        # TODO One loop limitation that cannot loop over a multiple command
                        # single confirm action (Yet never seen its example)
                        # if loop and because of the mentioned limitation, there is always one command to be queried
                        # Hence no need to append
                        save_list = [{'variable_name': val_to_search}]
                        if not loop:
                            save_list[0].update({'append': True})

                        try:
                            blitz_action_dict[action].update({'save': save_list})
                        except KeyError:
                            if "specifically_patterns" in blitz_action_dict:
                                pass

                    if not action_continue or action_continue != 'continue-on-failure':
                        try:
                            blitz_action_dict[action].update({'continue': False})
                        except KeyError:

                            # for cmds=patterns the output would be a dictionary of
                            # multiple blitz actions that is saved into a list
                            # It is necessary to update all those actions one by one
                            if "specifically_patterns" in blitz_action_dict:
                                blitz_action_dict.update({action:{'continue': False}})

                    if loop:
                        self._update_maple_action_with_loop(blitz_action_list, blitz_action_dict)
                    else:
                        if "specifically_patterns" in blitz_action_dict:
                            self._update_maple_actions_with_cmds_patterns(
                                                blitz_action_list, blitz_action_dict, action)
                        else:
                            blitz_action_list.append(blitz_action_dict)

                # in case match/unmatch exist, a map should be constructed
                # between match/unmatch to include/exclude
                # and the blitz action dictionary will be updated
                # match/unmatch might not always map to include exclude
                # they can be mapped to an equivalent action in blitz
                if match_unmatch_flag:
                    self._update_maple_actions_with_match_unmatch(blitz_action_dict,
                                                                  rule_data,
                                                                  rule_id,
                                                                  dev,
                                                                  val_to_search)

        return blitz_action_list

    # Need better Name
    def maple_command_to_blitz_action_converter(self, maple_action_type, command, device, maple_action, rule_id=None):

        ''' Example of different commands in maple
            confirm:
                devices:
                    N93_3:
                        rule-1: <-- rule_id
                            type: dmerest|yangrest|cli|tgen-config|smartman <-- all type of maple_action_type
                            commands: |
                                show module                                         <-- show commands
                                #@# cmds=waitfor:::show module,,Up,,10 #@#          <-- cmds commands

                                                                                    <-- plugin commands
                                #@# matcher:{                                       <-- plugin_type == matcher|confirm|commands
                                    "package":"maple.plugins.user.MatcherPlugins",  <-- package that plugin is residing in maple code
                                    "method":"populateObjects",                     <-- plugin method that will be called in maple code
                                    "command":"show version",                       <-- from here on out, the arguments to that maple plugin method
                                    "type":"cli"
                                    }
                                #@#

                                get,, <url>                                         <-- legacy dme commands
            __________________________________
            function description:
                Get a SINGLE command within a maple action and translate them into an equivalent blitz action

            args:
                command: whether cmds commands, show command, legacy_dme command or plugin commands
                         datatype: string if command == <show command> OR datatype: dict if cmds commands or plugin commands

                maple_action_type: type of maple_action whether it is (cli, dmerest, yangrest)
                                    datatype: string

                device: device that will actions executed on
                        datatype: string

                maple_action: confirm, apply, unapply
                              datatype: string

                rule_id: (optional) - the rule name for possible confirm action that will perform.
                         datatype: string

            returned_value:
                type(dict): containing the blitz action equivalent of each maple commands
                type(string): the blitz action name of the converted maple command
        '''

        # When stated as command, a plugin_type either can be of type matcher, or command
        plugin_type = 'command' if maple_action_type != 'matcher' else 'matcher'

        # if type of maple_action is dmerest and if command is not a dictionary
        # which means that the command is not for a plugin but for a legacy dme
        # legacy dme ex: get,, http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json
        # the legacy dme needs to be translated into its plugins equivalent
        # so blitz would understand it
        if maple_action_type == 'dmerest' and not isinstance(command, dict):

            # dme legacy commands needs to be converted to maple plugins arguments first
            # a LegacyDmeConverter object first created
            ldc = LegacyDmeConverter(command, maple_action)

            # converting legacy_dme_to_maple_plugin
            # command -> plugins command -> dictionary
            command = ldc.legacy_dme_to_maple_plugin_converter()

        # if type of maple_action is smartman
        # it means that the command should use a smartman cli
        # Blitz does not support smartman
        # Hence the smartman input should be converted into a smartman plugin
        # so blitz would understand it
        elif maple_action_type == 'smartman':

            # smartman commands needs to be converted to maple plugins arguments first
            # a LegacySmartmanConverter object first created
            lsc =  LegacySmartmanConverter(command)

            # converting smartman_to_maple_plugin
            # command -> plugins command -> dictionary
            command = lsc.smartman_to_maple_plugin_converter()

        # If the command is a dictionary then it is either cmds command or plugins command
        if isinstance(command, dict):

            # These cmds= are in the group of maple commands, such as waitfor, runraw etc.
            # All these should be translated from cmds= to plugin and then translated into blitz_action
            # Exception is cmds=patterns that directly translates to a list of blitz_action
            if 'cmds=' in command['plugin']:

                # cmds= commands all need to be translated into a plugin first
                # so blitz could understand it
                cmds_converter = CmdsConverter(command['plugin'], maple_action_type)

                # converting cmds commands to maple
                # command -> plugins command -> dictionary
                command =  cmds_converter.cmds_to_maple_plugin_converter()

                # There are two exceptions when translating cmds= commands to plugins cmds=patterns and cmds=eval
                # if the cmds=patterns (cmds= of type "patterns") then instead of translating it into a maple_plugins
                # we directly convert cmds=patterns into a dictionary containing a list of blitz actions
                # if maple action type is matcher and if cmds=pattrens
                if maple_action_type == 'matcher' and command.get('type') == 'patterns':
                    return cmds_converter.cmds_patterns_to_blitz_action_converter(
                                                                command['data'], device), 'execute'

                if command.get('type') == 'groups':
                    return cmds_converter.cmds_groups_command_to_blitz_action_converter(
                                                                command['data'], device), 'execute'

            # Whether if it is plugins commands the following function would convert it into a blitz action
            # if cmds= commands (with exception of two) they are already translated in maple plugins above
            # all of them now will be converted as maple plugin into an blitz action
            return plugin_to_blitz_action_converter(command,
                                                    maple_action_type,
                                                    device=device,
                                                    maple_action=maple_action,
                                                    plugin_type=plugin_type,
                                                    rule_id=rule_id), 'maple'

        # if command is not a dictionary then it is a show command
        else:
            # Normal commands translation
            # if maple_action == apply, unapply | blitz_action action configure
            # if maple_action == confirm | blitz action execute
            blitz_action = 'execute' if maple_action == 'confirm' else 'configure'

            # show commands translated into a blitz action
            return show_command_to_blitz_action_converter(command, device, blitz_action), blitz_action

    def _update_maple_action_with_loop(self, blitz_action_list, blitz_action_dict):

        if 'actions' not in blitz_action_list[0]['loop']:
            blitz_action_list[0]['loop'].update({'actions':[blitz_action_dict]})
        else:
            blitz_action_list[0]['loop']['actions'].append(blitz_action_dict)

    def _update_maple_actions_with_cmds_patterns(self, blitz_action_list, blitz_action_dict, action):

        cont_ = blitz_action_dict.pop(action, None)
        for item in blitz_action_dict['specifically_patterns']:
            if cont_:
                item[action].update({'continue': False})
            blitz_action_list.append(item)

    def _update_maple_actions_with_match_unmatch(self,
                                                 blitz_action_dict,
                                                 rule_data,
                                                 rule_id,
                                                 dev,
                                                 val_to_search):

        if "specifically_patterns" in blitz_action_dict:
            for action_dict in blitz_action_dict['specifically_patterns']:
                muc = MatchUnmatchConverter()
                action_dict = muc.match_unmatch_dispatcher(
                                    action_dict, 'maple_search', rule_data['type'],
                                    rule_id, device=dev, match=rule_data.get('match'),
                                    unmatch=rule_data.get('unmatch'), val_to_search=val_to_search)
        else:
            muc = MatchUnmatchConverter()
            blitz_action_dict = muc.match_unmatch_dispatcher(
               blitz_action_dict, 'maple_search', rule_data['type'],
               rule_id, device=dev, match=rule_data.get('match'),
               unmatch=rule_data.get('unmatch'), val_to_search=val_to_search)

    @property
    def testbed_file(self):
        '''
        This function adds os line to IXIA devices
        and generates a new testbed_file if need be
        '''

        blitz_overwritten_testbed = None
        runtime.job.testbed = self.testbed
        testbed_dict = self.testbed.raw_config

        for dev, dev_args in testbed_dict['devices'].items():
            if dev_args['type'] == 'ixia' and 'os' not in dev_args:
                dev_args['os'] = 'ixianative'

                dir_name = os.path.dirname(os.path.abspath(self.testbed.testbed_file))
                file_name = 'blitz_{}'.format(os.path.basename(
                                              os.path.abspath(self.testbed.testbed_file)))

                blitz_overwritten_testbed= os.path.join(dir_name, file_name)

        if blitz_overwritten_testbed:

            with open(blitz_overwritten_testbed, 'w') as f:
                f.write(ruamel.yaml.round_trip_dump(testbed_dict))
            return blitz_overwritten_testbed

        return os.path.abspath(self.testbed.testbed_file)

    @property
    def blitz_file(self):

        maple_script_full_path = os.path.abspath(self.maple_file)
        maple_script_path_splited = os.path.split(maple_script_full_path)
        blitz_script_file_name = maple_script_path_splited[1]
        dir_name = maple_script_path_splited[0]

        if not self.new_yaml:
            blitz_file_name = 'blitz_{}'.format(blitz_script_file_name)
        else:
            blitz_file_name = self.new_yaml


        return '{}/{}'.format(dir_name, blitz_file_name)

# IF YOU WANT TO ONLY CONVERT TWO SCRIPTS
# SIMPLY CALL THE CONVERTOR FUNCTION WITH
# THE NAME OF YOUR TESTSCRIPT AS AN ARGS

# converter = Converter('groups.yaml')
# # converter = Converter('anycast_testcase.yaml')

# trigger_uids = converter.convert()
