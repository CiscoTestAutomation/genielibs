'''Implementation for bgp unconfigconfig triggers'''

# python
import logging
import time

log = logging.getLogger(__name__)

# ATS
from pyats import aetest
from pyats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'capability',
               'keepalives', 'total', 'total_bytes', 'up_time', 'last_reset',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'distance_internal_as', 'bgp_neighbor_counters',
               'memory_usage', 'total_entries', 'routing_table_version',
               'total_memory', 'totals', 'distance_extern_as', 'reset_reason',
               'holdtime', 'keepalive_interval']


class TriggerUnconfigConfigBgp(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned BGP instance(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned BGP instance(s).

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

                bgp_id: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned BGP instance(s) from step 1
           with BGP Conf object
        4. Verify the BGP instance(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'bgp_id', '(?P<bgp_id>.*)']],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [[NotExists('info')]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'bgp_id':'all', 'instance':'all'})


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
           static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.
                instance: `str`
                vrf: `str`
                neighbor: `str`
                address_family: `str`
                rd: `str`
                default_vrf: `str`
                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
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

    @aetest.test
    def verify_unconfigure(self, uut, abstract, steps):
        time.sleep(120)
        super().verify_unconfigure(uut, abstract, steps)

    mapping = Mapping(requirements={
                          'ops.bgp.bgp.Bgp': {
                              'requirements': [['table', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<address_family>.*)', 'route_distinguisher', '(?P<rd>.*)']],
                              'kwargs': {
                                  'attributes': ['table', 'info']
                              },
                              'exclude': bgp_exclude + ['table_version']
                          },
                          'ops.vrf.vrf.Vrf': {
                              'requirements': [['info', 'vrfs', '(?P<vrf>.*)', 'route_distinguisher', '(?P<rd>.*)']],
                              'kwargs': {
                                  'attributes': ['info']
                              },
                              'exclude': ['maker']
                          }
                      },
                      config_info={
                          'conf.vrf.Vrf': {
                              'requirements': [['device_attr', '{uut}', 'rd', '(?P<rd>.*)']],
                              'verify_conf': False,
                              'kwargs': {
                                  'mandatory': {
                                      'name': '(?P<vrf>.*)'
                                  }
                              }
                          }
                      },
                      verify_ops={
                          'ops.bgp.bgp.Bgp': {
                              'requirements': [['table', 'instance', '(?P<instance>.*)', 'vrf', NotExists('(?P<vrf>.*)')]],
                              'kwargs': {
                                  'attributes': ['table', 'info']
                              },
                              'exclude':
                              bgp_exclude + [
                                  'label_allocation_mode', 'vpnv4 unicast',
                                  'vpnv6 unicast', 'table_version'
                              ]
                          },
                          'ops.vrf.vrf.Vrf': {
                              'requirements': [['info', 'vrfs', '(?P<vrf>.*)', NotExists('route_distinguisher')]],
                              'kwargs': {
                                  'attributes': ['info']
                              },
                              'exclude': ['maker']
                          }
                      },
                      num_values={
                          'vrf': 'all',
                          'instance': 1,
                          'address_family': 'all',
                          'rd': 1,
                      })
