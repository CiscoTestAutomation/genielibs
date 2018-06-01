'''IOSXE Implementation for Lag addremove triggers'''

# python
from functools import partial

# import genie.libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove
from genie.libs.sdk.libs.abstracted_libs.processors import ping_devices, debug_dumper
from genie.libs.sdk.libs.abstracted_libs.iosxe.processors import check_interface_counters

# ATS
from ats import aetest
from ats.utils.objects import NotExists, Not

# Which key to exclude for ACL Ops comparison
lag_exclude = ['maker', 'counters', 'system_priority']

interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'in_errors', '(Tunnel.*)', 'status']


class TriggerAddRemoveTrunkEtherchannelLacp(TriggerAddRemove):
    """Apply the Etherchannel in LACP mode, and remove the
    added Etherchannel in LACP mode
    """

    __description__ = """Apply the Etherchannel in LACP mode, and remove the
    added Etherchannel in LACP mode.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Interface Ops object to select trunk interfaces.
           Learn LAG ops object to find port-channle interfaces which does not have
           the learned interfaces as memebers.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of Etherchannel in LACP mode with interface Conf object
        4. Verify the interfaces are in the por-channle interfaces from step 3 has configured
        5. Remove the Etherchannel configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn LAG Ops again and verify it is the same as the Ops in step 1

    """
    # The added new values
    BUNDLE_ID = 10
    BUNDLE_ID_INTF = 'Port-channel' + str(BUNDLE_ID)

    # debug_dumper commands
    # Will be moved to trigger yaml file when feature is ready
    pre_commands = {'uut': {'pass': ["show int trunk",
                                "show ip int br | inc up",
                                "sh plat soft fed sw 1 etherchannel {} group-mask".format(BUNDLE_ID),
                                "sh plat soft fed sw 1 port summary",
                                "sh plat soft fed sw 2 etherchannel {} group-mask".format(BUNDLE_ID),
                                "sh plat soft fed sw 2 port summary",
                                "sh plat soft fed sw 3 etherchannel {} group-mask".format(BUNDLE_ID),
                                "sh plat soft fed sw 3 port summary"]}}

    post_commands = {'uut': {'fail': ["sh arp",
                                      "show run",
                                      "show cdp nei",
                                      "show ip inter brief | inc up",
                                      "sh int trunk",
                                      "sh interface counter error",
                                      "sh interface counter etherchannel",
                                      "show plat software fed switch 1 port summary",
                                      "Show plat software vp switch 1 r0 summary",
                                      "show plat software vp switch 2 r0 summary",
                                      "show plat software matm f0 table 1 content",
                                      "show plat software fed sw active punt cpuq 2",
                                      "show plat software fed sw active punt cpuq 0",
                                      "show log | red flash:/tracelogs/lacp_stack_ping_check.log",
                                      "show switch",
                                      "sh int {}".format(BUNDLE_ID_INTF),
                                      "show etherchannel detail",
                                      "sh plat soft fed sw 1 etherchannel {} group-mask".format(BUNDLE_ID),
                                      "sh plat soft fed sw 2 etherchannel {} group-mask".format(BUNDLE_ID),
                                      "sh plat soft fed sw 3 etherchannel {} group-mask".format(BUNDLE_ID)]},
                 'helper': {'fail': ["show run",
                                "show arp",
                                "show cdp nei",
                                "sh int trunk",
                                "show log | red flash:lacp_stack_ping_check.log",
                                "sh int {}".format(BUNDLE_ID_INTF),
                                "sh ip int br | inc up",
                                "show int trunk",
                                "show etherchannel detail"]}}

    # ping info
    # Will be moved to trigger yaml file when feature is ready
    pre_ping_info = [{'src': 'uut',
                        'dest': 'helper',
                        'ping': {
                           'proto': 'ip',
                           'count': 20,
                           'size': 64,
                           'extd_ping': 'n',
                           'ping_packet_timeout': 2
                        },
                        'timeout_interval': 5,
                        'timeout_max_time': 60,
                        'exp_succ_perc': 100,
                        'peer_num': 1},
                        {'src': 'helper',
                        'dest': 'uut',
                        'ping': {
                           'proto': 'ip',
                           'count': 100,
                           'size': 64,
                           'extd_ping': 'n',
                           'ping_packet_timeout': 2
                        },
                        'timeout_interval': 5,
                        'timeout_max_time': 60,
                        'exp_succ_perc': 100,
                        'peer_num': 1}]

    @aetest.processors(pre=[partial(debug_dumper, commands=pre_commands),
                            partial(ping_devices, ping_parameters=pre_ping_info),
                            partial(debug_dumper, commands=post_commands)],
                       post=[partial(check_interface_counters, ports=[BUNDLE_ID_INTF],
                                        keys = [['interface', BUNDLE_ID_INTF, 'out', 'ucast_pkts', '(.*)']],
                                        threshold='islargerthan(100)')])
    @aetest.test
    def verify_configuration(self, uut, abstract, steps):        
        super().verify_configuration(uut, abstract, steps)

    mapping = Mapping(requirements={'ops.lag.lag.Lag':{
                                            'requirements': [['info', 'interfaces', NotExists({BUNDLE_ID_INTF})], 
                                                             [NotExists('info')]],
                                            'all_keys': True,
                                            'kwargs':{'attributes':['info[interfaces][(.*)]']},
                                            'exclude': lag_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements':[['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                             'switchport_mode', 'trunk'],
                                                            ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                             'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                      'info[(.*)][enabled]',
                                                                      'info[(.*)][oper_status]',
                                                                      'info[(.*)][port_channel]']},
                                            'exclude': interface_exclude}},
                       config_info={'conf.interface.Interface':{
                                        'requirements':[['lag_bundle_id', BUNDLE_ID],
                                                        ['lag_activity', 'active']],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<intf>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.lag.lag.Lag':{
                                      'requirements': [\
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'bundle_id', BUNDLE_ID],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'protocol', 'lacp'],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'oper_status', 'up'],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'name', 'Port-channel10'],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'members', '(?P<intf>.*)', 'bundled', True]],
                                      'kwargs':{'attributes':['info[interfaces][(.*)]']},
                                      'exclude': lag_exclude},
                                  'ops.interface.interface.Interface':{
                                          'requirements':[['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'switchport_mode', 'trunk'],
                                                          ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'oper_status', 'up'],
                                                          ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'port_channel', 'port_channel_member', True],
                                                          ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'port_channel', 'port_channel_int', BUNDLE_ID_INTF],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'oper_status', 'up'],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'enabled', True],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'oper_status', 'up'],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'port_channel', 'port_channel_member', True],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'port_channel', 'port_channel_member_intfs', '(.*)'],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'switchport_enable', True],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'switchport_mode', 'trunk'],],
                                          'kwargs': {'attributes': ['info']},
                                          'exclude': interface_exclude}},
                      num_values={'intf':'all', 'bundle_id': 1})


