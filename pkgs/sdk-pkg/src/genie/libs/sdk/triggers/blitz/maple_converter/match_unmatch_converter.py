import re
import json
import ruamel.yaml

from .utils import replace_maple_markups,\
                   pre_testcase_checks,\
                   pre_section_checks, \
                   _XX_pattern_matching,\
                   verify_maple_env,\
                   _command_separator,\
                   plugin_to_blitz_action_converter,\
                   show_command_to_blitz_action_converter

from .cmds_converter import CmdsConverter


class MatchUnmatchConverter(object):

    def match_unmatch_dispatcher(self,
                                 blitz_action_dict, maple_action, maple_action_type,
                                 rule_id, device=None, match=None,
                                 unmatch=None, val_to_search=None, val_to_search_apply=None):
        """
        function description:  This function simply dispatch match/unmatch cases to the converter function

        args:
            blitz_action_dict: match/unmatch will add an action to the previous blitz_action_dict which has already a maple/execute/configure action in it
            maple_action: confirm/apply/unapply
            maple_action_type: (dmerest/cli/tgen-config etc.)
            rule_id: confirm action rule_id
            device: device name
            match: all the values that should be found the actions output
            unmatch: all the values that shouldn't be found the actions output
            val_to_search: variable to store the output of a confirm action and pass it to be searched for match/unmatchs
            val_to_search_apply: variable to store the output of an apply action and pass it to be searched for match/unmatchs

        returned_value: dictionary value containing the equivalent action of match/unmatch in blitz
        """

        if not match and not unmatch:
            return blitz_action_dict

        _include_list = _command_separator(match) if match else []
        _exclude_list = _command_separator(unmatch) if unmatch else []

        blitz_action_dict = self._match_unmatch_converter('include',
                                                          blitz_action_dict,
                                                          maple_action_type,
                                                          rule_id, device,
                                                          _include_list, val_to_search, val_to_search_apply)

        blitz_action_dict = self._match_unmatch_converter('exclude',
                                                          blitz_action_dict,
                                                          maple_action_type,
                                                          rule_id, device,\
                                                          _exclude_list, val_to_search,
                                                          val_to_search_apply)

        return blitz_action_dict

    def _match_unmatch_converter(self,
                                style,
                                blitz_action_dict,
                                maple_action_type,
                                rule_id,
                                device=None,\
                                _match_unmatch_list=None,
                                val_to_search=None,
                                val_to_search_apply=None):

        '''
            Explanation:
                1) if the match/unmatch values are simple values or regex then the blitz_action_dict contains already converted
                   maple actions. The output of those blitz actions are saved into val_to_search variable, and in this function
                   a maple_search would be created that would query that val_to_search variable.

                2)If the match/unmatch is confirm plugins, the input would convert into a blitz maple action to call the plugins
                  from the blitz code

                3)If the input is a cmds=eval then an arithmetic/logical statement is in the input. Blitz action compare is
                  the equivalent of this cmds= command

            EX-1)
            confirm:
                devices:
                    N93_3:
                        rule-1:
                            type: cli
                            commands: |
                                show vdc
                                show vrf
                            match: |
                                .*
                                UP
            ==============================
            - execute:
                device: N93_3
                command: show vdc
                save:
                - variable_name: rule-1_match_unmatch
                  append: true
              execute:
                device: N93_3
                command: show vrf
                save:
                 - variable_name: rule-1_match_unmatch
                   append: true
              maple_search:
                search_string: '%VARIABLES{rule-1_match_unmatch}'
                device: N93_3
                include:
                - .*
                - UP

            EX-2)
            step-2:
                confirm:
                    devices:
                        N93_3:
                            rule-1:
                                type: cli
                                commands: |
                                    show module
                                match: |
                                    #@# confirm:{
                                        "package":"maple.plugins.user.ConfirmPlugins",
                                        "method":"checkIfPresent",
                                        "options":[
                                            {"count":"1"},
                                            {"check1": "XX(dummy_key_name)XX"}
                                        ]}
                                    #@#
            ====================================================
            - step-2:
              - execute:
                  command: show module
                  continue: false
                  device: N93_3
                  save:
                  - append: true
                    variable_name: rule-1_match_unmatch
                maple:
                  device: N93_3
                  output: '%VARIABLES{rule-1_match_unmatch}'
                  section: '{"rule-1": {"type": "cli", "commands": "confirm:{\n    \"package\":\"maple.plugins.user.ConfirmPlugins\",\n    \"method\":\"checkIfPresent\",\n    \"options\":[\n        {\"count\":\"1\"},\n        {\"check1\":
                    \"%VARIABLES{dummy_key_name}\"}\n    ]}"}}'

            EX-3)
            step-2-get:
                confirm:
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
                                match: |
                                    #@# cmds=eval:::'XX(adminSt)XX' == 'enabled' #@#
                ======================================================
            - step-2-get:
              - continue: false
              - maple:
                  section: '{"rule-1": {"type": "dmerest", "commands": "command:{\n    \"method\":\"processdme\",\n    \"options\":[\n        {\"method\":\"GET\"},\n        {\"url\":\"http://acjain-laas:8001/api/node/mo/sys/ldp.json\"}\n    ]}"}}'
                  device: N93_3
                  save:
                  - variable_name: rule-1_match_unmatch
                    append: true
                  continue: false
                compare:
                  items:
                  - "'%VARIABLES{adminSt}' == 'enabled'"
        ____________________
        args:
            blitz_action_dict: match/unmatch will add an action to the previous blitz_action_dict which has already a maple/execute/configure action in it
            maple_action: confirm/apply/unapply
            maple_action_type: (dmerest/cli/tgen-config etc.)
            rule_id: confirm action rule_id
            device: device name
            _match_unmatch_list: list containing the values that would be used for checking their inclusion/exclusion
            val_to_search: variable to store the output of a confirm action and pass it to be searched for match/unmatchs
            val_to_search_apply: variable to store the output of an apply action and pass it to be searched for match/unmatchs

        returned_value: dictionary value containing the equivalent action of match/unmatch in blitz
        '''

        storage_list = []
        if not _match_unmatch_list:
            return blitz_action_dict

        # TODO : Fix the - not showing in yaml file (the fix should be done somewhere here)
        # val_to_search is to search the output of a confirm section
        # (bunch of show commands output that are appended together are stored in val_to_search)
        # val_to_search has priority over val_to_search_apply
        # that means if val_to_search is there val_to_search_apply will be ignored
        # val_to_search_apply for checking the include/exclude for outputs of the
        # apply section (could be equivalent of multiple actions in blitz)
        # This only applies when confirm section doesn't exist
        if val_to_search:
            blitz_action_dict.update(
                            {'maple_search':{'search_string': "%VARIABLES{}".format('{'+val_to_search+'}'),
                             'device': device
                             }
                            })

        elif val_to_search_apply:
            blitz_action_dict.update(
                            {'maple_search':{'search_string': "%VARIABLES{}".\
                              format('{'+val_to_search_apply+'}'),
                             'device': device
                             }
                            })

        for item in _match_unmatch_list:
            if isinstance(item, dict):

                # if in cmds=eval::: then it is an arithmetic/logical operation
                # mapped to action compare in blitz
                if 'cmds=' in item['plugin']:

                    cmds_converter = CmdsConverter(item['plugin'], maple_action_type)
                    # converting cmds commands to maple
                    # command -> plugins command -> dictionary
                    command =  cmds_converter.cmds_to_maple_plugin_converter()

                    # if cmds= then it is surely cmds=eval and it is a compare scenario
                    if command.get('type') == 'eval':
                        plugin_dict = cmds_converter.cmds_eval_to_blitz_action_converter(command['data'])

                    elif command.get('type') == 'groups':
                        plugin_dict = cmds_converter.cmds_groups_match_to_blitz_action(command['data'])

                    blitz_action_dict.update(plugin_dict)
                else:
                    # if it is a plugin it would ba confirm plugin_type which will be a maple action
                    plugin_dict = plugin_to_blitz_action_converter(item,
                                                                   maple_action_type,
                                                                   device=device,
                                                                   plugin_type='confirm',
                                                                   rule_id=rule_id)

                    if blitz_action_dict and val_to_search:
                        # if previously an action execute exist on this match/unmatch
                        # The output of that action execute needs to be stored for the
                        # maple action further use
                        plugin_dict['maple'].update({'output': "%VARIABLES{}".\
                                                      format('{'+val_to_search+'}')})

                    blitz_action_dict.update(plugin_dict)
            else:
                # This variable will put all the item whether int/boolean/str
                # in the double quote, which is necessary to not face any issue
                # in Blitz
                item = _XX_pattern_matching(str(item), 'replace')
                double_quote = ruamel.yaml.scalarstring.DoubleQuotedScalarString
                storage_list.append(double_quote(item))
                blitz_action_dict['maple_search'].update({style: storage_list})

        # if include/exclude added to maple_search there is
        # no point of having the maple_search in the output
        if 'maple_search' in blitz_action_dict:
            if 'include' not in blitz_action_dict['maple_search'] and\
               'exclude' not in blitz_action_dict['maple_search']:
                blitz_action_dict.pop('maple_search')

        return blitz_action_dict