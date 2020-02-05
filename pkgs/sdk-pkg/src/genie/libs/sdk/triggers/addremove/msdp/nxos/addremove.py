'''NXOS Implementation for Msdp add-remove triggers'''

# python
import logging
from copy import deepcopy
from time import sleep

# import pyats
from pyats import aetest
from pyats.utils.objects import find, R, NotExists ,Not

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)

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
                     

class TriggerAddRemoveMsdpOriginatorId(TriggerAddRemove):
    """Apply the MSDP originator-id, add remove added MSDP originator-id"""

    __description__ = """Apply the MSDP originator-id, add remove added MSDP originator-id.

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
        1. Learn Msdp Ops/Conf object and store the MSDP originator-id, learn Interface ops to 
           get interface with ip address and under same vrf as msdp originator-id.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of interface as msdp originator-id with Msdp Conf object
        4. Verify the msdp originator-id from step 3 has configured
        5. Remove the msdp originator-id configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1

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
                                               '(?P<vrf>.*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[(.*)][ipv4][(.*)][ip]',
                                              'info[(.*)][vrf]']},
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
                                          'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1, 'modify_originator_id': 1})


class TriggerAddRemoteMsdpSaFilterIn(TriggerAddRemove):
    """Apply MSDP peer(s) sa-filter in, and remove added MSDP peer(s) sa-filter in"""

    __description__ = """Apply MSDP peer(s) sa-filter in, and remove added MSDP peer(s) sa-filter in.

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

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP peer(s) which does not have sa-filter in.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp sa-filter in with Msdp Conf object
        4. Verify the msdp sa-filter in from step 3 has configured
        5. Remove the msdp sa-filter in configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_NAME = 'added_sa_filter_in'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                               NotExists('sa_filter'), NotExists('in')]],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                          'all_keys': True,
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'sa_filter_in', ADD_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                       'sa_filter', 'in', ADD_NAME]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerAddRemoveMsdpSaFilterOut(TriggerAddRemove):
    """Apply the MSDP peer(s) sa-filter out, and remove added MSDP peer(s) sa-filter out"""

    __description__ = """Apply the MSDP peer(s) sa-filter out, and
    remove added MSDP peer(s) sa-filter out.

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

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP peer(s) which does not have sa-filter out.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp sa-filter out with Msdp Conf object
        4. Verify the msdp sa-filter out from step 3 has configured
        5. Remove the msdp sa-filter out configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_NAME = 'added_sa_filter_out'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                               NotExists('sa_filter'), NotExists('out')]],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'sa_filter_out', ADD_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 
                                       'sa_filter', 'out', ADD_NAME]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][sa_filter]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerAddRemoveMsdpSaLimit(TriggerAddRemove):
    """Apply the MSDP peer(s) sa-limit, and remove added MSDP peer(s) sa-limit"""

    __description__ = """Apply the MSDP peer(s) sa-limit, and
    remove added MSDP peer(s) sa-limit.

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

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops object and store the MSDP peer(s) which does not have sa-limit.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp sa-limit with Msdp Conf object
        4. Verify the msdp sa-limit from step 3 has configured
        5. Remove the msdp sa-limit configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_NAME = 12345
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'sa_limit', 'unlimited']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_limit]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'sa_limit', ADD_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'sa_limit', str(ADD_NAME)]],
                                    'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][sa_limit]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerAddRemoveMsdpMeshGroup(TriggerAddRemove):
    """Apply the MSDP peer(s) mesh-group, and remove added MSDP peer(s) mesh-group"""

    __description__ = """Apply the MSDP peer(s) sa-limit, and
    remove added MSDP peer(s) sa-limit.

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

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Msdp Ops object and store the MSDP peer(s) which does not have mesh-group.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp mesh-group with Msdp Conf object
        4. Verify the msdp mesh-group from step 3 has configured
        5. Remove the msdp mesh-group configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_NAME = 'added_mesh_group'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', NotExists('mesh_group')]],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][mesh_group]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'mesh_group', ADD_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'mesh_group', ADD_NAME]],
                                    'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][mesh_group]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerAddRemoveMsdpKeepaliveHoldtime(TriggerAddRemove):
    """Apply the MSDP peer(s) keepalive&holdtime interval,
    and remove added MSDP peer(s) keepalive&holdtime interval"""

    __description__ = """Apply the MSDP peer(s) keepalive&holdtime interval, and
    remove added MSDP peer(s) keepalive&holdtime interval.

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

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Msdp Ops/Conf object and store the MSDP peer(s) which does not have
           keepalive&holdtime interval configured.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp keepalive&holdtime interval with Msdp Conf object
        4. Verify the msdp keepalive&holdtime interval from step 3 has configured
        5. Remove the msdp keepalive&holdtime interval configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1
    """
    # <1-60>  Keepalive interval in seconds
    keepalive_interval = 20
    # <1-90>  Keepalive timeout in seconds
    holdtime_interval = 40

    @aetest.test
    def add_configuration(self, uut, abstract, steps):
        '''need to sleep for the changed time interval taken place
        '''
        super().add_configuration(uut, abstract, steps)
        # sleep 
        log.info('sleep %s for msdp re-connect after changing the '
          'keepalive/holdtime interval' % self.holdtime_interval)
        sleep(self.holdtime_interval)

    @aetest.test
    def remove_configuration(self, uut, abstract, steps):
        '''need to sleep for the changed time interval taken place
        '''
        super().remove_configuration(uut, abstract, steps)
        # sleep default value since it will use default when removing the keepalive configs
        log.info('sleep %s for msdp re-connect after changing the '
          'keepalive/holdtime interval' % '90')
        sleep(90)

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', NotExists('keepalive_interval')],
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', NotExists('holdtime_interval')]],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)]']},
                                          'exclude': msdp_exclude},
                                    'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][peer][(.*)][session_state]',
                                                  'info[vrf][(.*)][peer][(.*)][timer][holdtime_interval]',
                                                  'info[vrf][(.*)][peer][(.*)][timer][keepalive_interval]']},
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
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][peer][(.*)][session_state]',
                                                  'info[vrf][(.*)][peer][(.*)][timer][holdtime_interval]',
                                                  'info[vrf][(.*)][peer][(.*)][timer][keepalive_interval]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerAddRemoveMsdpReconnectInterval(TriggerAddRemove):
    """Apply the MSDP vrf(s) reconnect interval,
    and remove added MSDP vrf(s) reconnect interval"""

    __description__ = """Apply the MSDP vrf(s) reconnect interval, and
    remove added MSDP vrf(s) reconnect interval.

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

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Msdp Ops/Conf object and store the MSDP vrf(s) which does not have
           reconnect interval configured.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp reconnect interval with Msdp Conf object
        4. Verify the msdp reconnect interval from step 3 has configured
        5. Remove the msdp reconnect interval configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    # <1-60>  Interval in seconds
    connect_retry_interval = 33

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               NotExists('global_connect_retry_interval')]],
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)]']},
                                          'exclude': msdp_exclude},
                                    'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)]']},
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
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 'all'})