class TriggerAddRemoveAccessEtherchannelPagp(TriggerAddRemove):
    """Apply the Etherchannel in PAGP mode, and remove the
    added Etherchannel in PAGP mode
    """

    __description__ = """Apply the Etherchannel in PAGP mode, and remove the
    added Etherchannel in PAGP mode.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Interface Ops object to select trunk interfaces.
           Learn LAG ops object to find port-channle interfaces which does not have
           the learned interfaces as memebers.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of Etherchannel in PAGP mode with interface Conf object
        4. Verify the interfaces are in the por-channle interfaces from step 3 has configured
        5. Remove the Etherchannel configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn LAG Ops again and verify it is the same as the Ops in step 1

    """
    BUNDLE_ID = 10
    BUNDLE_ID_INTF = 'Port-channel' + str(BUNDLE_ID)

    mapping = Mapping(requirements={'ops.lag.lag.Lag':{
                                            'requirements':[\
                                                ['info', 'interfaces', NotExists(BUNDLE_ID_INTF)],
                                                [NotExists('info')]],
                                            'all_keys': True,
                                            'kwargs':{'attributes':['info[interfaces][(.*)]']},
                                            'exclude': lag_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements':[['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                             'switchport_mode', 'static access'],
                                                            ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                             'oper_status', 'up']],
                                          'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                    'info[(.*)][enabled]',
                                                                    'info[(.*)][oper_status]',
                                                                    'info[(.*)][port_channel]']},
                                            'exclude': interface_exclude}},
                       config_info={'conf.interface.Interface':{
                                        'requirements':[['lag_bundle_id', BUNDLE_ID],
                                                        ['lag_activity', 'desirable']],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<intf>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.lag.lag.Lag':{
                                      'requirements': [\
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'bundle_id', BUNDLE_ID],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'protocol', 'pagp'],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'oper_status', 'up'],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'name', 'Port-channel10'],
                                                ['info', 'interfaces', BUNDLE_ID_INTF,
                                                 'members', '(?P<intf>.*)', 'bundled', True]],
                                      'kwargs':{'attributes':['info[interfaces][(.*)]']},
                                      'exclude': lag_exclude},
                                  'ops.interface.interface.Interface':{
                                          'requirements':[['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'switchport_mode', 'static access'],
                                                          ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'oper_status', 'up'],
                                                          ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'port_channel', 'port_channel_member', True],
                                                          ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'port_channel', 'port_channel_int', BUNDLE_ID_INTF],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'oper_status', 'up'],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'enabled', True],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'port_channel', 'port_channel_member', True],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'port_channel', 'port_channel_member_intfs', '(.*)'],
                                                          ['info', BUNDLE_ID_INTF,
                                                           'switchport_mode', 'static access']],
                                          'kwargs': {'attributes': ['info']},
                                          'exclude': interface_exclude}},
                      num_values={'intf':'all', 'bundle_id': 1})


