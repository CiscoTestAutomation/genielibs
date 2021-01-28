import re
from genie.libs.sdk.triggers.blitz.maple_converter.legacy_maple_converter import InternalConverter

from .utils import _XX_pattern_matching,\
                   _XR_pattern_matching,\
                   _command_separator


class CmdsConverter(InternalConverter):

    def __init__(self, command, maple_action_type):
        super().__init__()

        self.command = command
        self.maple_action_type = maple_action_type


    def cmds_to_maple_plugin_converter(self):

        '''
        Maple various cmds commands:
            cmds=patterns::: used for pattern matching
            cmds=eval::: used for performing arithmatic/logical
            anything that follows:
            cmds=<cmds_name>: is a legacy command
            _________________________________________
            returned_value:
                for cmds_patterns: a dictionary containing cmds=patterns info to be later on translated directly to blitz action
                for cmds_eval: a dictionary containing cmds=patterns info to be later on translated directly to blitz action
                for legacy_commands: legacy commands are translated into a their maple plugin equivalent
        '''

        pattern = re.compile(r'cmds=(?P<type>[\w\s]+):{1,3}(?P<data>[\S\s]+)?')
        m = pattern.match(self.command.strip())

        group = m.groupdict()
        if group['type'].strip() in ['patterns', 'eval', 'groups']:
            return group

        else:
            if self.maple_action_type == 'tgen-config':

                # legacy commands are translated into a list of arguments for its maple_plugin equivalent,
                legacy_ixia_plugins_args = self.ixia_legacy_cmds_to_plugin_args(group['type'].strip(),
                                                                                group['data'])
                # Then translated into maple plugin
                return self.legacy_cmds_to_maple_plugin_converter('ixia',
                                                                  legacy_ixia_plugins_args)
            else:
                # legacy commands are translated into a list of arguments for its maple_plugin equivalent,
                legacy_cmds_plugins_args = self.legacy_cmds_to_plugin_args(group['type'].strip(),
                                                                           group['data'])
                # Then translated into a maple plugin
                return self.legacy_cmds_to_maple_plugin_converter(
                                                                   group['type'].strip(),
                                                                   legacy_cmds_plugins_args)

    def ixia_legacy_cmds_to_plugin_args(self, _type, args_):

        ''' Example of ixia legacy commands in maple
            step-1:
                apply:
                    devices:
                        TGEN-1:
                            type: tgen-config
                            chassis: IXIA
                            commands: |
                                #@# cmds=startprotocols: #@#
                                #@# cmds=cleanupsession: #@#
                                #@# cmds=loadconfig:/ws/vinavisw-ott/nx/maple/MPLS/SRTE-I/SRTE-Traffic/SRTE9.ixncfg #@#
            ____________________________________________
            returned_value: a list containing the arguments for ixia maple plugins such as :
            ['{"command": "gettrafficstats"}', '{"sleep": "10"}']

        '''

        # translate legacy mode ixia commands to new plugin inputs,
        args_list= []

        args_list.append('{{"command":"{}"}},\n'.format(_type))
        # args_list.append('{"use_https": "False"},\n')

        if _type == 'trafficstats':
            args_list[0] = '{{"command":"{}"}},\n'.format('gettrafficstats')
            args_list.append('{{"sleep":"{}"}},\n'.format(args_))
        elif _type == 'loadconfig':
            args_list.append('{{"config_files":["{}"]}},\n'.format(args_))

        return args_list

    def legacy_cmds_to_plugin_args(self, _type, args_):

        '''
        Function description: All the legacy cmds except for dme, smartman and ixia ones
                              comes to this function and then either the args created here
                              like for switchto, suspendvdc, novpc etc
                              OR it gets passed to its designated function

        return_value: a list of arguments that would be used as input to the command maple plugin call
        '''
        if not args_:
            return []

        # gets the cmds=<command> and call the proper function
        type_func_str = "_cmds_{f}_translate"

        if _type in ['switchto', 'suspendvdc']:

            argument = '{{"value":"{}"}},\n'.format(args_)
            return [argument]

        elif _type in ['novpc', 'sso', 'sleep']:

            if args_:
                argument = '{{"duration":"{}"}},\n'.format(args_)
                return [argument]

        elif _type in ['killprocess', 'dialog',
                       'runonmodule', 'runraw',
                       'waitfor', 'issu',
                       'copy' ]:

            return getattr(self, type_func_str.format(f=_type))(args_)
        elif 'reload' in _type:
            return self._cmds_reload_translate(_type, args_)

        else:
            raise Exception("The cmds function {} does not exist".format(_type))

    def cmds_patterns_to_blitz_action_converter(self, cmd_pattern, device):

        '''
            step-3:
                confirm:
                    devices:
                        N93_3:
                            matcher_populate:
                                type: matcher
                                commands: |
                                    #@# cmds=patterns:::
                                    [show version,,BIOS:\s+version\s+XX(bios)XX([0-9A-Za-z()./]+).*]
                                    [show version,,bootflash:\s+XX(bootflash)XX([0-9A-Za-z()./]+)\s+XX(measure)XX(\w+).*]
                                    [show vrf,,default\s+XX(default)XX([0-9/]+)\s+XX(up_down)XX(Up|Down).*]
                                    #@#
            ==================================================
              - step-3:
                - continue: false
                - execute:
                    command: show version
                    device: N93_3
                    save:
                    - filter: BIOS:\s+version\s+(?P<bios>[0-9A-Za-z()./]+).*
                      regex: true
                    - filter: bootflash:\s+(?P<bootflash>[0-9A-Za-z()./]+)\s+(?P<measure>\w+).*
                      regex: true
                - execute:
                    command: show vrf
                    device: N93_3
                    save:
                    - filter: default\s+(?P<default>[0-9/]+)\s+(?P<up_down>Up|Down).*
                      regex: true

            ____________________________________________
            return_output_example:
                {'specifically_patterns': [
                    {'execute': {'device': 'N93_3', 'command': 'show version',
                    'save': [{'filter': 'BIOS:\\s+version\\s+(?P<bios>[0-9A-Za-z()./]+).*', 'regex': True}, {'filter': 'bootflash:\\s+(?P<bootflash>[0-9A-Za-z()./]+)\\s+(?P<measure>\\w+).*', 'regex': True}]}},
                    {'execute': {'device': 'N93_3', 'command': 'show vrf',
                    'save': [{'filter': 'default\\s+(?P<default>[0-9/]+)\\s+(?P<up_down>Up|Down).*', 'regex': True}
                    ]}}]}

        '''
        cmds_dict = {}
        blitz_action_list = []
        for cmd in cmd_pattern.splitlines():
            cmd = cmd.strip()
            if not cmd:
                continue

            cmds_list = cmd.strip('[]').split(',,')
            if cmds_list[0] not in cmds_dict:
                cmds_dict.update({cmds_list[0]: [cmds_list[1]]})
            else:
                cmds_dict[cmds_list[0]].append(cmds_list[1])

        for key, value in cmds_dict.items():

            blitz_action_dict = {}
            blitz_action_dict.update({'execute':{'device': device, 'command': key}})
            value_list = []
            for val in value:
                val = _XX_pattern_matching(val, 'save')
                val = _XR_pattern_matching(val)
                value_list.append({'filter': val, 'regex': True})
                blitz_action_dict['execute'].update({'save':value_list})

            # when checking the pattern matching
            # in matcher section
            # there might be a need for returning
            # multiple actions,
            # The goal here is to achieve that.
            # by strong all the blitz actions created in a ret_list
            blitz_action_list.append(blitz_action_dict)

        # returning it as a dictionray with a keyword to specify that a list of blitz actions are comming
        # because of cmds=patterns in maple
        # This later on would be unpacked
        # hacky :-(
        return {'specifically_patterns': blitz_action_list}

    def cmds_groups_command_to_blitz_action_converter(self, cmd_groups, device):

        # groups legacy commands, it should be originally changed into matcher in all the other maple scripts

        '''
            step-5:
                confirm:
                    devices:
                        NX2:
                          rule-1:
                            type: cli
                            commands: |
                                #@# cmds=groups:::
                                [ping6 77:77:77::2 vrf vrf_2_7_8 count 5,,\d+ packets transmitted, \d+ packets received, ([0-9.]+)% packet loss]
                                #@#
                            match: |
                                #@# cmds=groups:::1.1 <= 1.0 #@#
                          rule-2:
                            type: cli
                            commands: |
                                #@# cmds=groups:::
                                [sh int ethernet 1/6/1 counters detailed | section Rx | begin Packets,,Rx Packets:\s+(\d+)]
                                #@#
                            match: |
                                #@# cmds=groups:::1.1 > 1000 #@#

        =====================================================================

            - step-5:
              - execute:
                  device: NX2
                  command: ping6 77:77:77::2 vrf vrf_2_7_8 count 5
                  save:
                  - filter: \d+ packets transmitted, \d+ packets received, (?P<name1_1>[0-9.]+)%
                      packet loss
                    regex: true
                  continue: false
                compare:
                  items:
                  - '%VARIABLES{name1_1} <= 1.0'
              - execute:
                  device: NX2
                  command: sh int ethernet 1/6/1 counters detailed | section Rx | begin Packets
                  save:
                  - filter: Rx Packets:\s+(?P<name1_1>\d+)
                    regex: true
                  continue: false
                compare:
                  items:
                  - '%VARIABLES{name1_1} > 1000'
        '''

        pattern = re.compile(r"\(([\S\s]+?)\)")
        cmds_dict = {}
        blitz_action_list = []
        cmds_group_list = cmd_groups.split('\n')
        cmds_group_list = [cmd for cmd in cmds_group_list if cmd]
        for cmd in cmds_group_list:

            name_index = cmds_group_list.index(cmd) + 1
            cmds_list = cmd.strip('[]').split(',,')
            matches = list(re.finditer(pattern, cmds_list[1].strip()))

            for match in matches:
                regex_index = matches.index(match) + 1
                save_var_name_regx = '?P<{}>'.format('name'+str(name_index)+'_'+str(regex_index))
                cmds_list[1] = cmds_list[1].replace(match.group(1), '{}'.format(save_var_name_regx+match.group(1)))

            if cmds_list[0] not in cmds_dict:
                cmds_dict.update({cmds_list[0]: [cmds_list[1].strip()]})
            else:
                cmds_dict[cmds_list[0]].append(cmds_list[1].strip())

        for key, value in cmds_dict.items():
            blitz_action_dict = {}
            blitz_action_dict.update({'execute':{'device': device, 'command': key}})
            value_list = []
            for val in value:
                val = _XX_pattern_matching(val, 'save')
                val = _XR_pattern_matching(val)
                value_list.append({'filter': val, 'regex': True})
                blitz_action_dict['execute'].update({'save':value_list})

            blitz_action_list.append(blitz_action_dict)

        return {'specifically_patterns': blitz_action_list}

    def cmds_groups_match_to_blitz_action(self, cmd_groups):

        pattern = re.compile(r'(?P<left_hand>\d+.\d+)\s*(?P<ops>[><=]+)\s*(?P<right_hand>[\S\s]+)')
        compare_item_list = []
        blitz_action_dict = {}

        for cmd in cmd_groups.splitlines():
            cmd = cmd.strip()
            if not cmd:
                continue
            cmds_groups_list = re.split(r"and|or", cmd)

            for itm in cmds_groups_list:
                itm = itm.strip()
                m = pattern.match(itm)
                group = m.groupdict()
                left_hnd_val = group['left_hand'].replace('.','_')
                left_hnd_val = 'name' + left_hnd_val
                left_hnd_val = '%VARIABLES{}'.format('{'+left_hnd_val+'}')
                cmd = cmd.replace(group['left_hand'], left_hnd_val)

            compare_item_list.append(cmd)
            blitz_action_dict.update({'compare':{'items':compare_item_list}})

        return blitz_action_dict

    def cmds_eval_to_blitz_action_converter(self, cmd_eval):

        #changing cmds=eval to compare action in blitz
        blitz_action_dict = {}
        compare_item_list = []
        for cmd in cmd_eval.splitlines():
            cmd = cmd.strip()
            if not cmd:
                continue
            cmd = _XX_pattern_matching(cmd, 'replace')
            compare_item_list.append(cmd)
        blitz_action_dict.update({'compare':{'items':compare_item_list}})

        return blitz_action_dict

    def _cmds_dialog_translate(self, data):

        '''
            syntax:
                #@# cmds=dialog:::command~{"dialog-list":[["request text","request response"],["request text","request response"]]}~sleep_value~timeout #@#

            example:
                #@# cmds=dialog:::show tech-support routing ip unicast > urib_v4.ts~{"dialog-list":[["Do you want to overwrite","y"]]}~0~120 #@#
        '''

        data_list = data.split('~')

        data_list[0] = '{{"cmd":"{}"}},\n'.format(data_list[0])
        data_list[1] = '{{"dialog-list":{}}},\n'.format(data_list[1])
        data_list[2] = '{{"sleep":"{}"}},\n'.format(data_list[2])
        if len(data_list) == 4:
            data_list[3] = '{{"timeout":"{}"}},\n'.format(data_list[3])

        return data_list

    def _cmds_killprocess_translate(self, args_):

        '''
            syntax:

                n7k
                    #@# cmds=killprocess:<media>,<debug plugin>,<process name> #@#
                n9k
                    #@# cmds=killprocess:<process name> #@#

            example:
                #@# cmds=killprocess:bootflash,debug-img,l3vm #@#
                #@# cmds=killprocess:ulib #@#
        '''

        args_splited = args_.split(',')

        if len(args_splited) > 1:
            args_splited[0] = '{{"media":"{}"}},\n'.format(args_splited[0])
            args_splited[1] = '{{"debug_plugin":"{}"}},\n'.format(args_splited[1])
            args_splited[2] = '{{"process_name":"{}"}},\n'.format(args_splited[2])
        else:
            args_splited[0] = '{{"process_name":"{}"}},\n'.format(args_splited[0])

        return args_splited

    def _cmds_copy_translate(self, args_):

        '''
            syntax:

                #@# cmds=copy:<server>,<source>,<vrf>,<username>,<password>,<media>,<source file with path>,<destination file>,<optional compact copy true|false> #@#

            example:
                #@# cmds=copy:123.100.101.79,scp,management,root,roZes,bootflash,/ws/skasimut-ott/images/n7700-s2-dk9.8.0.1.bin,n7700-s2-dk9.8.0.1.bin,true #@#

        '''

        args_splited = args_.split(',')
        temp_list = []
        args_splited[0] = '{{"server":"{}"}},\n'.format(args_splited[0])
        args_splited[1] = '{{"source":"{}"}},\n'.format(args_splited[1])
        args_splited[2] = '{{"vrf":"{}"}},\n'.format(args_splited[2])
        args_splited[3] = '{{"username":"{}"}},\n'.format(args_splited[3])
        args_splited[4] = '{{"password":"{}"}},\n'.format(args_splited[4])
        args_splited[5] = '{{"media":"{}"}},\n'.format(args_splited[5])
        args_splited[6] = '{{"source_file":"{}"}},\n'.format(args_splited[6])
        if len(args_splited) > 7:
            temp_list = args_splited[7:]

            if len(temp_list) == 2:
                args_splited[7] = '{{"dest_file":"{}"}},\n'.format(args_splited[7])
                args_splited[8] = '{{"compact_copy":"{}"}},\n'.format(args_splited[8])
            else:
                args_splited[7] = '{{"dest_file":"{}"}},\n'.format(args_splited[7])

        return args_splited

    def _cmds_reload_translate(self, _type, args_):
        '''
            syntax_reload:
                #@# cmds=reload:<sleep in seconds, default is 0>,<skip copy running-config to startup-config, True|False, default is False>,<timeout in seconds, default is 1200>,<ascii reload, True|False, default is False> #@#

            syntax_reload_vdc:
                #@# cmds=reload_vdc:<vdc name> #@#

            syntax_reload_module:
                #@# cmds=reload_module:<module> #@#

            Examples:
                #@# cmds=reload_module:1 #@#
                #@# cmds=reload_vdc:VDC1 #@#
                #@# cmds=reload:360 #@#
                #@# cmds=reload: #@#
        '''

        if not args_:
            return ['{{"command":"{}"}},\n'.format(_type)]

        args_splited = args_.split(',')
        if _type == 'reload':
            if len(args_splited) == 1:
                args_splited[0] = '{{"sleep":"{}"}}\n'.format(args_splited[0])

            if len(args_splited) == 2:
                args_splited[0] = '{{"sleep":"{}"}},\n'.format(args_splited[0])
                args_splited[1] = '{{"no_copy_rs":"{}"}}\n'.format(args_splited[1])

            if len(args_splited) == 3:

                args_splited[0] = '{{"sleep":"{}"}},\n'.format(args_splited[0])
                args_splited[1] = '{{"no_copy_rs":"{}"}},\n'.format(args_splited[1])
                args_splited[2] = '{{"timeout":"{}"}}\n'.format(args_splited[2])

            if len(args_splited) == 4:
                args_splited[0] = '{{"sleep":"{}"}},\n'.format(args_splited[0])
                args_splited[1] = '{{"no_copy_rs":"{}"}},\n'.format(args_splited[1])
                args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])
                args_splited[3] = '{{"is_ascii":"{}"}}\n'.format(args_splited[3])

        elif _type == 'reload_vdc' or _type == 'reload_module':
            args_splited[0] = '{{"value":"{}"}}\n'.format(args_splited[0])

        args_splited.insert(0, '{{"command":"{}"}},\n'.format(_type))

        return args_splited

    def _cmds_issu_translate(self, args_):

        '''
        syntax:
            n7k
                #@# cmds=issu:<media>,<kickstart image>,<system image>,<timeout in seconds>,<optional issu options> #@#
            n9k
                #@# cmds=issu:<media>,<system image>,<timeout in seconds>,<optional issu options> #@#

        example:
            #@# cmds=issu:bootflash,n7000-s2-kickstart.8.2.0.SK.0.83.upg.gbin,n7000-s2-dk9.8.2.0.SK.0.83.upg.gbin,900 #@#

            #@# cmds=issu:bootflash,nxos.7.0.3.IHD8.0.430.bin,900 #@#
        '''

        args_splited = args_.split(',')
        ret_list  = []
        ret_list.append('{{"media":"{}"}},\n'.format(args_splited[0]))

        if len(args_splited) == 4:
            ret_list.append('{{"kickstart":"{}"}},\n'.format(args_splited[1]))
            ret_list.append('{{"system":"{}"}},\n'.format(args_splited[2]))
            ret_list.append('{{"sleep":"{}"}},\n'.format(args_splited[3]))
        elif len(args_splited) == 3:

            if not args_splited[-1].isdigit():
                ret_list.append('{{"kickstart":"{}"}},\n'.format(args_splited[1]))
                ret_list.append('{{"system":"{}"}},\n'.format(args_splited[2]))
                ret_list.append('{{"sleep":"{}"}},\n'.format("0"))
            else:
                ret_list.append('{{"nxos":"{}"}},\n'.format(args_splited[1]))
                ret_list.append('{{"sleep":"{}"}},\n'.format(args_splited[2]))

        elif len(args_splited) == 2:
            ret_list.append('{{"system":"{}"}},\n'.format(args_splited[1]))
            ret_list.append('{{"sleep":"{}"}},\n'.format("0"))

        return ret_list

    def _cmds_waitfor_translate(self, args_):

        '''
            example of a legacy input:
                #@# cmds=waitfor:::show vlan,,Up,,9 #@#

            plugin syntax:
                #@# command: {
                "method":"waitfor",
                "options": [
                    {"command": "<cli command>"},
                    {"match": "<regex to match>"},
                    {"fail_on_timeout": "True"},
                    {"timeout": "<max timeout in seconds>"}
                ]}
                #@#
        '''

        args_splited = args_.split(',,')
        args_splited[0] = '{{"command":"{}"}},\n'.format(args_splited[0].replace('\n', '\\n').replace('"', '\\"'))
        args_splited[1] = '{{"match":"{}"}},\n'.format(args_splited[1])
        args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])

        return args_splited

    def _cmds_runraw_translate(self, args_):

        args_splited = args_.split(',,')

        args_splited[0] = '{{"command":"{}"}},\n'.format(args_splited[0].replace('\n', '\\n'))

        args_splited[1] = '{{"patterns":["{}"]}},\n'.format(args_splited[1])
        if len(args_splited) > 2:
            args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])

        return args_splited

    def _cmds_runonmodule_translate(self, args_):

        '''
            syntax-legacy:
                #@# cmds=runonmodule:<module number>,<command>,<timeout> #@#

            syntax-plugin:

                #@# command:{
                "method":"runonmodule",
                "options":[
                    {"module": <module number>},
                    {"command": <command>},
                    {"timeout": <timeout>}
                ]}
                #@#
        '''
        args_splited = args_.split(',')

        args_splited[0] = '{{"module":"{}"}},\n'.format(args_splited[0])
        args_splited[1] = '{{"command":"{}"}},\n'.format(args_splited[1].replace('\n', '\\n'))
        if len(args_splited) == 3:
            args_splited[2] = '{{"timeout":"{}"}},\n'.format(args_splited[2])

        return args_splited
