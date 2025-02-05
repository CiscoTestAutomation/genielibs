'''NXOS Implementation for Interface unconfigconfig triggers'''

# python
from functools import partial

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from genie.libs.sdk.libs.utils.triggeractions import verify_ops_or_logic
# ATS
from pyats.utils.objects import NotExists, Not

interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'accounting']

# Which key to exclude for NVE Ops comparison
nve_exclude = ['maker',]

multisite_exclude = ['elapsedtime','keepalive','remoteport',
                     'keepaliverecvd','keepalivesent','lastread','lastwrite',
                     'msgrecvd','msgsent','neighbortableversion',
                     'tableversion','rtrefreshsent','updatesrecvd','updatessent',
                     'bytessent','bytesrecvd','localport','connsdropped',
                     'connsestablished','opensrecvd','openssent','prefixversion']

# Which key to exclude for Pim Ops comparison
pim_exclude = ['maker', 'bsr_next_bootstrap', 'rp_candidate_next_advertisement',
               'expiration', 'up_time']

# Which key to exclude for Pim Conf comparison
pim_conf_exclude = ['__testbed__', 'devices', 'interfaces', 'parent']

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'accounting']


class TriggerUnconfigConfigVxlanNveOverlayInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned Nve onverlay interface(s)."""

    __description__ = """Unconfigure and reapply the dynamically learned Nve onverlay interface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn VxLan Ops object and verify if has any "up" Nve interface(s),
           otherwise, SKIP the trigger
        2. Unconfigure the learned Nve interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Nve interface(s) from step 2 is removed
        4. Reapply the configuration of Nve interface(s) with checkpoint
        5. Learn VxLan Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<name>.*)', 'if_state', 'up']],
                                        'kwargs': {'attributes': [
                                                      'nve[(.*)][if_state]',
                                                      'nve[(.*)][vni][(.*)][vni]','l2route','bgp_l2vpn_evpn']},
                                        'exclude': nve_exclude + multisite_exclude+ ['tx_id','flags','peer_id','pathnr',
                                                                                     'bestpathnr','advertisedto','prefixversion',
                                                                                     'prefixreceived','mac','prefix','bytesattrs',
                                                                                     'memoryused','totalpaths', 'numberattrs','mac_ip',
                                                                                     'memory','objects','total_mem','total_obj','total_memory',
                                                                                     'totalnetworks']}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                        'requirements':[[NotExists('nve')]], # enh to support or() could be [['nve', NotExists('(?P<name>.*)')]]
                                        'kwargs': {'attributes': [
                                                      'nve[(.*)][if_state]',
                                                      'nve[(.*)][vni][(.*)][vni]','l2route','bgp_l2vpn_evpn']},
                                        'exclude': nve_exclude + ['l2route','bgp_l2vpn_evpn']}},
                      num_values={'name': 1})


class TriggerUnconfigConfigAutoRpInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim auto-rp interface(s) under default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned pim auto-rp interface(s) under default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up"  pim auto-rp
           interface(s) under default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim auto-rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim auto-rp interface(s) from step 2 is removed
        4. Reapply the configuration of pim auto-rp interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.pim.Pim': {
                                        'requirements': [['device_attr', '{uut}', '_vrf_attr',
                                                          '(?P<vrf>^default$)', '_address_family_attr',
                                                          '(?P<af>ipv4)', 'send_rp_announce_intf', r'(?P<rp_intf>(l|L)oopback\d+)']],
                                        'kwargs': {'attributes': ['pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_intf]']},
                                        'exclude': pim_conf_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<rp_intf>.*)')]],
                                       'kwargs': {'attributes': ['info[(.*)][enabled]']},
                                       'exclude': interface_exclude}},
                      num_values={'rp_intf': 1})


class TriggerUnconfigConfigAutoRpVrfInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim auto-rp interface(s) under non-default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned pim
    auto-rp interface(s) under non-default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up"  pim auto-rp
           interface(s) under non-default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim auto-rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim auto-rp interface(s) from step 2 is removed
        4. Reapply the configuration of pim auto-rp interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.pim.Pim': {
                                        'requirements': [['device_attr', '{uut}', '_vrf_attr',
                                                          r'(?P<vrf>^(?!default)\w+$)', '_address_family_attr',
                                                          '(?P<af>ipv4)', 'send_rp_announce_intf', '(?P<rp_intf>.*)']],
                                        'kwargs': {'attributes': ['pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_intf]']},
                                        'exclude': pim_conf_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<rp_intf>.*)')]],
                                       'kwargs': {'attributes': ['info[(.*)][enabled]']},
                                       'exclude': interface_exclude}},
                      num_values={'rp_intf': 1})


class TriggerUnconfigConfigBsrRpInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim bsr-candidate interface(s) under default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned pim bsr-candidate interface(s) under default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up"  pim bsr-candidate
           interface(s) under default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim bsr-candidate interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim bsr-candidate interface(s) from step 2 is removed
        4. Reapply the configuration of pim bsr-candidate interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', '(?P<vrf>^default$)',
                                                          'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                          '(?P<rp_addr>.*)', 'address', '(?P<rp_addr>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<rp_intf>.*)', 'vrf', '(?P<vrf>^default$)'],
                                                         ['info', '(?P<rp_intf>.*)', 'ipv4',
                                                          r'(?P<ip>[\w\.\:]+)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<rp_intf>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<rp_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        NotExists('bsr')],
                                                       ['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        NotExists('bsr_candidate')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerUnconfigConfigBsrRpVrfInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim bsr-candidate interface(s) under non-default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned pim
    bsr-candidate interface(s) under non-default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up"  pim bsr-candidate
           interface(s) under non-default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim bsr-candidate interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim bsr-candidate interface(s) from step 2 is removed
        4. Reapply the configuration of pim bsr-candidate interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                          '(?P<rp_addr>.*)', 'address', '(?P<rp_addr>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<rp_intf>.*)', 'ipv4',
                                                          '(?P<ip>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<rp_intf>.*)', 'vrf', r'(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', '(?P<rp_intf>.*)', 'oper_status', 'up']],
                                        'all_keys': True,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<rp_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        NotExists('bsr')],
                                                       ['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        NotExists('bsr_candidate')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerUnconfigConfigStaticRpInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim static rp interface(s) under default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned pim
    static rp interface(s) under default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up"  pim static rp
           interface(s) under default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim static rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim static rp interface(s) from step 2 is removed
        4. Reapply the configuration of pim static rp interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', '(?P<vrf>^default$)',
                                                          'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                          '(?P<rp_addr>.*)', '(?P<rp_rest>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<rp_intf>.*)', 'ipv4',
                                                          '(?P<rp_addr>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<rp_intf>.*)', 'vrf', '(?P<vrf>^default$)'],
                                                         ['info', '(?P<rp_intf>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<rp_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements': [[partial(verify_ops_or_logic,
                                                            requires=[['info', 'vrf', '(?P<vrf>^default$)',
                                                                       'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                                       NotExists('(?P<rp_addr>.*)')],
                                                                      ['info', 'vrf', '(?P<vrf>^default$)',
                                                                       'address_family','(?P<af>.*)', 'rp', NotExists('static_rp')],
                                                                      ['info', 'vrf', '(?P<vrf>^default$)',
                                                                       'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                                       '(?P<rp_addr>.*)', '(?P<rp_rest>.*)'],
                                                               ])
                                                  ],
                                                ],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerUnconfigConfigStaticRpVrfInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim static rp interface(s) under non-default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned pim
    static rp interface(s) under non-default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up"  pim static rp
           interface(s) under non-default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim static rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim static rp interface(s) from step 2 is removed
        4. Reapply the configuration of pim static rp interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                          '(?P<rp_addr>.*)', '(?P<rp_rest>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<rp_intf>.*)', 'ipv4',
                                                          '(?P<rp_addr>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<rp_intf>.*)', 'vrf', r'(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', '(?P<rp_intf>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<rp_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[[partial(verify_ops_or_logic,
                                                            requires=[['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                                       'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                                       NotExists('(?P<rp_addr>.*)')],
                                                                      ['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                                       'address_family','(?P<af>.*)', 'rp', NotExists('static_rp')],
                                                                      ['info', 'vrf', '(?P<vrf>.*)',
                                                                       'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                                       '(?P<rp_addr>.*)', '(?P<rp_rest>.*)'],
                                                               ])
                                                  ],
                                                ],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerUnconfigConfigPimNbrInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim neighbor interface(s) under default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned  pim neighbor interface(s) under default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up"  pim neighbor
           interface(s) under default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim neighbor interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim neighbor interface(s) from step 2 is removed
        4. Reapply the configuration of pim neighbor interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', '(?P<vrf>^default$)',
                                                          'interfaces','(?P<pim_intf>.*)',
                                                          'address_family', '(?P<af>.*)', 'oper_status', 'up'],
                                                         ['info', 'vrf', '(?P<vrf>^default$)',
                                                          'interfaces','(?P<pim_intf>.*)',
                                                          'address_family', '(?P<af>.*)', 'neighbors', '(?P<address>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<pim_intf>.*)', 'vrf', '(?P<vrf>.*)'],
                                                         ['info', '(?P<pim_intf>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<pim_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<pim_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'interfaces',NotExists('(?P<pim_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude }},
                      num_values={'pim_intf': 1, 'vrf': 1})


class TriggerUnconfigConfigPimNbrVrfInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned pim neighbor interface(s) under non-default vrf."""

    __description__ = """Unconfigure and reapply the dynamically learned
    pim neighbor interface(s) under non-default vrf.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Pim Ops object and verify if has any "up" pim neighbor
           interface(s) under non-default vrf, otherwise, SKIP the trigger
        2. Unconfigure the learned pim neighbor interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim neighbor interface(s) from step 2 is removed
        4. Reapply the configuration of pim neighbor interface(s) with checkpoint
        5. Learn Pim Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'interfaces',r'(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<af>.*)', 'oper_status', 'up'],
                                                         ['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'interfaces',r'(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<af>.*)', 'neighbors', '(?P<address>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', r'(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))', 'vrf', '(?P<vrf>.*)'],
                                                         ['info', r'(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<pim_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<pim_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                        'interfaces', NotExists('(?P<pim_intf>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude }},
                      num_values={'pim_intf': 1, 'vrf': 'all'})
