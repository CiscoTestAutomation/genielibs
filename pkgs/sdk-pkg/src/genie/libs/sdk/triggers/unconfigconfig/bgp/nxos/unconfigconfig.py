'''NXOS Implementation for BGP unconfigconfig triggers'''

# python
import logging
from functools import partial

log = logging.getLogger(__name__)

# ATS
from ats import aetest
from ats.utils.objects import NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.libs.utils.triggeractions import Configure
from genie.libs.sdk.libs.utils.mapping import Mapping, Different
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# ipaddress
from ipaddress import IPv4Address, IPv6Address


# Which keys to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'last_reset',
               'keepalives', 'total', 'total_bytes', 'up_time',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'route_reflector_client', 'capability',
               'distance_internal_as', 'bgp_neighbor_counters', 'memory_usage',
               'total_entries', 'routing_table_version', 'total_memory',
               'path', 'prefixes', 'cluster_id', 'distance_extern_as']


class TriggerUnconfigConfigBgpNeighborSendCommunity(TriggerUnconfigConfig):
    """Unconfigure send-community under BGP and
        reapply the whole configurations for learned BGP."""

    __description__ = """Unconfigure send-community under BGP and reapply the
                    whole configurations for learned BGP
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

    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure send-community under bgp pid from step 1
           with BGP Conf object
        4. Verify the send-comunity from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)','vrf', '(?P<vrf>.*)',
                                                           'neighbor','(?P<neighbor>.*)','address_family','(?P<af>.*)',
                                                           'send_community','(?P<send_community>.*)'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                          'all_keys':True,
                                          'kwargs':{'attributes': ['info']},
                                          'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                      'neighbor_attr','(?P<neighbor>.*)',
                                                      'address_family_attr','(?P<af>.*)', 'nbr_af_send_community','(?P<send_community>.*)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)','vrf', '(?P<vrf>.*)',
                                                           'neighbor','(?P<neighbor>.*)','address_family','(?P<af>.*)',
                                                           'send_community']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'bgp_id':1, 'instance':1 , 'vrf':1, 'af':1, 'neighbor':1 })


class TriggerUnconfigConfigBgpNeighborSendCommunityExtended(TriggerUnconfigConfig):
    """Unconfigure send-community extended under a BGP neighbor and
       reapply the whole configurations of dynamically learned BGP pid"""

    __description__ = """Unconfigure send-community extended for a BGP neighbor and
       reapply the whole configurations of dynamically learned BGP pid

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

    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure send-community extended for a BGP neighbor of learned BGP pid from step 1
        4. Verify the send-community extended for BGP neighbor from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)','vrf', '(?P<vrf>.*)',
                                                           'neighbor','(?P<neighbor>.*)','address_family','(?P<af>.*)',
                                                           'send_community','(?P<send_community>(both|extended)+)$'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                          'all_keys':True,
                                          'kwargs':{'attributes': ['info']},
                                          'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                      'neighbor_attr','(?P<neighbor>.*)',
                                                      'address_family_attr','(?P<af>.*)', 'nbr_af_send_community','(?P<send_community>.*)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)','vrf', '(?P<vrf>.*)',
                                                           'neighbor','(?P<neighbor>.*)','address_family','(?P<af>.*)',
                                                           'send_community']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'bgp_id':1, 'instance':1 , 'vrf':1, 'af':1, 'neighbor':1 })