class TriggerAddRemoveMsdpDescription(TriggerAddRemove):
    """Apply the MSDP peer(s) description,
    and remove added MSDP peer(s) description"""

    __description__ = """Apply the MSDP vrf(s) description, and
    remove added MSDP vrf(s) description.

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

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Msdp Ops object and store the MSDP peer(s) which does not have
           description configured.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp description with Msdp Conf object
        4. Verify the msdp description from step 3 has configured
        5. Remove the msdp description configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_NAME = 'Added description'
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'conf.msdp.Msdp':{
                                          'requirements':[\
                                              ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)',
                                               '_peer_attr', '(?P<peer>.*)', NotExists('description')]],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'msdp[vrf_attr][(.*)][peer_attr][(.*)]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'description', ADD_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                       '(?P<peer>.*)', 'description', ADD_NAME]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][description]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 1, 'peer': 1})


class TriggerAddRemoveMsdpPeer(TriggerAddRemove):
    """Apply the msdp peer, and remove the added msdp peer."""

    __description__ = """Apply the msdp peer, and remove the added msdp peer.

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
                connect_source: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Msdp Ops object and store the "established" MSDP peer(s), get different peer
           address as new msdp peer.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of msdp peer with Msdp Conf object
        4. Verify the msdp peer from step 3 has configured
        5. Remove the msdp peer configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Msdp Ops again and verify it is the same as the Ops in step 1
    """

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        super().verify_prerequisite(uut, abstract, steps, timeout)

        with steps.start("Finding peer device of uut %s, "
          "and peer device id" % uut.name) as step:

            # initial new mapping keys list to update with the added peer values
            new_mapping_keys = []
            self.uut_peer = ''

            # get the route which are not in the existing msdp peers
            for item in self.mapping.keys:
                # get info from uut.neighbors, the structure should be
                # [<dev name>][vrf][<vrf>]
                #     [address_family][<af>][ip][<ip>][interface][<intf>]
                reqs = ['(?P<nbr>.*)', 'vrf', item.get('vrf', ''), 'address_family',
                        'ipv4', 'ip', '(?P<peer_ip>^(?!%s).*)' % item.get('peer', ''),
                        'interface', '(?P<peer_intf>.*)']
                ret = find([getattr(uut, 'neighbors', {})], R(reqs),
                           filter_=False, all_keys=True)
                if ret:
                    values = GroupKeys.group_keys(
                                reqs=[reqs], ret_num={}, source=ret, all_keys=True)
                    # pick one neighbor as added peer
                    if values:
                        neighbor_attrs = values[0]
                    else:
                        continue

                    new_mapping_keys.append(
                        {'vrf': item.get('vrf', ''),
                         'originator_id': item.get('originator_id', ''),
                         'peer_ip': neighbor_attrs.get('peer_ip', ''),
                         'peer_intf': neighbor_attrs.get('peer_intf', ''),
                         'connect_source': item.get('connect_source', '')})
                    # set this trigger uut peer device
                    self.uut_peer = self.parameters['testbed']\
                                      .devices[neighbor_attrs.get('nbr', '')]

                    if self.uut_peer and new_mapping_keys:
                        break

            # overwrite the mapping.keys for further mapping implementation
            if not self.uut_peer or not new_mapping_keys:
                self.skipped('Cannot find neighbor devices which has '
                             'different peer address', goto=['next_tc'])
            self.mapping.keys = new_mapping_keys

            # print out info
            log.info('\nFind peer device: %s \npeer device id: %s\n'
                     'uut local connect_source interface: %s\n' \
                     % (self.uut_peer.name,
                        self.mapping.keys[0].get('peer_ip'),
                        self.mapping.keys[0].get('peer_intf')))

    @aetest.test
    def save_configuration(self, uut, method, abstract):
      super().save_configuration(uut, method, abstract)
      # save uut restore obj
      self.uut_restore = self.lib
      super().save_configuration(self.uut_peer, method, abstract)
      # save peer restore obj
      self.peer_restore = self.lib

    @aetest.test
    def add_configuration(self, uut, abstract, steps):

      # store original config_info
      original_config_info = deepcopy(self.mapping.config_info)
      super().add_configuration(uut, abstract, steps)

      # change peer conf requirements to use uut msdp info
      for item in self.mapping.config_info['conf.msdp.Msdp']['requirements']:
          if 'connected_source' in item:
              item[-1] = '(?P<peer_intf>.*)'
              item[5] = '(?P<originator_id>.*)'
      super().add_configuration(self.uut_peer, abstract, steps)

      # revert original config_info
      self.mapping.config_info = original_config_info

    @aetest.test
    def remove_configuration(self, uut, abstract, steps):
      super().remove_configuration(uut, abstract, steps)

      # change peer conf requirements to use uut msdp info
      for item in self.mapping.config_info['conf.msdp.Msdp']['requirements']:
          if 'connected_source' in item:
              item[-1] = '(?P<peer_intf>.*)'
              item[5] = '(?P<originator_id>.*)'
              
      super().remove_configuration(self.uut_peer, abstract, steps)

    @aetest.test
    def restore_configuration(self, uut, method, abstract):
      # restore object point uut restore
      self.lib = self.uut_restore
      super().restore_configuration(uut, method, abstract)
      # restore object point peer restore
      self.lib = self.peer_restore
      super().restore_configuration(self.uut_peer, method, abstract)

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'global',
                                               'originator_id', '(?P<originator_id>.*)'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'connect_source', '(?P<connect_source>.*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][enable]',
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][connect_source]',
                                              'info[vrf][(.*)][global][originator_id]']},
                                          'exclude': msdp_exclude}},
                      config_info={'conf.msdp.Msdp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'enabled', True],
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer_ip>.*)',
                                          'connected_source', '(?P<connect_source>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[\
                                      ['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer_ip>.*)',
                                       'session_state', 'established']],
                                    'kwargs':{'attributes': [
                                                 'info[vrf][(.*)][peer][(.*)][enable]',
                                                 'info[vrf][(.*)][peer][(.*)][session_state]',
                                                 'info[vrf][(.*)][peer][(.*)][connect_source]',
                                                 'info[vrf][(.*)][global][originator_id]']},
                                    'exclude': msdp_exclude}},
                      num_values={'vrf': 'all', 'peer': 'all'})