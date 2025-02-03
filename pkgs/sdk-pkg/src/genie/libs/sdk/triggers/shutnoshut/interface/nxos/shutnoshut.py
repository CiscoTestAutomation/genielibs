'''Implementation for interface shutnoshut triggers'''

# ats
from pyats.utils.objects import Not, NotExists

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
    """Shut and unshut the dynamically learned Vlan interface(s)"""

    __description__ = """Shut and unshut the dynamically learned Vlan interface(s).

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
             static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`
                mtu: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

     steps:
         1. Learn Interface Ops object and verify if has any "up" Vlan interface(s),
            if has any, otherwise, SKIP the trigger
         2. Shut the learned Vlan interface(s) from step 1 with Interface Conf object
         3. Verify the state of learned Vlan interface(s) from step 2 is "down"
         4. Unshut the Vlan interface(s) with Interface Conf object
         5. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>Vlan[0-9]+)', 'mtu', '(?P<mtu>.*)'],
                                                        ['info', '(?P<interface>.*)', 'enabled', True],
                                                        ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'all_keys': True,
                                        'exclude': interface_exclude}},
                       config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                       verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                        ['info', '(?P<interface>.*)', 'oper_status', '(.*down)']],
                                        'exclude': interface_exclude + ['ipv6']}},
                       num_values={'interface': 1, 'mtu': 1})


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
            static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<interface>.*)', 'ipv4', '(?P<ipv4>.*)']],
                                        'exclude': interface_exclude + ['ipv6']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'address_family','ipv4','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>Vlan[0-9]+)', 'enabled', False],
                                                       ['info', '(?P<interface>Vlan[0-9]+)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv6']}},
                      num_values={'interface': 1})


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
            static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<interface>.*)', 'ipv6', '(?P<ipv6>.*)']],
                                        'exclude': interface_exclude + ['ipv4','status']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'address_family','ipv6','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv4','status']}},
                      num_values={'interface': 1})

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
            static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                                          '(?P<address_family>ipv4)', 'send_rp_announce_intf', '(?P<interface>.*)']],
                                        'kwargs': {'attributes': ['pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_intf]']},
                                        'exclude': pim_conf_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                       'exclude': interface_exclude}},
                      num_values={'interface': 1, 'vrf': 1, 'address_family': 1})


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
            static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               send_rp_announce_intf: `str`
               vrf: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                                          r'(?P<vrf>^(?!default)\w+$)', '_address_family_attr',
                                                          '(?P<address_family>ipv4)', 'send_rp_announce_intf', '(?P<send_rp_announce_intf>.*)']],
                                        'kwargs': {'attributes': ['pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_intf]']},
                                        'exclude': pim_conf_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<send_rp_announce_intf>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<send_rp_announce_intf>.*)', 'enabled', False],
                                                       ['info', '(?P<send_rp_announce_intf>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                       'exclude': interface_exclude}},
                      num_values={'send_rp_announce_intf': 1, 'vrf': 1, 'address_family': 1})


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
            static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               vrf: `str`
               address_family: `str`
               rp_addr: `str`
               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)

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
                                                          'address_family','(?P<address_family>.*)', 'rp', 'bsr',
                                                          '(?P<rp_addr>.*)', 'address', '(?P<rp_addr>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<interface>.*)', 'vrf', '(?P<vrf>^default$)'],
                                                         ['info', '(?P<interface>.*)', 'ipv4',
                                                          r'(?P<ip>[\w\.\:]+)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]',]},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<address_family>.*)', 'rp', 'bsr',
                                                        NotExists('bsr')],
                                                       ['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<address_family>.*)', 'rp', 'bsr',
                                                        NotExists('bsr_candidate')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'interface': 1, 'vrf': 'all', 'rp_addr': 'all', 'address_family': 'all'})


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
         static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               vrf: `str`
               address_family: `str`
               rp_addr: `str`
               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)

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
                                        'requirements': [['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'address_family','(?P<address_family>.*)', 'rp', 'bsr',
                                                          '(?P<rp_addr>.*)', 'address', '(?P<rp_addr>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<interface>.*)', 'ipv4',
                                                          '(?P<ip>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<interface>.*)', 'vrf', r'(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', '(?P<interface>.*)', 'oper_status', 'up']],
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
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<address_family>.*)', 'rp', 'bsr',
                                                        NotExists('bsr')],
                                                       ['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<address_family>.*)', 'rp', 'bsr',
                                                        NotExists('bsr_candidate')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][bsr][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'interface': 1, 'vrf': 'all', 'rp_addr': 'all', 'address_family': 'all'})


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
        static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               vrf: `str`
               address_family: `str`
               rp_addr: `str`
               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                                          'address_family','(?P<address_family>.*)', 'rp', 'static_rp',
                                                          '(?P<rp_addr>.*)', '(?P<rp_rest>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<interface>.*)', 'ipv4',
                                                          '(?P<rp_addr>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<interface>.*)', 'vrf', '(?P<vrf>^default$)'],
                                                         ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'address_family','(?P<address_family>.*)', 'rp', 'static_rp',
                                                        NotExists('(?P<static_rp>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'interface': 1, 'vrf': 'all', 'rp_addr': 'all', 'address_family': 'all'})


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
        static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               vrf: `str`
               address_family: `str`
               rp_addr: `str`
               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                        'requirements': [['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'address_family','(?P<address_family>.*)', 'rp', 'static_rp',
                                                          '(?P<rp_addr>.*)', '(?P<rp_rest>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<interface>.*)', 'ipv4',
                                                          '(?P<rp_addr>.*)','ip', '(?P<rp_addr>.*)'],
                                                         ['info', '(?P<interface>.*)', 'vrf', r'(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][(ipv4|ipv6)][(.*)][ip]',
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                        'address_family','(?P<address_family>.*)', 'rp', 'static_rp',
                                                        NotExists('(?P<static_rp>.*)')]],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][address_family][(.*)][rp][static_rp][(.*)]']},
                                        'exclude': pim_exclude }},
                      num_values={'interface': 1, 'vrf': 'all', 'rp_addr': 'all', 'address_family': 'all'})


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
        static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               vrf: `str`
               address_family: `str`
               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                                          'interfaces',r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<address_family>.*)', 'oper_status', 'up'],
                                                         ['info', 'vrf', '(?P<vrf>^default$)',
                                                          'interfaces',r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<address_family>.*)', 'neighbors', '(?P<address>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'vrf', '(?P<vrf>^default$)'],
                                                         ['info', r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements':[['info', 'vrf', '(?P<vrf>^default$)',
                                                        'interfaces', '(?P<interface>.*)', 'address_family',
                                                        '(?P<address_family>.*)', NotExists('neighbors')],
                                                       ['info', 'vrf', '(?P<vrf>^default$)',
                                                        'interfaces', '(?P<interface>.*)', 'address_family',
                                                        '(?P<address_family>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][default][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude }},
                      num_values={'interface': 1, 'vrf': 'all'})


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
        static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               vrf: `str`
               address_family: `str`
               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
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
                                        'requirements': [['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'interfaces',r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<address_family>.*)', 'oper_status', 'up'],
                                                         ['info', 'vrf', r'(?P<vrf>^(?!default)\w+$)',
                                                          'interfaces',r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'address_family', '(?P<address_family>.*)', 'neighbors', '(?P<address>.*)']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude },
                                  'ops.interface.interface.Interface': {
                                        'requirements': [['info', r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'vrf', r'(?P<vrf>^(?!default)\w+$)'],
                                                         ['info', r'(?P<interface>(Ethernet\d+\/\d+\.\d+)|(Loopback\d+))',
                                                          'oper_status', 'up']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[(.*)][vrf]',
                                                      'info[(.*)][enabled]',
                                                      'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude},
                                  'ops.pim.pim.Pim':{
                                       'requirements': [['info', 'vrf', '(?P<vrf>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'address_family',
                                                        '(?P<address_family>.*)', NotExists('neighbors')],
                                                       ['info', 'vrf', '(?P<vrf>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'address_family',
                                                        '(?P<address_family>.*)', 'oper_status', 'down']],
                                        'kwargs': {'attributes': [
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                                      'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbors]']},
                                        'exclude': pim_exclude }},
                      num_values={'interface': 1, 'vrf': 'all'})

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
         static:
               The keys below are dynamically learnt by default.
               However, they can also be set to a custom value when provided in the trigger datafile.

               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)

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
                                            ['info', r'(?P<interface>([p|P]ort-channel)(\S+))', 'oper_status', 'up'],
                                            ['info', '(?P<interface>.*)', 'enabled', True]],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<interface>.*)', 'enabled', False],
                                            ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                            ['info', '(.*)', 'enabled', False]],
                                        'exclude': interface_exclude}},
                      num_values={'interface': 1})