class TriggerUnconfigConfigBgpNeighborSoftReconfiguration(TriggerUnconfigConfig):
    """Unconfigure soft-reconfiguration inbound for a BGP neighbor and
           reapply the whole configurations for learned BGP pid"""

    __description__ = """Unconfigure soft-reconfiguration inbound for a BGP neighbor and
           reapply the whole configurations for learned BGP pid

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

        steps:
            1. Learn BGP Ops object and store the BGP instance(s)
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure soft-reconfiguration inbound for a BGP neighbor of learned BGP pid from step 1
            4. Verify the soft-reconfiguration for BGP neighbor from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)','vrf', '(?P<vrf>.*)',
                                                           'neighbor','(?P<neighbor>.*)','address_family','(?P<af>.*)',
                                                           'soft_configuration',True ],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                          'all_keys':True,
                                          'kwargs':{'attributes': ['info']},
                                          'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements': [['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                      'neighbor_attr','(?P<neighbor>.*)',
                                                      'address_family_attr','(?P<af>.*)',
                                                      'nbr_af_soft_reconfiguration',True]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)','vrf', '(?P<vrf>.*)',
                                                           'neighbor','(?P<neighbor>.*)','address_family','(?P<af>.*)',
                                                           'soft_configuration']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'bgp_id':1, 'instance':1 , 'vrf':1, 'neighbor':1 })


class TriggerUnconfigConfigBgpKeepaliveHoldtime(TriggerUnconfigConfig):
    """Unconfigure keepalive interval and holdtime  and
        reapply the whole configurations for learned BGP pid"""

    __description__ = """Unconfigure keepalive interval and holdtime and
               reapply the whole configurations for learned BGP pid

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

            steps:
                1. Learn BGP Ops object and store the BGP instance(s)
                   if has any, otherwise, SKIP the trigger
                2. Save the current device configurations through "method" which user uses
                3. Unconfigure keepalive interval and holdtime for learned BGP pid from step 1
                4. Verify the keepalive interval and holdtime for BGP pid from step 3 are no longer existed
                5. Recover the device configurations to the one in step 2
                6. Learn BGP Ops again and verify it is the same as the Ops in step 1
        """
    mapping = Mapping(\
            requirements={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        [['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'keepalive_interval', '(?P<keepalive_interval>.*)']],
                        [['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'holdtime', '(?P<holdtime>.*)']]],
                    'exclude': bgp_exclude},
                'ops.bgp.bgp.Bgp': {
                    'requirements': [\
                        ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                    'all_keys':True,
                    'kwargs': {'attributes': ['info']},
                    'exclude': bgp_exclude}},
            config_info={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'keepalive_interval', '(?P<keepalive_interval>.*)'],
                        ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'holdtime', '(?P<holdtime>.*)']],
                    'verify_conf': False,
                    'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
            verify_ops={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'keepalive_interval'],
                        ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'holdtime']],
                    'exclude': bgp_exclude}},
            num_values={'device': 1, 'bgp_id': 1, 'vrf': 1, 'instance': 1, 'neighbor': 1})


class TriggerUnconfigConfigBgpFastExternalFallover(TriggerUnconfigConfig):
    """Unconfigure fast-external-fallover and reapply the whole configurations for learned BGP pid"""

    __description__ = """Unconfigure fast-external-fallover under a BGP and
                   reapply the whole configurations for learned BGP pid

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

                steps:
                    1. Learn BGP Ops object and store the BGP instance(s)
                       if has any, otherwise, SKIP the trigger
                    2. Save the current device configurations through "method" which user uses
                    3. Unconfigure fast-external-fallover under learned BGP pid from step 1
                    4. Verify the fast-external-fallover under BGP pid from step 3 are no longer existed
                    5. Recover the device configurations to the one in step 2
                    6. Learn BGP Ops again and verify it is the same as the Ops in step 1
            """


    mapping = Mapping(\
            requirements={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'fast_external_fallover', True]],
                    'exclude': bgp_exclude},
                'ops.bgp.bgp.Bgp': {
                    'requirements': [\
                        ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                    'all_keys':True,
                    'kwargs': {'attributes': ['info']},
                    'exclude': bgp_exclude}},
            config_info={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'fast_external_fallover', True]],
                    'verify_conf': False,
                    'kwargs': {'mandatory': {'bgp_id': [['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']]}}}},
            verify_ops={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'fast_external_fallover']],
                    'exclude': bgp_exclude}},
            num_values={'device': 1, 'bgp_id': 1, 'vrf': 1, 'instance': 1, 'neighbor': 1})


class TriggerUnconfigConfigBgpGracefulRestart(TriggerUnconfigConfig):
    """Unconfigure graceful restart configured under BGP and then
    reapply the whole configuration of dynamically learned BGP instance(s)."""

    __description__ = """Unconfigure graceful restart configured under BGP and then 
    reapply the whole configuration of dynamically learned BGP instance(s).

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

    Steps:
        1. Learn BGP Ops object and store the BGP instance(s) if any,
           else SKIP the trigger
        2. Save the current device configurations using the "method" specified
           by user in Trigger YAML.
        3. Unconfigure the learned BGP instance(s) from step 1
           with BGP Conf object
        4. Verify the BGP instance(s) from step 3 no longer exists
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    @aetest.test
    def verify_unconfigure(self, uut, abstract, steps):
        '''Verify that the unconfiguration was done correctly and Ops state is
           as expected.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                            steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        'unconfigure feature', from_exception=e)

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart', True]],
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'graceful_restart', True]],
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart', False]],
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerUnconfigConfigBgpNeighborDefaultOriginate(TriggerUnconfigConfig):
    """Unconfigure default originate configured under BGP neighbor and then
    reapply the whole configuration of dynamically learned BGP instance(s)."""

    __description__ = """Unconfigure default originate configured under BGP neighbor and then 
    reapply the whole configuration of dynamically learned BGP instance(s).

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

    Steps:
        1. Learn BGP Ops object and store the BGP instance(s) if any,
           else SKIP the trigger
        2. Save the current device configurations using the "method" specified
           by user in Trigger YAML.
        3. Unconfigure the learned BGP instance(s) from step 1
           with BGP Conf object
        4. Verify the BGP instance(s) from step 3 no longer exists
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'default_originate', True],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'address_family_attr', '(?P<address_family>.*)', 'nbr_af_default_originate', True]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'default_originate']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerUnconfigConfigBgpNeighborNextHopSelf(TriggerUnconfigConfig):
    """Unconfigure next hop self configured under BGP neighbor and then
    reapply the whole configuration of dynamically learned BGP instance(s)."""

    __description__ = """Unconfigure next hop self configured under BGP neighbor and then 
    reapply the whole configuration of dynamically learned BGP instance(s).

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

    Steps:
        1. Learn BGP Ops object and store the BGP instance(s) if any,
           else SKIP the trigger
        2. Save the current device configurations using the "method" specified
           by user in Trigger YAML.
        3. Unconfigure the learned BGP instance(s) from step 1
           with BGP Conf object
        4. Verify the BGP instance(s) from step 3 no longer exists
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'next_hop_self', True],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'address_family_attr', '(?P<address_family>.*)', 'nbr_af_next_hop_self', True]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'next_hop_self']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerUnconfigConfigBgpNeighborTransportConnectionModePassive(TriggerUnconfigConfig):
    """Unconfigure transportation connection mode (if passive) configured under
    BGP neighbor and then reapply the whole configuration of dynamically 
    learned BGP instance(s)."""

    __description__ = """Unconfigure transportation connection mode (if passive) configured under 
    BGP neighbor and then reapply the whole configuration of dynamically 
    learned BGP instance(s).

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

    Steps:
        1. Learn BGP Ops object and store the BGP instance(s) if any,
           else SKIP the trigger
        2. Save the current device configurations using the "method" specified
           by user in Trigger YAML.
        3. Unconfigure the learned BGP instance(s) from step 1
           with BGP Conf object
        4. Verify the BGP instance(s) from step 3 no longer exists
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'bgp_session_transport', 'connection', 'mode', 'passive'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'nbr_transport_connection_mode', 'passive']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'bgp_session_transport', 'connection', 'mode']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerUnconfigConfigBgpNeighborPassword(TriggerUnconfigConfig):
    """Unconfigure the password configured under BGP neighbor and then
    reapply the whole configuration of dynamically learned BGP instance(s)."""

    __description__ = """Unconfigure the password configured under BGP neighbor and then 
    reapply the whole configuration of dynamically learned BGP instance(s).

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

    Steps:
        1. Learn BGP Ops object and store the BGP instance(s) if any,
           else SKIP the trigger
        2. Save the current device configurations using the "method" specified
           by user in Trigger YAML.
        3. Unconfigure the learned BGP instance(s) from step 1
           with BGP Conf object
        4. Verify the BGP instance(s) from step 3 no longer exists
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'password_text', '(?P<password_text>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'nbr_password_text', '(?P<password_text>.*)']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'nbr_password_text']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerUnconfigConfigBgpNeighborBfd(TriggerUnconfigConfig):
    """Unconfigure bfd configured under BGP neighbor and then
    reapply the whole configuration of dynamically learned BGP instance(s)."""

    __description__ = """Unconfigure bfd configured under BGP neighbor and then 
    reapply the whole configuration of dynamically learned BGP instance(s).

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

    Steps:
        1. Learn BGP Ops object and store the BGP instance(s) if any,
           else SKIP the trigger
        2. Save the current device configurations using the "method" specified
           by user in Trigger YAML.
        3. Unconfigure the learned BGP instance(s) from step 1
           with BGP Conf object
        4. Verify the BGP instance(s) from step 3 no longer exists
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'fall_over_bfd', True],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'nbr_fall_over_bfd', True]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'fall_over_bfd']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerUnconfigConfigBgpNeighborRouteReflectorClient(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned BGP neighbor(s) route-reflector-client."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned BGP neighbor(s) route-reflector-client.

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP neighbor(s) with route-reflector-client
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP neighbor(s) route-reflector-client from step 1 
           with BGP Conf object
        4. Verify the BGP vrf(s) route_distinguisher from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # configuration steps callable
    def unconfigure_route_ref(self, conf_obj, path, **kwargs):

        paths = self._path_population([path], kwargs['device'])
        # find position that neighbor (ip) sit
        # replace ip string to IPv4Address object
        for path in paths:
            ipv4_index_list = [path.index(val) for val in path if '.' in str(val)]
            ipv6_index_list = [path.index(val) for val in path if ':' in str(val)]

            for index in ipv4_index_list:
                path[index] = IPv4Address(path[index])
            for index in ipv6_index_list:
                path[index] = IPv6Address(path[index])

        config = '\n'.join([str(conf_path) for conf_path in paths])
        log.info('With following configuration:\n{c}'
                 .format(c=config))

        Configure.conf_configure(device=kwargs['device'],
                                 conf=conf_obj,
                                 conf_structure=paths,
                                 unconfig=True)


    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'address_family',
                                                           '(?P<address_family>.*)',
                                                           'route_reflector_client', True],
                                                           ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[[partial(unconfigure_route_ref, path = ['device_attr', '{uut}', 'vrf_attr',
                                                      '(?P<vrf>.*)', 'neighbor_attr',
                                                      '(?P<neighbor>.*)', 'address_family_attr',
                                                      '(?P<address_family>.*)',
                                                      'nbr_af_route_reflector_client', True])
                                                    ]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                     'vrf', '(?P<vrf>.*)', 'neighbor',
                                                     '(?P<neighbor>.*)', 'address_family',
                                                     '(?P<address_family>.*)',
                                                     'route_reflector_client']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':'all', 'instance':'all', 'neighbor': 'all',
                                  'address_family':'all', 'rd': 'all'})


class TriggerUnconfigConfigBgpNeighborIpv4(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned BGP IPv4 neighbor(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned BGP IPv4 neighbor(s).

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP IPv4 neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP IPv4 neighbor(s) from step 1 
           with BGP Conf object
        4. Verify the BGP IPv4 neighbor(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>^[\d\.]+$)', 'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                      'neighbor_attr','(?P<neighbor>^[\d\.]+$)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor',
                                                   '(?P<neighbor>.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude + ['vpnv4 unicast']}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})


class TriggerUnconfigConfigBgpNeighborIpv6(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned BGP IPv6 neighbor(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned BGP IPv6 neighbor(s).

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP IPv6 neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP IPv6 neighbor(s) from step 1 
           with BGP Conf object
        4. Verify the BGP IPv6 neighbor(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>^[\w\:]+$)', 'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                      'neighbor_attr','(?P<neighbor>^[\w\:]+$)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor',
                                                   '(?P<neighbor>.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})


class TriggerUnconfigConfigBgpNeighborIbgp(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned iBGP neighbor(s)."""
    
    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned iBGP neighbor(s).

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the iBGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned iBGP neighbor(s) from step 1 
           with BGP Conf object
        4. Verify the iBGP neighbor(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'bgp_id', '(?P<bgp_id>.*)'],
                                                           ['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'remote_as',
                                                           '(?P<bgp_id>.*)'],
                                                           ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'session_state', 'established']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                        'neighbor_attr','(?P<neighbor>.*)']
                                      ],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor',
                                                   '(?P<neighbor>.*)', '(.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1,
                                  'neighbor':1, 'bgp_id': 1})


class TriggerUnconfigConfigBgpRouterId(TriggerUnconfigConfig):
    """Unconfigure and reapply the bgp-id of dynamically learned BGP instance(s)."""
    
    __description__ = """Unconfigure and reapply the bgp-id of dynamically learned BGP instance(s).

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Conf object and store the BGP instance(s)
           if has bgp_id configured, otherwise, SKIP the trigger.
           And learn BGP ops object for verifying in step 4 and 6
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP instance(s) bgp-id from step 1 
           with BGP Conf object
        4. Verify the BGP instance(s) bgp-id from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)','router_id', '(?P<routerId>.*)'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude},
                                    'conf.bgp.Bgp':{
                                          'requirements':[['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                                           'router_id', '(?P<router_id>.*)']]}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                      'router_id', '(?P<router_id>.*)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', NotExists('router_id')]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude},
                                  'conf.bgp.Bgp':{
                                    'requirements': [['device_attr', '{uut}', '_vrf_attr',
                                                      '(?P<vrf>.*)', 'router_id', '(?P<router_id>.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'router_id':'all'})
    

class TriggerUnconfigConfigBgpNeighborVrf(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned BGP IPv6 neighbor(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned BGP IPv6 neighbor(s).

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP IPv6 neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP IPv6 neighbor(s) from step 1 
           with BGP Conf object
        4. Verify the BGP IPv6 neighbor(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>^(?!default).*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>^(?!default).*)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})


class TriggerUnconfigConfigBgpNeighborAsOverride(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned BGP neighbors(s) as_override."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned BGP neighbors(s) as_override.

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP neighbors(s)
           if has as_override enabled, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP neighbors(s) as_override from step 1 
           with BGP Conf object
        4. Verify the BGP neighbors(s) as_override from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # configuration steps callable
    def unconfigure_route_ref(self, conf_obj, path, **kwargs):

        paths = self._path_population([path], kwargs['device'])
        # find position that neighbor (ip) sit
        # replace ip string to IPv4Address object
        for path in paths:
            ipv4_index_list = [path.index(val) for val in path if '.' in str(val)]
            ipv6_index_list = [path.index(val) for val in path if ':' in str(val)]

            for index in ipv4_index_list:
                path[index] = IPv4Address(path[index])
            for index in ipv6_index_list:
                path[index] = IPv6Address(path[index])

        config = '\n'.join([str(conf_path) for conf_path in paths])
        log.info('With following configuration:\n{c}'
                 .format(c=config))

        Configure.conf_configure(device=kwargs['device'],
                                 conf=conf_obj,
                                 conf_structure=paths,
                                 unconfig=True)

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                           'address_family', '(?P<address_family>.*)',
                                                           'as_override', True],
                                                          ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[[partial(unconfigure_route_ref, path = [
                                                        'device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                        'neighbor_attr', '(?P<neighbor>.*)', 'address_family_attr',
                                                        '(?P<address_family>.*)', 'nbr_af_as_override', True]),
                                      ]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                      'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                      'address_family', '(?P<address_family>.*)',
                                                      'as_override']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'address_family':'all', 'neighbor': 'all'})


class TriggerUnconfigConfigBgpNeighborEbgp(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned EBGP neighbor(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned EBGP neighbor(s).

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the EBGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned EBGP neighbor(s) from step 1 
           with BGP Conf object
        4. Verify the BGP IPv6 neighbor(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>^(?!default).*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>^(?!default).*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'remote_as', Different('(?P<bgp_id>.*)')]],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>^(?!default).*)',
                                                      'neighbor_attr','(?P<neighbor>.*)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor',
                                                   '(?P<neighbor>.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude + ['vpnv4 unicast']}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})


class TriggerUnconfigConfigBgpVpnRd(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned BGP vrf(s) route-distinguisher."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned BGP vrf(s) route-distinguisher.

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP vrf(s) with route_distinguisher
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP vrf(s) route-distinguisher from step 1 
           with BGP Conf object
        4. Verify the BGP vrf(s) route_distinguisher from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['table', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'address_family',
                                                           '(?P<address_family>.*)', 'route_distinguisher',
                                                           '(?P<rd>.*)'],
                                                           ['table', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'address_family',
                                                           '(?P<address_family>.*)', 'default_vrf',
                                                           '(?P<name>.*)']],
                                        'kwargs':{'attributes':['table', 'info']},
                                        'exclude': bgp_exclude},
                                    'ops.vrf.vrf.Vrf':{
                                          'requirements':[['info', 'vrfs', '(?P<name>^(?!default).*)',
                                                           'route_distinguisher', '(?P<rd>.*)']],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': ['maker']}},
                      config_info={'conf.vrf.Vrf':{
                                     'requirements':[['device_attr', '{uut}', 'rd', '(?P<rd>.*)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'name': '(?P<name>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['table', 'instance', '(?P<instance>.*)',
                                                     'vrf', '(?P<vrf>.*)', 'address_family',
                                                     '(?P<address_family>.*)', 'route_distinguisher'],
                                                     ['table', 'instance', '(?P<instance>.*)',
                                                     'vrf', '(?P<vrf>.*)', 'address_family',
                                                     '(?P<address_family>.*)', 'default_vrf']],
                                    'kwargs':{'attributes':['table', 'info']},
                                    'exclude': bgp_exclude + ['label_allocation_mode']},
                                  'ops.vrf.vrf.Vrf':{
                                        'requirements':[['info', 'vrfs', '(?P<name>.*)',
                                                         'route_distinguisher']],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': ['maker']}},
                      num_values={'vrf': 'all', 'instance':1, 
                                  'address_family': 'all', 'rd': 1, 'name': 1})


class TriggerUnconfigConfigBgpL2vpnCapability(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned BGP l2vpn evpn address-family."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned BGP l2vpn evpn address-family.

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
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP l2vpn evpn address-family
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP l2vpn evpn address-family from step 1 
           with BGP Conf object
        4. Verify the BGP l2vpn evpn address-family from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)',
                             'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>^l2vpn +evpn$)',
                             'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info[instance][(.*)][bgp_id]',
                                    'info[list_of_vrfs]',
                                    'info[instance][(.*)][vrf][(.*)][neighbor]'
                                       '[(.*)][address_family][(.*)][session_state]']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                             'neighbor_attr', '(?P<neighbor>.*)', 'address_family_attr', '(?P<address_family>.*)']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)',
                             'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>^l2vpn +evpn$)']],
                        'kwargs':{'attributes':['info[instance][(.*)][bgp_id]',
                                    'info[list_of_vrfs]',
                                    'info[instance][(.*)][vrf][(.*)][neighbor]'
                                       '[(.*)][address_family][(.*)][session_state]']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1 , 'address_family': 1})


