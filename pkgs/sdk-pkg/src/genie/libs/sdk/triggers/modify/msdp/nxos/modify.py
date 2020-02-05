'''NXOS Implementation for Msdp modify triggers'''

# python
from copy import deepcopy 

# pyats
from pyats import aetest

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# pyats
from pyats.utils.objects import Not, NotExists

# Which key to exclude for Msdp Ops comparison
msdp_exclude = ['maker', 'elapsed_time', 'discontinuity_time',
           'keepalive', 'total', 'up_time', 'expire', 'remote',
           'last_message_received', 'num_of_comparison', 'rpf_failure',
           'total_accept_count', 'total_reject_count', 'notification']

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'bandwidth', 'load_interval',
                     'port_speed', 'in_crc_errors', 'in_discards',
                     'unnumbered', '(Tunnel.*)', 'accounting']


class TriggerModifyMsdpOriginatorId(TriggerModify):
    """Modify dynamically learned MSDP peer(s) originator-id then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) originator-id then restore the
      configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                originator_id: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP originator-id
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned MSDP originator-id from step 1 
           with Msdp Conf object
        4. Verify the MSDP originator-id from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'global',
                                               'originator_id', '(?P<originator_id>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][global][originator_id]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                          'exclude': msdp_exclude},
                                    'ops.interface.interface.Interface':{
                                          'requirements':[\
                                              ['info', '(?P<modify_originator_id>.*)', 'ipv4',
                                               '(?P<ipv4>.*)', 'ip', '(?P<diff_originator_ip>.*)'],
                                              ['info', '(?P<modify_originator_id>.*)', 'vrf',
                                               '(?P<vrf>.*)'],
                                              ['info', '(?P<modify_originator_id>.*)', 'oper_status',
                                               'up']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[(.*)][ipv4][(.*)][ip]',
                                              'info[(.*)][vrf]',
                                              'info[(.*)][oper_status]']},
                                          'exclude': interface_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'originating_rp', '(?P<modify_originator_id>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'global',
                                               'originator_id', '(?P<diff_originator_ip>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][global][originator_id]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                          'exclude': msdp_exclude},
                                  'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<modify_originator_id>.*)', 'oper_status',
                                             'up']],
                                        'all_keys': True,
                                        'kwargs':{'attributes': [
                                            'info[(.*)][ipv4][(.*)][ip]',
                                            'info[(.*)][vrf]',
                                            'info[(.*)][oper_status]']},
                                        'exclude': interface_exclude}},
                      num_values={'vrf': 1, 'peer': 1, 'modify_originator_id': 1})


class TriggerModifyMsdpSaFilterIn(TriggerModify):
    """Modify dynamically learned MSDP peer(s) sa-filter in then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) sa-filter in then restore the
      configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                sa_filter_in: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the "established" MSDP peer(s) sa-filter in
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. MOdify the learned MSDP peer(s) sa-filter in from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) sa-filter in from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    MODIFY_NAME = 'modified_sa_filter_in'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                               'sa_filter', 'in', '(?P<sa_filter_in>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'sa_filter_in',MODIFY_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                       'sa_filter', 'in', MODIFY_NAME]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerModifyMsdpSaFilterOut(TriggerModify):
    """Modify dynamically learned MSDP peer(s) sa-filter out then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) sa-filter out then restore the
      configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                sa_filter_out: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Msdp Ops object and store the "established" MSDP peer(s) sa-filter out
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. MOdify the learned MSDP peer(s) sa-filter in from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) sa-filter out from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    MODIFY_NAME = 'modified_sa_filter_out'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                               'sa_filter', 'out', '(?P<sa_filter_out>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'sa_filter_out', MODIFY_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                       'sa_filter', 'out', MODIFY_NAME]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerModifyMsdpSaLimit(TriggerModify):
    """Modify dynamically learned MSDP peer(s) sa-limit then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) sa-limit then restore the
      configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                sa_limit: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Msdp Ops object and store the "established" MSDP peer(s) sa-limit
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned MSDP peer(s) sa-limit from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) sa-limit from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    MODIFY_NAME = 12345
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'sa_limit', '(?P<sa_limit>\d+)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_limit]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'sa_limit', MODIFY_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'sa_limit', str(MODIFY_NAME)]],
                                    'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_limit]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerModifyMsdpMeshGroup(TriggerModify):
    """Modify dynamically learned MSDP peer(s) mesh-group then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) mesh-group then restore the
      configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                mesh_group: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Msdp Ops object and store the 'established' MSDP peer(s) mesh group
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned MSDP peer(s) mesh group from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) mesh group from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    MODIFY_NAME = 'modified_mesh_group'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'mesh_group', '(?P<mesh_group>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][mesh_group]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'mesh_group', MODIFY_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'mesh_group', MODIFY_NAME]],
                                    'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][mesh_group]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerModifyMsdpKeepaliveHoldtime(TriggerModify):
    """Modify dynamically learned MSDP peer(s) keepalive&holdtime interval
      then restore the configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) keepalive&holdtime interval
      then restore the configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                keepalive_interval: `int`
                holdtime_interval: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the 'established' MSDP peer(s)
           keepalive&holdtime interval if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned MSDP peer(s) keepalive&holdtime interval from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) keepalive&holdtime interval from step 3
           is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # <1-60>  Keepalive interval in seconds
    keepalive_interval = 33
    # <1-90>  Keepalive timeout in seconds
    holdtime_interval = 66

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                               'timer', 'keepalive_interval', '(?P<keepalive_interval>.*)'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                               'timer', 'holdtime_interval', '(?P<holdtime_interval>.*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][timer]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'peer_attr',
                                          '(?P<peer>.*)', 'keepalive_interval', keepalive_interval],
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'peer_attr',
                                          '(?P<peer>.*)', 'holdtime_interval', holdtime_interval]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                          ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                           'timer', 'keepalive_interval', keepalive_interval],
                                          ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                           'timer', 'holdtime_interval', holdtime_interval]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][timer]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerModifyMsdpReconnectInterval(TriggerModify):
    """Modify dynamically learned MSDP peer(s) reconnect interval
      then restore the configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) reconnect interval
      then restore the configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                connect_retry_interval: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP reconnect interval
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. MOdify the learned MSDP reconnect interval from step 1 
           with Msdp Conf object
        4. Verify the MSDP reconnect interval from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # <1-60>  Interval in seconds
    connect_retry_interval = 33
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 'timer',
                                               'connect_retry_interval', '(?P<connect_retry_interval>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][timer]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'global_connect_retry_interval', connect_retry_interval]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 'timer',
                                       'connect_retry_interval', connect_retry_interval]], 
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][timer]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 'all'})


class TriggerModifyMsdpDescription(TriggerModify):
    """Modify dynamically learned MSDP peer(s) description
      then restore the configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP peer(s) description
      then restore the configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                description: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP peer(s) description
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned MSDP peer(s) description from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) description from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    MODIFY_NAME = 'Modified Description'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'description', '(?P<description>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][description]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'description', MODIFY_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'description', MODIFY_NAME]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][description]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerModifyMsdpPeerConnectedSource(TriggerModify):
    """Modify dynamically learned MSDP 'established' peer(s) connect-source 
      then restore the configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP 'established' peer(s) connect-source 
      then restore the configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                connect_source: `str`
                modify_connect_source: `str`
                ip: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP 'established' peer(s) connect-source 
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned MSDP peer(s) connect-source from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) connect-source  from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    @aetest.test
    def modify_configuration(self, uut, abstract, steps):
        # shut no-shut msdp to make the change get effected
        original_conf = deepcopy(self.mapping.config_info['conf.msdp.Msdp']['requirements'])

        # shutdown the peer first        
        self.mapping.config_info['conf.msdp.Msdp']['requirements'] = \
          [['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'peer_attr', '(?P<peer>.*)', 'enable', False]]
        super().modify_configuration(uut, abstract, steps)

        # modify connected-source
        self.mapping.config_info['conf.msdp.Msdp']['requirements'] = deepcopy(original_conf)
        super().modify_configuration(uut, abstract, steps)

        # unshut the peer
        self.mapping.config_info['conf.msdp.Msdp']['requirements'] = \
          [['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'peer_attr', '(?P<peer>.*)', 'enable', True]]
        super().modify_configuration(uut, abstract, steps)

        # revert the requirements
        self.mapping.config_info['conf.msdp.Msdp']['requirements'] = original_conf

    @aetest.test
    def restore_configuration(self, uut, method, abstract, steps):
        # before rollback, need to shutdown the modified peer to
        # let the rollback successfull  
        self.mapping.config_info['conf.msdp.Msdp']['requirements'] = \
          [['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'peer_attr', '(?P<peer>.*)', 'enable', False]]
        super().modify_configuration(uut, abstract, steps)

        # retore the router
        super().restore_configuration(uut, method, abstract)


    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'connect_source', '(?P<connect_source>.*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)]']},
                                          'exclude': msdp_exclude},
                                    'ops.interface.interface.Interface':{
                                          'requirements':[\
                                              ['info', '(?P<modify_connect_source>.*)', 'ipv4',
                                               '(?P<ipv4>.*)', 'ip', '(?P<ip>.*)'],
                                              ['info', '(?P<modify_connect_source>.*)', 'vrf',
                                               '(?P<vrf>.*)'],
                                              ['info', '(?P<modify_connect_source>.*)', 'oper_status',
                                               'up']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[(.*)][ipv4][(.*)][ip]',
                                              'info[(.*)][vrf]',
                                              'info[(.*)][oper_status]']},
                                          'exclude': interface_exclude},
                                    'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', NotExists('peer_as')]],
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)][peer_as]',
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)][connected_source]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'connected_source',
                                          '(?P<modify_connect_source>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'connect_source', '(?P<modify_connect_source>.*)'],
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'session_state', '(^(?!established).*)']],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)]']},
                                    'exclude': msdp_exclude},
                                  'ops.interface.interface.Interface':{
                                    'requirements':[\
                                              ['info', '(?P<modify_connect_source>.*)', 'oper_status',
                                               'up']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[(.*)][ipv4][(.*)][ip]',
                                              'info[(.*)][vrf]',
                                              'info[(.*)][oper_status]']},
                                          'exclude': interface_exclude}},
                      num_values={'vrf': 1, 'peer': 1, 'modify_connect_source': 1})


class TriggerModifyMsdpPeerAs(TriggerModify):
    """Modify dynamically learned MSDP 'established' peer(s) remote-as
      then restore the configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned MSDP 'established' peer(s) remote-as
      then restore the configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
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
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`
                peer_as: `int`
                connected_source: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP 'established' peer(s) remote-as
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned MSDP peer(s) remote-as from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) remote-as from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # change 0xx to xx
    MODIFY_NAME = '333'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)]']},
                                          'exclude': msdp_exclude},
                                    'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', 'peer_as', '(?P<peer_as>.*)'],
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', 'connected_source',
                                               '(?P<connected_source>.*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)][connected_source]',
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)][peer_as]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'peer_as', MODIFY_NAME],
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'connected_source',
                                          '(?P<connected_source>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'peer_as', MODIFY_NAME]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})
