'''NXOS Implementation for Msdp unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# import pyats
from pyats.utils.objects import Not, NotExists

# Which key to exclude for Msdp Ops comparison
msdp_exclude = ['maker', 'elapsed_time', 'discontinuity_time',
           'keepalive', 'total', 'up_time', 'expire', 'remote',
           'last_message_received', 'num_of_comparison', 'rpf_failure',
           'total_accept_count', 'total_reject_count', 'notification']


class TriggerUnconfigConfigMsdpPeer(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s).

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
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vrf: `str`
                peer: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the "established" MSDP peer(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned MSDP peer(s) from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', NotExists('(?P<peer>.*)')]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer':1})


class TriggerUnconfigConfigMsdpSaFilterIn(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) sa-filter in."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) sa-filter in.

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
        3. Unconfigure the learned MSDP peer(s) sa-filter in from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) sa-filter in from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
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
                                          'peer_attr', '(?P<peer>.*)', 'sa_filter_in','(?P<sa_filter_in>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                       'sa_filter', NotExists('in')]], # , '(?P<sa_filter_in>.*)'
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer':1})


class TriggerUnconfigConfigMsdpSaFilterOut(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) sa-filter out."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) sa-filter out.

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
        3. Unconfigure the learned MSDP peer(s) sa-filter out from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) sa-filter out from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
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
                                          'peer_attr', '(?P<peer>.*)', 'sa_filter_out','(?P<sa_filter_out>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                       'sa_filter', NotExists('out')]], # , '(?P<sa_filter_out>.*)'
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer':1})


class TriggerUnconfigConfigMsdpSaLimit(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) sa-limit."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) sa-limit.

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
        3. Unconfigure the learned MSDP peer(s) sa-limit from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) sa-limit from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'sa_limit', r'(?P<sa_limit>\d+)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_limit]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'sa_limit',r'(?P<sa_limit>\d+)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'sa_limit', 'unlimited']],
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][peer][(.*)][session_state]',
                                                  'info[vrf][(.*)][peer][(.*)][sa_limit]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer':1})


class TriggerUnconfigConfigMsdpMeshGroup(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned 'established' MSDP peer(s) mesh group."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned 'established' MSDP peer(s) mesh group.

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
        3. Unconfigure the learned MSDP peer(s) mesh group from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) mesh group from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
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
                                          'peer_attr', '(?P<peer>.*)', 'mesh_group','(?P<mesh_group>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', NotExists('mesh_group')]], # , '(?P<mesh_group>.*)'
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][peer][(.*)][session_state]',
                                                  'info[vrf][(.*)][peer][(.*)][mesh_group]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer':1})


class TriggerUnconfigConfigMsdpOriginatorId(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP originator-id."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP originator-id.

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
                originator_id: `str`
                originating_rp: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP originator-id
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned MSDP originator-id from step 1 
           with Msdp Conf object
        4. Verify the MSDP originator-id from step 3 are no longer existed
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
                                    'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               'originating_rp', '(?P<originating_rp>.*)']],
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][originating_rp]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'originating_rp', '(?P<originating_rp>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'conf.msdp.Msdp':{
                                    'requirements':[\
                                        ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                         NotExists('originating_rp')]], # , '(?P<originating_rp>.*)'
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][originating_rp]',
                                                  'info[vrf][(.*)][peer][(.*)][session_state]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer':1})


class TriggerUnconfigConfigMsdpKeepaliveHoldtime(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) keepalive&holdtime interval."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) keepalive&holdtime interval.

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
        1. Learn Msdp Ops object and store the MSDP peer(s)
           keepalive&holdtime interval if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned MSDP peer(s) keepalive&holdtime interval from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) keepalive&holdtime interval from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', 'keepalive_interval',
                                               '(?P<keepalive_interval>.*)'],
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', 'holdtime_interval',
                                               '(?P<holdtime_interval>.*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)]']},
                                          'exclude': msdp_exclude},
                                    'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                               'timer', 'keepalive_interval', '(?P<keepalive_interval>.*)'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                               'timer', 'holdtime_interval', '(?P<holdtime_interval>.*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][timer]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'peer_attr',
                                          '(?P<peer>.*)', 'keepalive_interval','(?P<keepalive_interval>.*)'],
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'peer_attr',
                                          '(?P<peer>.*)', 'holdtime_interval','(?P<holdtime_interval>.*)']],
                                       'verify_conf': True,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                          ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                           'timer', 'keepalive_interval', 60], # change to default value
                                          ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                           'timer', 'holdtime_interval', 90]], # change to default value
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][peer][(.*)][session_state]',
                                                  'info[vrf][(.*)][peer][(.*)][timer]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer':1})


class TriggerUnconfigConfigMsdpReconnectInterval(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP reconnect interval."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP reconnect interval.

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
        3. Unconfigure the learned MSDP reconnect interval from step 1 
           with Msdp Conf object
        4. Verify the MSDP reconnect interval from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               'global_connect_retry_interval',
                                               '(?P<connect_retry_interval>.*)']],
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][global_connect_retry_interval]']},
                                          'exclude': msdp_exclude},
                                    'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 'timer',
                                               'connect_retry_interval', '(?P<connect_retry_interval>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][timer]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'global_connect_retry_interval', '(?P<connect_retry_interval>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 'timer',
                                       'connect_retry_interval', 10]], # change to default value
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][peer][(.*)][session_state]',
                                                  'info[vrf][(.*)][peer][(.*)][timer]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 'all'})


class TriggerUnconfigConfigMsdpDescription(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) description."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned MSDP peer(s) description.

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
        1. Learn Msdp Ops object and store the MSDP peer(s) description
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned MSDP peer(s) description from step 1 
           with Msdp Conf object
        4. Verify the MSDP peer(s) description from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', 'description',
                                               '(?P<description>.*)']],
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)]']},
                                          'exclude': msdp_exclude},
                                    'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'description', '(?P<description>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][description]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'description','(?P<description>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', NotExists('description')]], # , '(?P<description>.*)'
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][peer][(.*)][session_state]',
                                                  'info[vrf][(.*)][peer][(.*)][description]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})
