'''NXOS implementation for bgp disable/enable triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.disableenable.disableenable import \
                                      TriggerDisableEnable


# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'capability',
               'keepalives', 'total', 'total_bytes', 'up_time', 'last_reset',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'distance_internal_as', 'distance_extern_as', 'totals',
               'reset_reason', 'holdtime', 'keepalive_interval']


class TriggerDisableEnableBgp(TriggerDisableEnable):
    """Disable and enable feature BGP when there is bgp instance(s)."""
    
    __description__ = """Disable and enable feature BGP when there is bgp instance(s).

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

                instance: `str`
                bgp_id: `int`

              (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable BGP feature with command "no feature bgp"
           via BGP Conf object
        4. Verify the state of feature hsrp is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature hsrp is "enabled" and
           learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'bgp_id', '(?P<bgp_id>.*)']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'enabled', True]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'bgp_session_transport', 'connection', 'state',
                                                   '(^[I|i]dle.*|^[A|a]ctive.*|^[0-9].*)'],
                                                    ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'bgp_session_transport', 'session_state',
                                                   '(^[I|i]dle.*|^[A|a]ctive.*|^[0-9].*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'instance':1, 'bgp_id':1})
    # feature name
    # used for creating checkpoint name and log information
    feature_name = 'bgp'

