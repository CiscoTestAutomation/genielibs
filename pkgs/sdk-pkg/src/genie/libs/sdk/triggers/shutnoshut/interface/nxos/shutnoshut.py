'''Implementation for interface shutnoshut triggers'''

# ats
from ats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'accounting']

hsrp_exclude = ['maker', 'active_ip_address', 'standby_ip_address',
                'active_router', 'hello_msec_flag', 'hold_msec_flag',
                'hello_msec', 'hold_msec', 'hello_sec', 'hold_sec',
                'active_ipv6_address', 'standby_ipv6_address']

nve_exclude = ['maker', ]

pim_conf_exclude = ['__testbed__', 'devices', 'interfaces', 'parent']

pim_exclude = ['maker', 'bsr_next_bootstrap', 'rp_candidate_next_advertisement',
               'expiration', 'up_time']


class TriggerShutNoShutVlanInterface(TriggerShutNoShut):

     # Mapping of Information between Ops and Conf
     # Also permit to dictate which key to verify
     mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<name>Vlan[0-9]+)', 'mtu', '(?P<mtu>.*)'],
                                                        ['info', '(?P<name>.*)', 'enabled', True],
                                                        ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                       config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                       verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                        ['info', '(?P<name>.*)', 'oper_status', '(.*down)']],
                                        'exclude': interface_exclude + ['ipv6']}},
                       num_values={'name': 1, 'mtu': 1})


class TriggerShutNoShutHsrpIpv4VlanInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Hsrp Ipv4 Vlan interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Hsrp Ipv4 Vlan interface(s).

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
        1. Learn Interface Ops object and verify if has any "up" "ipv4" Vlan interface(s),
           and learn Hsrp Ops verify if has any "up" "ipv4" Vlan interface(s) that exists
           in learned Vlan interface(s) from Interface Ops. Store the filtered
           "up" "ipv4" Vlan interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned Hsrp Ipv4 Vlan interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Hsrp Ipv4 Vlan interface(s) from step 2 is "down"
        4. Unshut the Hsrp Ipv4 Vlan interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<name>.*)', 'ipv4', '(?P<ipv4>.*)']],
                                        'exclude': interface_exclude + ['ipv6']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'address_family','ipv4','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>Vlan[0-9]+)', 'enabled', False],
                                                       ['info', '(?P<name>Vlan[0-9]+)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv6']}},
                      num_values={'name': 1})