class TriggerAddRemoveL3EtherchannelPagp(TriggerAddRemove):
    """Apply the configuration for L3 Etherchannel in PAGP mode, and remove the
    added Etherchannel in PAGP mode
    """

    __description__ = """Apply the configuration for L3 Etherchannel in PAGP mode, and remove the
    added Etherchannel in PAGP mode.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Interface Ops object to select up interfaces.
           Learn LAG ops object to find port-channle interfaces which does not exists.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of Etherchannel in PAGP mode with interface Conf object,
           Add ip address configuration to the learned port-channel interfaces
        4. Verify the interfaces are in the por-channle interfaces from step 3 has configured
        5. Remove the Etherchannel and port-channel configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn LAG Ops again and verify it is the same as the Ops in step 1

    """
    counters_port = []
    counters_keys = [['interface', '(?P<bundle_intf>.*)', 'out', 'ucast_pkts', '(.*)']]

    # ping info
    pre_ping_info = [{'src': 'uut',
                        'dest': 'helper',
                        'ping': {
                           'proto': 'ip',
                           'count': 20,
                           'size': 64,
                           'extd_ping': 'n',
                           'ping_packet_timeout': 2
                        },
                        'timeout_interval': 5,
                        'timeout_max_time': 60,
                        'exp_succ_perc': 100,
                        'peer_num': 1},
                        {'src': 'helper',
                        'dest': 'uut',
                        'ping': {
                           'proto': 'ip',
                           'count': 100,
                           'size': 64,
                           'extd_ping': 'n',
                           'ping_packet_timeout': 2
                        },
                        'timeout_interval': 5,
                        'timeout_max_time': 60,
                        'exp_succ_perc': 100,
                        'peer_num': 1}]

    @aetest.processors(pre=[partial(ping_devices, ping_parameters=pre_ping_info)],
                       post=[partial(check_interface_counters, ports=counters_port,
                                        keys =counters_keys, threshold='islargerthan(100)')])
    @aetest.test
    def verify_configuration(self, uut, abstract, steps):
        super().verify_configuration(uut, abstract, steps)


    mapping = Mapping(requirements={'ops.lag.lag.Lag':{
                                            'requirements':[\
                                                ['info', 'interfaces', '(?P<bundle_intf>.*)', NotExists('members')],
                                                ['info', 'interfaces', '(?P<bundle_intf>.*)', 'bundle_id', '(?P<bundle_id>.*)']],
                                            'all_keys': True,
                                            'kwargs':{'attributes':['info[interfaces][(.*)]']},
                                            'exclude': lag_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements':[['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                             'switchport_enable', False],
                                                            ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                             'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info[(.*)][switchport_enable]',
                                                                      'info[(.*)][operational_mode]',
                                                                      'info[(.*)][oper_status]',
                                                                      'info[(.*)][enabled]',
                                                                      'info[(.*)][port_channel]']},
                                            'exclude': interface_exclude}},
                       config_info={'conf.interface.Interface':{
                                        'requirements':[['lag_bundle_id', '(?P<bundle_id>.*)'],
                                                        ['lag_activity', 'desirable']],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<intf>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.lag.lag.Lag':{
                                      'requirements': [\
                                                ['info', 'interfaces', '(?P<bundle_intf>.*)',
                                                 'bundle_id', '(?P<bundle_id>.*)'],
                                                ['info', 'interfaces', '(?P<bundle_intf>.*)',
                                                 'protocol', 'pagp'],
                                                ['info', 'interfaces', '(?P<bundle_intf>.*)',
                                                 'oper_status', 'up'],
                                                ['info', 'interfaces', '(?P<bundle_intf>.*)',
                                                 'name', '(?P<bundle_intf>.*)'],
                                                ['info', 'interfaces', '(?P<bundle_intf>.*)',
                                                 'members', '(?P<intf>.*)', 'bundled', True]],
                                      'kwargs':{'attributes':['info[interfaces][(.*)]']},
                                      'exclude': lag_exclude + ['attribute']},
                                  'ops.interface.interface.Interface':{
                                          'requirements':[['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'switchport_enable', False],
                                                          ['info', '(?P<intf>\w+Ethernet[\d\/]+$)',
                                                           'oper_status', 'up'],
                                                          ['info', '(?P<bundle_intf>.*)',
                                                           'oper_status', 'up'],
                                                          ['info', '(?P<bundle_intf>.*)',
                                                           'enabled', True],
                                                          ['info', '(?P<bundle_intf>.*)',
                                                           'oper_status', 'up'],
                                                          ['info', '(?P<bundle_intf>.*)',
                                                           'port_channel', 'port_channel_member', True],
                                                          ['info', '(?P<bundle_intf>.*)',
                                                           'port_channel', 'port_channel_member_intfs', '(.*)']],
                                            'kwargs': {'attributes': ['info[(.*)][switchport_enable]',
                                                                      'info[(.*)][operational_mode]',
                                                                      'info[(.*)][oper_status]',
                                                                      'info[(.*)][enabled]',
                                                                      'info[(.*)][port_channel]']},
                                          'exclude': interface_exclude}},
                      num_values={'intf':'all', 'bundle_id': 1})