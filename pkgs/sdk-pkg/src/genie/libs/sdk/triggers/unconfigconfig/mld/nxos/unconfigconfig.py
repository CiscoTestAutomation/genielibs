'''NXOS Implementation for Mld unconfigconfig triggers'''

# python
from functools import partial

# ats
from pyats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from genie.libs.sdk.libs.utils.triggeractions import configure_add_attributes, verify_ops_or_logic
from genie.libs.conf.mld.mld_group import MldGroup

# Which key to exclude for Mld Ops comparison
mld_exclude = ['maker', 'expire', 'up_time']


class TriggerUnconfigConfigMldEnable(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned enabled Mld interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations
    of dynamically learned enabled Mld interface(s).

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

                interface: `str`
                vrf: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Mld Ops object and store the enabled Mld interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Mld interface(s)'s enable from step 1 
           with Mld Conf object
        4. Verify the Mld interface(s)'s enable from step 3
           are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'enable', True]],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)]']},
                                'exclude': mld_exclude}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'interface_attr', '(?P<interface>.*)', 'enable', True]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     NotExists('(?P<interface>.*)')]],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)]']},
                                'exclude': mld_exclude}},
                      num_values={'vrf': 1, 'interface': 1})


class TriggerUnconfigConfigMldVersion(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned enabled Mld interface(s)'s version."""

    __description__ = """Unconfigure and reapply the whole configurations
    of dynamically learned enabled Mld interface(s)'s version.

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

                interface: `str`
                vrf: `str`
                version: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Mld Ops object and store the enabled Mld interface(s)'s version
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Mld interface(s)'s version from step 1 
           with Mld Conf object
        4. Verify the Mld interface(s)'s version from step 3
           are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'enable', True],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'version', '(?P<version>^(?!2).*)']],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': mld_exclude}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'interface_attr', '(?P<interface>.*)', 'version',
                                          '(?P<version>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'version', 2]],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': mld_exclude}},
                      num_values={'vrf': 1, 'interface': 1})


class TriggerUnconfigConfigMldJoinGroup(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned enabled Mld interface(s)'s join-groups."""

    __description__ = """Unconfigure and reapply the whole configurations
    of dynamically learned enabled Mld interface(s)'s join-groups.

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

                interface: `str`
                vrf: `str`
                group: `str`
                join_group: `str`
                source: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Mld Ops object and store the enabled Mld interface(s)'s join-groups
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Mld interface(s)'s join-groups from step 1 
           with Mld Conf object
        4. Verify the Mld interface(s)'s join-groups from step 3
           are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'join_group', '(?P<join_group>.*)',
                                     'group', '(?P<group>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'join_group', '(?P<join_group>.*)',
                                     'source', r'(?P<source>\*)']],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': mld_exclude}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         [partial(configure_add_attributes,  # callable configuration
                                            add_obj=MldGroup,
                                            base=[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                  'interface_attr', '(?P<interface>.*)']],
                                            add_attribute=[['join_group', '(?P<group>.*)'],
                                                           ['join_group_source_addr', '(?P<source>.*)'],],
                                            add_method='add_groups',
                                        )]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements': [[partial(verify_ops_or_logic,
                                                      requires=[['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'join_group',
                                                                 NotExists('(?P<join_group>.*)')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', NotExists('join_group')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'join_group',
                                                                 '(?P<join_group>.*)', '(.*)']
                                                               ])
                                                  ],
                                                  [partial(verify_ops_or_logic,
                                                      requires=[['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'group', NotExists('(?P<group>.*)')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', NotExists('group')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'group', '(?P<group>.*)',
                                                                 'source', NotExists(r'(?P<source>\*)')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'group', '(?P<group>.*)',
                                                                 NotExists('source')]
                                                               ])
                                                  ],
                                                ],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': mld_exclude + ['static_group']}},
                      num_values={'vrf': 1, 'interface': 1, 'join_group': 1, 'group': 1, 'source': 1})


class TriggerUnconfigConfigMldStaticGroup(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned enabled Mld interface(s)'s static-groups."""

    __description__ = """Unconfigure and reapply the whole configurations
    of dynamically learned enabled Mld interface(s)'s static-groups.

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

                interface: `str`
                vrf: `str`
                group: `str`
                static_group: `str`
                source: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Mld Ops object and store the enabled Mld interface(s)'s static-groups
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Mld interface(s)'s static-groups from step 1 
           with Mld Conf object
        4. Verify the Mld interface(s)'s static-groups from step 3
           are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'static_group', '(?P<static_group>.*)',
                                     'group', '(?P<group>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'static_group', '(?P<static_group>.*)',
                                     'source', r'(?P<source>\*)']],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group]']},
                                'exclude': mld_exclude + ['last_reporter']}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         [partial(configure_add_attributes,  # callable configuration
                                            add_obj=MldGroup,
                                            base=[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                  'interface_attr', '(?P<interface>.*)']],
                                            add_attribute=[['static_group', '(?P<group>.*)'],
                                                           ['static_group_source_addr', '(?P<source>.*)'],],
                                            add_method='add_groups',
                                        )]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements': [[partial(verify_ops_or_logic,
                                                      requires=[['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'static_group',
                                                                 NotExists('(?P<static_group>.*)')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', NotExists('static_group')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'static_group',
                                                                 '(?P<static_group>.*)', '(.*)']
                                                               ])
                                                  ],
                                                  [partial(verify_ops_or_logic,
                                                      requires=[['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'group', NotExists('(?P<group>.*)')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', NotExists('group')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'group', '(?P<group>.*)',
                                                                 'source', NotExists(r'(?P<source>\*)')],
                                                                ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                                                 '(?P<interface>.*)', 'group', '(?P<group>.*)',
                                                                 NotExists('source')]
                                                               ])
                                                  ],
                                                ],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group]']},
                                'exclude': mld_exclude + ['last_reporter']}},
                      num_values={'vrf': 1, 'interface': 1, 'static_group': 1, 'group': 1})

