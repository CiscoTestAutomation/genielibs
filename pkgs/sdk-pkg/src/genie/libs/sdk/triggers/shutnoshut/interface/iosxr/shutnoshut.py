'''IOSXR Implementation for interface shutnoshut triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut

# Which key to exclude for BGP Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'accounting']

## IOSXR TriggerShutNoShutTrunkInterface implemented seperately since it
## doesn't need port_channel_member = False as in NXOS.


class TriggerShutNoShutTrunkInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned interface(s) when switchport mode is trunk."""

    __description__ = """Shut and unshut the dynamically learned interface(s) when switchport mode is trunk.

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
           1. Learn Interface Ops object and store the "up" interface(s)
              if has any, otherwise, SKIP the trigger, then check the switchport mode to be "trunk"
              if not, SKIP the trigger
           2. Shut the learned interface(s) from step 1 with Interface Conf object
           3. Verify the state of learned interface(s) from step 2 is "down"
           4. Unshut the interface(s) with Interface Conf object
           5. Learn Interface Ops again and verify it is the same as the Ops in step 1

       """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'switchport_mode', 'trunk'],
                                                       ['info', '(?P<interface>.*)', 'enabled', True],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude}},
                      num_values={'interface': 1})