class TriggerShutNoShutHsrpIpv6VlanInterface(TriggerShutNoShut):
    """Shut and Unshut the dynamically learned Hsrp Ipv6 Vlan interface(s)."""
    
    __description__ = """Shut and Unshut the dynamically learned Hsrp Ipv6 Vlan interface(s).

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
        1. Learn Interface Ops object and verify if has any "up" "ipv6" Vlan interface(s),
           and learn Hsrp Ops verify if has any "up" "ipv6" Vlan interface(s) that exists
           in learned Vlan interface(s) from Interface Ops. Store the filtered
           "up" "ipv6" Vlan interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned Hsrp Ipv6 Vlan interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Hsrp Ipv6 Vlan interface(s) from step 2 is "down"
        4. Unshut the Hsrp Ipv6 Vlan interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<name>.*)', 'ipv6', '(?P<ipv6>.*)']],
                                        'exclude': interface_exclude + ['ipv4','status']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'address_family','ipv6','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv4','status']}},
                      num_values={'name': 1})


class TriggerShutNoShutNveOverlayInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Nve onverlay interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Nve onverlay interface(s).

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
        2. Shut the learned Nve interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Nve interface(s) from step 2 is "down"
        4. Unshut the Nve interface(s) with Interface Conf object
        5. Learn VxLan Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<name>.*)', 'if_state', 'up']],
                                        'kwargs': {'attributes': [
                                                      'nve[(.*)][if_state]',
                                                      'nve[(.*)][vni][(.*)][vni]']},
                                        'exclude': nve_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                        'requirements':[['nve', '(?P<name>.*)', 'if_state', 'down']],
                                        'kwargs': {'attributes': [
                                                      'nve[(.*)][if_state]',
                                                      'nve[(.*)][vni][(.*)][vni]']},
                                        'exclude': nve_exclude}},
                      num_values={'name': 1})


class TriggerShutNoShutAutoRpInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim auto-rp interface(s) under default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim auto-rp interface(s) under default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim auto-rp interface(s) under default vrf,
           store pim auto-rp interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim auto-rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim auto-rp interface(s) from step 2 is "down"
        4. Unshut the pim auto-rp interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.pim.Pim': {
                                        'requirements': [['device_attr', '{uut}', '_vrf_attr',
                                                          '(?P<vrf>^default$)', '_address_family_attr',
                                                          '(?P<af>ipv4)', 'send_rp_announce_intf', '(?P<rp_intf>.*)']],
                                        'kwargs': {'attributes': ['pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_intf]']},
                                        'exclude': pim_conf_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<rp_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<rp_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                       'exclude': interface_exclude}},
                      num_values={'rp_intf': 1, 'vrf': 1, 'af': 1})


class TriggerShutNoShutAutoRpVrfInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim auto-rp interface(s) under non-default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim auto-rp interface(s) under non-default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim auto-rp interface(s) under non-default vrf,
           store pim auto-rp interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim auto-rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim auto-rp interface(s) from step 2 is "down"
        4. Unshut the pim auto-rp interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.pim.Pim': {
                                        'requirements': [['device_attr', '{uut}', '_vrf_attr',
                                                          '(?P<vrf>^(?!default)\w+$)', '_address_family_attr',
                                                          '(?P<af>ipv4)', 'send_rp_announce_intf', '(?P<rp_intf>.*)']],
                                        'kwargs': {'attributes': ['pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_intf]']},
                                        'exclude': pim_conf_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<rp_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<rp_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                       'exclude': interface_exclude}},
                      num_values={'rp_intf': 1, 'vrf': 1, 'af': 1})


# TODO: Enhance find to take (.*) after the first level
class TriggerShutNoShutBsrRpInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim bsr-candidate interface(s) under default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim bsr-candidate interface(s) under default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim bsr-candidate interface(s) under default vrf,
           store pim bsr interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim bsr-candidate interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim bsr-candidate interface(s) from step 2 is "down"
        4. Unshut the pim bsr-candidate interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
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
                                                          '(?P<ip>[\w\.\:]+)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<rp_intf>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<rp_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<rp_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        'bsr'],
                                                       ['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        'bsr_candidate']],
                                        'missing': True,
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerShutNoShutBsrRpVrfInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim bsr-candidate interface(s) under non-default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim bsr-candidate interface(s) under non-default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim bsr-candidate interface(s) under non-default vrf,
           store pim bsr-candidate interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim bsr-candidate interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim bsr-candidate interface(s) from step 2 is "down"
        4. Unshut the pim bsr-candidate interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                          'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                          '(?P<rp_addr>.*)', 'address', '(?P<rp_addr>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<rp_intf>.*)', 'ipv4',
                                                          '(?P<ip>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<rp_intf>.*)', 'vrf', '(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', '(?P<rp_intf>.*)', 'oper_status', 'up']],
                                        'all_keys': True,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<rp_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<rp_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        'bsr'],
                                                       ['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'bsr',
                                                        'bsr_candidate']],
                                        'missing': True,
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerShutNoShutStaticRpInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim static-rp interface(s) under default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim static-rp interface(s) under default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim static-rp interface(s) under default vrf,
           store pim static-rp interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim static-rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim static-rp interface(s) from step 2 is "down"
        4. Unshut the pim static-rp interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
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
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<rp_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<rp_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                        '(?P<static_rp>.*)']],
                                        'missing': True,
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerShutNoShutStaticRpVrfInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim static-rp interface(s) under non-default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim static-rp interface(s) under non-default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim static-rp interface(s) under non-default vrf,
           store pim static-rp interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim static-rp interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim static-rp interface(s) from step 2 is "down"
        4. Unshut the pim static-rp interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                          'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                          '(?P<rp_addr>.*)', '(?P<rp_rest>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<rp_intf>.*)', 'ipv4',
                                                          '(?P<rp_addr>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<rp_intf>.*)', 'vrf', '(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', '(?P<rp_intf>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<rp_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<rp_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<rp_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<af>.*)', 'rp', 'static_rp',
                                                        '(?P<static_rp>.*)']],
                                        'missing': True,
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'rp_intf': 1, 'vrf': 'all', 'rp_addr': 'all', 'af': 'all'})


class TriggerShutNoShutPimNbrInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim neighbor interface(s) under default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim neighbor interface(s) under default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim neighbor interface(s) under default vrf,
           store pim neighbor interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim neighbor interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim neighbor interface(s) from step 2 is "down"
        4. Unshut the pim neighbor interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', '(?P<vrf>^default$)',
                                                          'interfaces','(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<af>.*)', 'oper_status', 'up'],
                                                         ['info', 'vrf', '(?P<vrf>^default$)',
                                                          'interfaces','(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<af>.*)', 'neighbors', '(?P<address>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'vrf', '(?P<vrf>^default$)'],
                                                         ['info', '(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<pim_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<pim_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<pim_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'interfaces','(?P<pim_intf>.*)', 'address_family',
                                                        '(?P<af>.*)', 'oper_status'],
                                                       ['info', 'vrf', '(?P<vrf>^default$)',
                                                        'interfaces','(?P<pim_intf>.*)', 'address_family',
                                                        '(?P<af>.*)', 'neighbors', '(?P<address>.*)']],
                                        'missing': True,
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude }},
                      num_values={'pim_intf': 1, 'vrf': 'all'})


class TriggerShutNoShutPimNbrVrfInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned pim neighbor interface(s) under non-default vrf."""

    __description__ = """Shut and unshut the dynamically learned  pim neighbor interface(s) under non-default vrf.

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
        1. Learn PIM Ops object and verify if has any "up" pim neighbor interface(s) under non-default vrf,
           store pim neighbor interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned pim neighbor interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned pim neighbor interface(s) from step 2 is "down"
        4. Unshut the pim neighbor interface(s) with Interface Conf object
        5. Learn PIM Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.pim.pim.Pim': {
                                        'requirements': [['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                          'interfaces','(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<af>.*)', 'oper_status', 'up'],
                                                         ['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                          'interfaces','(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<af>.*)', 'neighbors', '(?P<address>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'vrf', '(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', '(?P<pim_intf>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<pim_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<pim_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<pim_intf>.*)', 'oper_status', 'down']],
                                        'missing': False,
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                        'interfaces','(?P<pim_intf>.*)', 'address_family',
                                                        '(?P<af>.*)', 'oper_status'],
                                                       ['info', 'vrf', '(?P<vrf>^(?!default)\w+$)',
                                                        'interfaces','(?P<pim_intf>.*)', 'address_family',
                                                        '(?P<af>.*)', 'neighbors', '(?P<address>.*)']],
                                        'missing': True,
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude }},
                      num_values={'pim_intf': 1, 'vrf': 'all'})

class TriggerShutNoShutPortChannelInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Port Channel interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Port Channel interface(s).

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
        1. Learn Interface Ops object and store the "up" Port Channel interface(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned Port Channel interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Port Channel interface(s) from step 2 is "down"
        4. Unshut the Port Channel interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<name>Ethernet(\S+))', 'oper_status', 'up'],
                                            ['info', '(?P<name>.*)', 'enabled', True]],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<name>.*)', 'enabled', False],
                                            ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                            ['info', '(.*)', 'enabled', False]],
                                        'exclude': interface_exclude}},
                      num_values={'name': 1})
