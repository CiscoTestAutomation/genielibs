'''NXOS Implementation for BGP addremove triggers'''

# python
import re
import logging
from functools import partial

log = logging.getLogger(__name__)

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.libs.utils.triggeractions import Configure
from genie.libs.sdk.libs.utils.mapping import Mapping, Different
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove

# ATS
from ats import aetest
from ats.utils.objects import NotExists ,Not
from ipaddress import IPv4Address

# ipaddress
from ipaddress import IPv4Address, IPv6Address

# Which keys to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'capability',
               'keepalives', 'total', 'total_bytes', 'up_time', 'last_reset',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'distance_internal_as', 'distance_extern_as', 'totals',
               'reset_reason', 'holdtime', 'keepalive_interval']

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'bandwidth', 'load_interval',
                     'port_speed', 'in_crc_errors', 'in_errors',
                     'in_discards', '(Tunnel.*)', 'accounting']

bgp_exclude_keepalive = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'last_reset',
               'keepalives', 'total', 'total_bytes', 'up_time',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'route_reflector_client', 'capability',
               'distance_internal_as', 'bgp_neighbor_counters', 'memory_usage',
               'total_entries', 'routing_table_version', 'total_memory',
               'path', 'prefixes', 'cluster_id']
ospf_exclude = ['maker', 'age', 'checksum', 'seq_num',
                'hello_timer', 'dead_timer']


class TriggerAddRemoveBgpNeighborUpdateSource(TriggerAddRemove):
    """Add update source configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add update source configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add update source configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added update source config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', NotExists('update_source')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'ops.interface.interface.Interface':{
                        'requirements':[\
                            ['info', '(?P<intf_name>(Loopback|loopback)[0-9]+)', 'vrf', '(?P<vrf>.*)'],
                            ['info', '(?P<intf_name>(Loopback|loopback)[0-9]+)', 'enabled', True],
                            ['info', '(?P<intf_name>(Loopback|loopback)[0-9]+)', 'oper_status', 'up']],
                        'exclude': interface_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_update_source', '(?P<intf_name>(Loopback|loopback)[0-9]+)']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'update_source', '(?P<intf_name>(Loopback|loopback)[0-9]+)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1, 'intf_name':1})


class TriggerAddRemoveBgpNeighborDescription(TriggerAddRemove):
    """Add description configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add description configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add description configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added description config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', NotExists('description')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_description', 'test']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'description', 'test']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerAddRemoveBgpNeighborDisableConnectedCheck(TriggerAddRemove):
    """Add connected-check configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add connected-check configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add connected-check configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added connected-check config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', NotExists('disable_connected_check')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'ebgp_multihop', True],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_disable_connected_check', True]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'disable_connected_check', True]],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerAddRemoveBgpNeighborBfd(TriggerAddRemove):
    """Add bfd configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add bfd configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add bfd configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added bfd config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', NotExists('fall_over_bfd')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
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
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'fall_over_bfd', True]],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerAddRemoveBgpNeighborMaximumPrefix(TriggerAddRemove):
    """Add maximum-prefix configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add maximum-prefix configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add maximum-prefix configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added maximum-prefix config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', NotExists('maximum_prefix_max_prefix_no')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'address_family_attr', '(?P<address_family>.*)', 'nbr_af_maximum_prefix_max_prefix_no', 163]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'maximum_prefix_max_prefix_no', 163],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerAddRemoveBgpNeighborNextHopSelf(TriggerAddRemove):
    """Add next-hop self configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add next-hop self configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add next-hop self configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added next-hop self config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>^(?!l2vpn|vpnv|.*mvpn).*)', '(?P<af>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', NotExists('next_hop_self')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
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
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'next_hop_self', True]],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1, 'address_family':1})


class TriggerAddRemoveBgpNeighborDefaultOriginate(TriggerAddRemove):
    """Add default originate configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add default originate configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add default originate configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added default originate config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>^(?!l2vpn|vpnv|.*mvpn).*)', '(?P<af>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', NotExists('default_originate')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
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
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'default_originate', True]],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1, 'address_family':1})


class TriggerAddRemoveBgpNeighborPassword(TriggerAddRemove):
    """Add password configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add password configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add password configuration under BGP neighbor of BGP  pid 
           learned in step 1 using Genie BGP Conf.
        4. Verify the newly added password config under BGP neighbor is 
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    @aetest.test
    def add_configuration(self, uut, abstract, steps):

        super().add_configuration(uut, abstract, steps)

        # Flap neighbor for config change to take effect
        cmd = "router bgp (?P<bgp_id>.*)\n"\
              " vrf (?P<vrf>.*)\n"\
              "  neighbor (?P<neighbor>.*)\n"\
              "   shutdown\n"\
              "   no shutdown"
        x = re.findall(r'\S+|\n', cmd)
        req = self.mapping._path_population([x], uut)
        req_str = []
        for item in req[0]:
            req_str.append(str(item))

        # combine command
        cmd = ' '.join(req_str)
        cmd = cmd.replace('vrf default \n', '')
        try:
            uut.configure(cmd)
        except Exception as e:
            self.failed("Unable to configure: '{c}'".format(c=cmd),
                        from_exception=e)

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', NotExists('password_text')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'nbr_password_text', 'asgrocks']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'idle'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'password_text', 'set (disabled)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerAddRemoveBgpNeighborTransportConnectionModePassive(TriggerAddRemove):
    """Add transport connection mode configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Add transport connection mode configuration under a BGP neighor and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration 
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config 
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the 
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is 
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Add transport connection mode configuration under BGP neighbor of BGP
           pid learned in step 1 using Genie BGP Conf.
        4. Verify the newly added transport connection mode config under BGP 
           neighbor is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'bgp_session_transport', 'connection', NotExists('mode')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True,
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
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'bgp_session_transport', 'connection', 'mode', 'passive']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerAddRemoveBgpNeighborRoutemap(TriggerAddRemove):
    """Add route-map configuration under a BGP neighbor and then restore the
         configuration by reapplying the whole running configuration"""

    __description__ = """Add route-map configuration under a BGP neighbor and then restore the
                            configuration by reapplying the whole running configuration

        trigger_datafile:
            Mandatory Arguments:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger in seconds.
                                      Default: 180
                    interval (`int`): Wait time between iteration when looping is
                                      needed in seconds. Default: 15
                    method (`str`): Method to recover the device configuration.
                                    Supported methods:
                                        'checkpoint': Rollback the configuration
                                                      using checkpoint (nxos),
                                                      archive file (iosxe),
                                                      load the saved running-config
                                                      file on disk (iosxr)
            Optional Arguments:
                tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                     restored to the reference rate in seconds.
                                     Default: 60
                tgn_delay (`int`): Wait time between each poll to verify if traffic
                                   is resumed in seconds. Default: 10
                timeout_recovery:
                    Buffer recovery timeout make sure devices are recovered at the
                    end of the trigger execution. Used when previous timeouts have
                    been exhausted.
                    max_time (`int`): Maximum wait time for the last step of the
                                      trigger in seconds. Default: 180
                    interval (`int`): Wait time between iteration when looping is
                                      needed in seconds. Default: 15

        Steps:
            1. Learn BGP Ops configured on device. SKIP the trigger if there
               is no BGP configured on the device.
            2. Save the current device configurations using "method" specified.
            3. Add route-map in and route-map out configuration under a BGP neighbor of BGP pid learned in
               step 1 using Genie BGP Conf.
            4. Verify the newly route-maps under BGP neighbor is reflected in
               device configuration.
            5. Restore the device configuration to the original configuration saved
               in step 2.
            6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
        """

    mapping = Mapping(requirements={\
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'address_family', '(?P<af>.*)', NotExists('route_map_name_in')],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'address_family', '(?P<af>.*)', NotExists('route_map_name_out')],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                'all_keys':True, 
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude},
            'ops.route_policy.route_policy.RoutePolicy': {
                'requirements': [ \
                    ['info', '(?P<policy>.*)', 'statements', '(?P<statements>.*)']],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}
        },
        config_info={ \
            'conf.bgp.Bgp': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)',
                     'address_family_attr','(?P<af>.*)','nbr_af_route_map_name_in','(?P<policy>.*)'],
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)',
                     'address_family_attr', '(?P<af>.*)', 'nbr_af_route_map_name_out', '(?P<policy>.*)']
                ],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={ \
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'address_family','(?P<af>.*)','route_map_name_in','(?P<policy>.*)'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'address_family', '(?P<af>.*)', 'route_map_name_out', '(?P<policy>.*)']
                ],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}},
        num_values={'instance': 1, 'vrf': 1, 'neighbor': 1,'statements':1,'policy':1 })


class TriggerAddRemoveBgpNeighborCapabilitySuppress4ByteAs(TriggerAddRemove):
    """Add capability suppress 4-byte-as configuration under a BGP neighbor and then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add capability suppress 4-byte-as under a BGP neighbor and then restore the
                           configuration by reapplying the whole running configuration

           trigger_datafile:
               Mandatory Arguments:
                   timeout:
                       max_time (`int`): Maximum wait time for the trigger in seconds.
                                         Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15
                       method (`str`): Method to recover the device configuration.
                                       Supported methods:
                                           'checkpoint': Rollback the configuration
                                                         using checkpoint (nxos),
                                                         archive file (iosxe),
                                                         load the saved running-config
                                                         file on disk (iosxr)
               Optional Arguments:
                   tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                        restored to the reference rate in seconds.
                                        Default: 60
                   tgn_delay (`int`): Wait time between each poll to verify if traffic
                                      is resumed in seconds. Default: 10
                   timeout_recovery:
                       Buffer recovery timeout make sure devices are recovered at the
                       end of the trigger execution. Used when previous timeouts have
                       been exhausted.
                       max_time (`int`): Maximum wait time for the last step of the
                                         trigger in seconds. Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15

           Steps:
               1. Learn BGP Ops configured on device. SKIP the trigger if there
                  is no BGP configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add capability suppress 4-byte-as under a BGP neighbor of BGP pid learned in
                  step 1 using Genie BGP Conf.
               4. Verify the newly capability suppress 4-byte-as under BGP neighbor is reflected in
                  device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
           """

    mapping = Mapping(requirements={ \
        'ops.bgp.bgp.Bgp': {
            'requirements': [ \
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                  NotExists('suppress_four_byte_as_capability')],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'session_state', 'established'],
                ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
            'all_keys':True, 
            'kwargs': {'attributes': ['info']},
            'exclude': bgp_exclude}},
        config_info={ \
            'conf.bgp.Bgp': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)',
                     'nbr_suppress_four_byte_as_capability', True]],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={ \
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'suppress_four_byte_as_capability', True]],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}},
        num_values={'instance': 1, 'vrf': 1, 'neighbor': 1})


class TriggerAddRemoveBgpNeighborSendCommunity(TriggerAddRemove):
    """Add send-community configuration under a BGP neighbor and then restore the
                configuration by reapplying the whole running configuration"""

    __description__ = """Add send-community under a BGP neighbor and then restore the
                       configuration by reapplying the whole running configuration

               trigger_datafile:
                   Mandatory Arguments:
                       timeout:
                           max_time (`int`): Maximum wait time for the trigger in seconds.
                                             Default: 180
                           interval (`int`): Wait time between iteration when looping is
                                             needed in seconds. Default: 15
                           method (`str`): Method to recover the device configuration.
                                           Supported methods:
                                               'checkpoint': Rollback the configuration
                                                             using checkpoint (nxos),
                                                             archive file (iosxe),
                                                             load the saved running-config
                                                             file on disk (iosxr)
                   Optional Arguments:
                       tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                            restored to the reference rate in seconds.
                                            Default: 60
                       tgn_delay (`int`): Wait time between each poll to verify if traffic
                                          is resumed in seconds. Default: 10
                       timeout_recovery:
                           Buffer recovery timeout make sure devices are recovered at the
                           end of the trigger execution. Used when previous timeouts have
                           been exhausted.
                           max_time (`int`): Maximum wait time for the last step of the
                                             trigger in seconds. Default: 180
                           interval (`int`): Wait time between iteration when looping is
                                             needed in seconds. Default: 15

               Steps:
                   1. Learn BGP Ops configured on device. SKIP the trigger if there
                      is no BGP configured on the device.
                   2. Save the current device configurations using "method" specified.
                   3. Add send-community under a BGP neighbor of BGP pid learned in
                      step 1 using Genie BGP Conf.
                   4. Verify the newly send-community under BGP neighbor is reflected in
                      device configuration.
                   5. Restore the device configuration to the original configuration saved
                      in step 2.
                   6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
               """
    mapping = Mapping(requirements={ \
        'ops.bgp.bgp.Bgp': {
            'requirements': [ \
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'address_family', '(?P<af>.*)',NotExists('send_community')],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'session_state', 'established'],
                ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
            'all_keys':True, 
            'kwargs': {'attributes': ['info']},
            'exclude': bgp_exclude}},
        config_info={ \
            'conf.bgp.Bgp': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)',
                     'address_family_attr', '(?P<af>.*)','nbr_af_send_community', 'standard']],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={ \
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'address_family', '(?P<af>.*)', 'send_community', 'standard']],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}},
        num_values={'instance': 1, 'vrf': 1, 'neighbor': 1, 'af':1})


class TriggerAddRemoveBgpNeighborSendCommunityExtended(TriggerAddRemove):
    """Add send-community extended configuration under a BGP neighbor and then restore the
                  configuration by reapplying the whole running configuration"""

    __description__ = """Add send-community extended under a BGP neighbor and then restore the
                         configuration by reapplying the whole running configuration

                 trigger_datafile:
                     Mandatory Arguments:
                         timeout:
                             max_time (`int`): Maximum wait time for the trigger in seconds.
                                               Default: 180
                             interval (`int`): Wait time between iteration when looping is
                                               needed in seconds. Default: 15
                             method (`str`): Method to recover the device configuration.
                                             Supported methods:
                                                 'checkpoint': Rollback the configuration
                                                               using checkpoint (nxos),
                                                               archive file (iosxe),
                                                               load the saved running-config
                                                               file on disk (iosxr)
                     Optional Arguments:
                         tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                              restored to the reference rate in seconds.
                                              Default: 60
                         tgn_delay (`int`): Wait time between each poll to verify if traffic
                                            is resumed in seconds. Default: 10
                         timeout_recovery:
                             Buffer recovery timeout make sure devices are recovered at the
                             end of the trigger execution. Used when previous timeouts have
                             been exhausted.
                             max_time (`int`): Maximum wait time for the last step of the
                                               trigger in seconds. Default: 180
                             interval (`int`): Wait time between iteration when looping is
                                               needed in seconds. Default: 15

                 Steps:
                     1. Learn BGP Ops configured on device. SKIP the trigger if there
                        is no BGP configured on the device.
                     2. Save the current device configurations using "method" specified.
                     3. Add send-community extended under a BGP neighbor of BGP pid learned in
                        step 1 using Genie BGP Conf.
                     4. Verify the newly send-community extended under BGP neighbor is reflected in
                        device configuration.
                     5. Restore the device configuration to the original configuration saved
                        in step 2.
                     6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
                 """
    mapping = Mapping(requirements={ \
        'ops.bgp.bgp.Bgp': {
            'requirements': [ \
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'address_family', '(?P<af>.*)',NotExists('send_community')],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'session_state', 'established'],
                ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
            'all_keys':True, 
            'kwargs': {'attributes': ['info']},
            'exclude': bgp_exclude}},
        config_info={ \
            'conf.bgp.Bgp': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)',
                     'address_family_attr', '(?P<af>.*)','nbr_af_send_community', 'extended']],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={ \
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'address_family', '(?P<af>.*)', 'send_community', 'extended']],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}},
        num_values={'instance': 1, 'vrf': 1, 'neighbor': 1 , 'af':1})


class TriggerAddRemoveBgpNeighborSoftReconfiguration(TriggerAddRemove):
    """Add soft-reconfiguration inbound under a BGP neighbor and then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add soft-reconfiguration inbound under BGP neighbor and then restore the
                             configuration by reapplying the whole running configuration

                     trigger_datafile:
                         Mandatory Arguments:
                             timeout:
                                 max_time (`int`): Maximum wait time for the trigger in seconds.
                                                   Default: 180
                                 interval (`int`): Wait time between iteration when looping is
                                                   needed in seconds. Default: 15
                                 method (`str`): Method to recover the device configuration.
                                                 Supported methods:
                                                     'checkpoint': Rollback the configuration
                                                                   using checkpoint (nxos),
                                                                   archive file (iosxe),
                                                                   load the saved running-config
                                                                   file on disk (iosxr)
                         Optional Arguments:
                             tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                                  restored to the reference rate in seconds.
                                                  Default: 60
                             tgn_delay (`int`): Wait time between each poll to verify if traffic
                                                is resumed in seconds. Default: 10
                             timeout_recovery:
                                 Buffer recovery timeout make sure devices are recovered at the
                                 end of the trigger execution. Used when previous timeouts have
                                 been exhausted.
                                 max_time (`int`): Maximum wait time for the last step of the
                                                   trigger in seconds. Default: 180
                                 interval (`int`): Wait time between iteration when looping is
                                                   needed in seconds. Default: 15

                     Steps:
                         1. Learn BGP Ops configured on device. SKIP the trigger if there
                            is no BGP configured on the device.
                         2. Save the current device configurations using "method" specified.
                         3. Add soft-reconfiguration inbound under BGP neighbor of BGP pid learned in
                            step 1 using Genie BGP Conf.
                         4. Verify the newly soft-reconfiguration inbound under BGP neighbor is reflected in
                            device configuration.
                         5. Restore the device configuration to the original configuration saved
                            in step 2.
                         6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
                     """
    mapping = Mapping(requirements={ \
        'ops.bgp.bgp.Bgp': {
            'requirements': [ \
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'address_family', '(?P<af>.*)', NotExists('soft_configuration')],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'session_state', 'established'],
                ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
            'all_keys':True, 
            'kwargs': {'attributes': ['info']},
            'exclude': bgp_exclude}},
        config_info={ \
            'conf.bgp.Bgp': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)',
                     'address_family_attr', '(?P<af>.*)', 'nbr_af_soft_reconfiguration', True]],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={ \
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'address_family', '(?P<af>.*)', 'soft_configuration', True]],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}},
        num_values={'instance': 1, 'vrf': 1, 'neighbor': 1 ,'af':1})


class TriggerAddRemoveBgpNeighborRemovePrivateAs(TriggerAddRemove):
    """Add remove-private-as configuration under a BGP neighbor and then restore the
           configuration by reapplying the whole running configuration"""

    __description__ = """Add remove-private-as configuration under a BGP neighbor and then restore the
          configuration by reapplying the whole running configuration

          trigger_datafile:
              Mandatory Arguments:
                  timeout:
                      max_time (`int`): Maximum wait time for the trigger in seconds.
                                        Default: 180
                      interval (`int`): Wait time between iteration when looping is
                                        needed in seconds. Default: 15
                      method (`str`): Method to recover the device configuration.
                                      Supported methods:
                                          'checkpoint': Rollback the configuration
                                                        using checkpoint (nxos),
                                                        archive file (iosxe),
                                                        load the saved running-config
                                                        file on disk (iosxr)
              Optional Arguments:
                  tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                       restored to the reference rate in seconds.
                                       Default: 60
                  tgn_delay (`int`): Wait time between each poll to verify if traffic
                                     is resumed in seconds. Default: 10
                  timeout_recovery:
                      Buffer recovery timeout make sure devices are recovered at the
                      end of the trigger execution. Used when previous timeouts have
                      been exhausted.
                      max_time (`int`): Maximum wait time for the last step of the
                                        trigger in seconds. Default: 180
                      interval (`int`): Wait time between iteration when looping is
                                        needed in seconds. Default: 15

          Steps:
              1. Learn BGP Ops configured on device. SKIP the trigger if there
                 is no BGP configured on the device.
              2. Save the current device configurations using "method" specified.
              3. Add remove-private-as configuration under a BGP neighbor of BGP pid learned in
                 step 1 using Genie BGP Conf.
              4. Verify the newly remove-private-as under BGP is reflected in device configuration.
              5. Restore the device configuration to the original configuration saved
                 in step 2.
              6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
          """

    mapping = Mapping(requirements={ \
        'ops.bgp.bgp.Bgp': {
            'requirements': [ \
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                  NotExists('remove_private_as')],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'remote_as',Not(100)],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'session_state', 'established'],
                ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
            'all_keys':True, 
            'kwargs': {'attributes': ['info']},
            'exclude': bgp_exclude}},
        config_info={ \
            'conf.bgp.Bgp': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)',
                      'nbr_remove_private_as', True]],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={ \
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'remove_private_as', True]],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}},
        num_values={'instance': 1, 'vrf': 1, 'neighbor': 1})


class TriggerAddRemoveBgpAggregateAddressIpv4(TriggerAddRemove):
    """Add aggregate-address configuration for ipv4 under a BGP and then restore the
           configuration by reapplying the whole running configuration"""

    __description__ = """Add aggregate-address configuration for ipv4 under a BGP and then restore the
          configuration by reapplying the whole running configuration

          trigger_datafile:
              Mandatory Arguments:
                  timeout:
                      max_time (`int`): Maximum wait time for the trigger in seconds.
                                        Default: 180
                      interval (`int`): Wait time between iteration when looping is
                                        needed in seconds. Default: 15
                      method (`str`): Method to recover the device configuration.
                                      Supported methods:
                                          'checkpoint': Rollback the configuration
                                                        using checkpoint (nxos),
                                                        archive file (iosxe),
                                                        load the saved running-config
                                                        file on disk (iosxr)
              Optional Arguments:
                  tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                       restored to the reference rate in seconds.
                                       Default: 60
                  tgn_delay (`int`): Wait time between each poll to verify if traffic
                                     is resumed in seconds. Default: 10
                  timeout_recovery:
                      Buffer recovery timeout make sure devices are recovered at the
                      end of the trigger execution. Used when previous timeouts have
                      been exhausted.
                      max_time (`int`): Maximum wait time for the last step of the
                                        trigger in seconds. Default: 180
                      interval (`int`): Wait time between iteration when looping is
                                        needed in seconds. Default: 15

          Steps:
              1. Learn BGP Ops configured on device. SKIP the trigger if there
                 is no BGP configured on the device.
              2. Save the current device configurations using "method" specified.
              3. Add aggregate-address configuration for ipv4 under BGP pid learned in
                 step 1 using Genie BGP Conf.
              4. Verify the newly aggregate-address under BGP is reflected in device
                 configuration.
              5. Restore the device configuration to the original configuration saved
                 in step 2.
              6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
          """

    mapping = Mapping(requirements={ \
        'ops.bgp.bgp.Bgp': {
            'requirements': [ \
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family','(?P<af>^(ipv4)[\w ]+)',
                 NotExists('aggregate_address_ipv4_address')],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>^(ipv4)[\w ]+)',
                 NotExists('aggregate_address_ipv4_mask')],
                ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                 'session_state', 'established'],
                ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
            'all_keys':True, 
            'kwargs': {'attributes': ['info']},
            'exclude': bgp_exclude}},
        config_info={ \
            'conf.bgp.Bgp': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr', '(?P<af>^(ipv4)[\w ]+)',
                     'af_aggregate_address_ipv4_address', '83.0.0.0'],
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr', '(?P<af>^(ipv4)[\w ]+)',
                     'af_aggregate_address_ipv4_mask', '16']
                ],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={ \
            'ops.bgp.bgp.Bgp': {
                'requirements': [ \
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                     'session_state', 'established'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>^(ipv4)[\w ]+)',
                     'aggregate_address_ipv4_address', '83.0.0.0'],
                    ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>^(ipv4)[\w ]+)',
                     'aggregate_address_ipv4_mask', '16'],
                ],
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude}},
        num_values={'instance': 1, 'vrf': 1, 'neighbor': 1 ,'af':1})


class TriggerAddRemoveBgpAggregateAddressIpv6(TriggerAddRemove):
    """Add aggregate-address configuration for ipv6 under a BGP and then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add aggregate-address configuration for ipv6 under a BGP and then restore the
               configuration by reapplying the whole running configuration

               trigger_datafile:
                   Mandatory Arguments:
                       timeout:
                           max_time (`int`): Maximum wait time for the trigger in seconds.
                                             Default: 180
                           interval (`int`): Wait time between iteration when looping is
                                             needed in seconds. Default: 15
                           method (`str`): Method to recover the device configuration.
                                           Supported methods:
                                               'checkpoint': Rollback the configuration
                                                             using checkpoint (nxos),
                                                             archive file (iosxe),
                                                             load the saved running-config
                                                             file on disk (iosxr)
                   Optional Arguments:
                       tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                            restored to the reference rate in seconds.
                                            Default: 60
                       tgn_delay (`int`): Wait time between each poll to verify if traffic
                                          is resumed in seconds. Default: 10
                       timeout_recovery:
                           Buffer recovery timeout make sure devices are recovered at the
                           end of the trigger execution. Used when previous timeouts have
                           been exhausted.
                           max_time (`int`): Maximum wait time for the last step of the
                                             trigger in seconds. Default: 180
                           interval (`int`): Wait time between iteration when looping is
                                             needed in seconds. Default: 15

               Steps:
                   1. Learn BGP Ops configured on device. SKIP the trigger if there
                      is no BGP configured on the device.
                   2. Save the current device configurations using "method" specified.
                   3. Add aggregate-address configuration for ipv6 under BGP pid learned in
                      step 1 using Genie BGP Conf.
                   4. Verify the newly aggregate-address under BGP is reflected in
                      device configuration.
                   5. Restore the device configuration to the original configuration saved
                      in step 2.
                   6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
               """

    mapping = Mapping(\
                requirements={ \
                    'ops.bgp.bgp.Bgp': {
                        'requirements': [\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>(ipv6 u).*)', NotExists('v6_aggregate_address_ipv6_address')],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True,
                        'kwargs': {'attributes': ['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp': {
                        'requirements': [\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr', '(?P<af>.*)', 'af_v6_aggregate_address_ipv6_address', '2000::/8']],
                        'verify_conf': False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp': {
                        'requirements': [\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>.*)', 'v6_aggregate_address_ipv6_address', '2000::/8']],
                        'kwargs': {'attributes': ['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance': 1, 'vrf': 1, 'neighbor': 1, 'af': 1})


class TriggerAddRemoveBgpKeepaliveHoldtime(TriggerAddRemove):
    """Add keepalive interval and holdtime configuration under a BGP and then restore the
            configuration by reapplying the whole running configuration"""

    __description__ = """Add keepalive interval and holdtime under BGP and then restore the
                   configuration by reapplying the whole running configuration

           trigger_datafile:
               Mandatory Arguments:
                   timeout:
                       max_time (`int`): Maximum wait time for the trigger in seconds.
                                         Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15
                       method (`str`): Method to recover the device configuration.
                                       Supported methods:
                                           'checkpoint': Rollback the configuration
                                                         using checkpoint (nxos),
                                                         archive file (iosxe),
                                                         load the saved running-config
                                                         file on disk (iosxr)
               Optional Arguments:
                   tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                        restored to the reference rate in seconds.
                                        Default: 60
                   tgn_delay (`int`): Wait time between each poll to verify if traffic
                                      is resumed in seconds. Default: 10
                   timeout_recovery:
                       Buffer recovery timeout make sure devices are recovered at the
                       end of the trigger execution. Used when previous timeouts have
                       been exhausted.
                       max_time (`int`): Maximum wait time for the last step of the
                                         trigger in seconds. Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15

           Steps:
               1. Learn BGP Ops configured on device. SKIP the trigger if there
                  is no BGP configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add keepalive interval and holdtime under BGP pid learned in
                  step 1 using Genie BGP Conf.
               4. Verify the newly keepalive interval and holdtime under BGP is reflected in
                  device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
           """

    mapping = Mapping(\
            requirements={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        [['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', NotExists('keepalive_interval')]],
                        [['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', NotExists('holdtime')]]],
                    'exclude': bgp_exclude_keepalive},
                'ops.bgp.bgp.Bgp': {
                    'requirements': [\
                        ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                    'all_keys':True,
                    'kwargs': {'attributes': ['info']},
                    'exclude': bgp_exclude_keepalive}},
            config_info={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'keepalive_interval', 10],
                        ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'holdtime', 30]],
                    'verify_conf': False,
                    'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
            verify_ops={\
                'conf.bgp.Bgp': {
                    'requirements': [\
                        ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'keepalive_interval',10],
                        ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'holdtime', 30]],
                    'exclude': bgp_exclude_keepalive}},
            num_values={'device': 1, 'bgp_id': 1, 'vrf': 1, 'instance': 1, 'neighbor':1})


class TriggerAddRemoveBgpNetworkIPv4(TriggerAddRemove):
    """Add network ip configuration under a BGP and then restore the
           configuration by reapplying the whole running configuration"""

    __description__ = """Add network ip under a BGP and then restore the
           configuration by reapplying the whole running configuration

           trigger_datafile:
               Mandatory Arguments:
                   timeout:
                       max_time (`int`): Maximum wait time for the trigger in seconds.
                                         Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15
                       method (`str`): Method to recover the device configuration.
                                       Supported methods:
                                           'checkpoint': Rollback the configuration
                                                         using checkpoint (nxos),
                                                         archive file (iosxe),
                                                         load the saved running-config
                                                         file on disk (iosxr)
               Optional Arguments:
                   tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                        restored to the reference rate in seconds.
                                        Default: 60
                   tgn_delay (`int`): Wait time between each poll to verify if traffic
                                      is resumed in seconds. Default: 10
                   timeout_recovery:
                       Buffer recovery timeout make sure devices are recovered at the
                       end of the trigger execution. Used when previous timeouts have
                       been exhausted.
                       max_time (`int`): Maximum wait time for the last step of the
                                         trigger in seconds. Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15

           Steps:
               1. Learn BGP Ops configured on device. SKIP the trigger if there
                  is no BGP configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add network ip configuration under BGP pid learned in
                  step 1 using Genie BGP Conf.
               4. Verify the newly network ip under BGP is
                  reflected in device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
           """

    mapping = Mapping(\
        requirements={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr', '(?P<af>^(ipv4)[\w ]+)', NotExists('af_network_number')]],
                'exclude': bgp_exclude_keepalive},
            'ops.bgp.bgp.Bgp': {
                'requirements': [\
                    ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                'all_keys':True, 
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude_keepalive}},
        config_info={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr','(?P<af>.*)', 'af_network_number', IPv4Address('34.34.34.0')],
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr','(?P<af>.*)', 'af_network_mask', 24]],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr', '(?P<af>.*)', 'af_network_number', '34.34.34.0'],
                    ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr', '(?P<af>.*)', 'af_network_mask', 24]],
                'exclude': bgp_exclude_keepalive}},
        num_values={'device': 1, 'bgp_id': 1, 'vrf': 1, 'instance': 1, 'af': 1})


class TriggerAddRemoveBgpNetworkIPv6(TriggerAddRemove):
    """Add network ipv6 configuration under a BGP and then restore the
           configuration by reapplying the whole running configuration"""

    __description__ = """Add network ipv6 under a BGP and then restore the
           configuration by reapplying the whole running configuration

           trigger_datafile:
               Mandatory Arguments:
                   timeout:
                       max_time (`int`): Maximum wait time for the trigger in seconds.
                                         Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15
                       method (`str`): Method to recover the device configuration.
                                       Supported methods:
                                           'checkpoint': Rollback the configuration
                                                         using checkpoint (nxos),
                                                         archive file (iosxe),
                                                         load the saved running-config
                                                         file on disk (iosxr)
               Optional Arguments:
                   tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                        restored to the reference rate in seconds.
                                        Default: 60
                   tgn_delay (`int`): Wait time between each poll to verify if traffic
                                      is resumed in seconds. Default: 10
                   timeout_recovery:
                       Buffer recovery timeout make sure devices are recovered at the
                       end of the trigger execution. Used when previous timeouts have
                       been exhausted.
                       max_time (`int`): Maximum wait time for the last step of the
                                         trigger in seconds. Default: 180
                       interval (`int`): Wait time between iteration when looping is
                                         needed in seconds. Default: 15

           Steps:
               1. Learn BGP Ops configured on device. SKIP the trigger if there
                  is no BGP configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add network ipv6 configuration under BGP pid learned in
                  step 1 using Genie BGP Conf.
               4. Verify the newly network ipv6 under BGP is
                  reflected in device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
           """

    mapping = Mapping(\
        requirements={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr',
                     '(?P<af>(AddressFamily.)(ipv6|ipv6[\S]+)(.*))', NotExists('af_v6_network_number')]],
                'exclude': bgp_exclude_keepalive},
            'ops.bgp.bgp.Bgp': {
                'requirements': [\
                    ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                'all_keys':True,
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude_keepalive}},
        config_info={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr','(?P<af>.*)',
                     'af_v6_network_number', '2000::/8']],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr',
                     '(?P<af>.*)', 'af_v6_network_number', '2000::/8']],
                'exclude': bgp_exclude_keepalive}},
        num_values={'device': 1, 'bgp_id': 1, 'vrf': 1, 'instance': 1, 'af': 1})


class TriggerAddRemoveBgpMaximumPathsEbgp(TriggerAddRemove):
    """Add maximum ebgp paths configuration under a BGP and then restore the
       configuration by reapplying the whole running configuration"""

    __description__ = """Add maximum ebgp paths under a BGP and then restore the
       configuration by reapplying the whole running configuration

       trigger_datafile:
           Mandatory Arguments:
               timeout:
                   max_time (`int`): Maximum wait time for the trigger in seconds.
                                     Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15
                   method (`str`): Method to recover the device configuration.
                                   Supported methods:
                                       'checkpoint': Rollback the configuration
                                                     using checkpoint (nxos),
                                                     archive file (iosxe),
                                                     load the saved running-config
                                                     file on disk (iosxr)
           Optional Arguments:
               tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                    restored to the reference rate in seconds.
                                    Default: 60
               tgn_delay (`int`): Wait time between each poll to verify if traffic
                                  is resumed in seconds. Default: 10
               timeout_recovery:
                   Buffer recovery timeout make sure devices are recovered at the
                   end of the trigger execution. Used when previous timeouts have
                   been exhausted.
                   max_time (`int`): Maximum wait time for the last step of the
                                     trigger in seconds. Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15

       Steps:
           1. Learn BGP Ops configured on device. SKIP the trigger if there
              is no BGP configured on the device.
           2. Save the current device configurations using "method" specified.
           3. Add maximum ebgp paths configuration under BGP pid learned in
              step 1 using Genie BGP Conf.
           4. Verify the newly maximum ebgp paths under BGP is
              reflected in device configuration.
           5. Restore the device configuration to the original configuration saved
              in step 2.
           6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
       """
    mapping = Mapping(\
        requirements={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)','_address_family_attr', '(?P<af>(AddressFamily.)(.*))', NotExists('af_maximum_paths_ebgp')]],
                'exclude': bgp_exclude_keepalive},
            'ops.bgp.bgp.Bgp': {
                'requirements': [\
                    ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                'all_keys':True, 
                'kwargs': {'attributes': ['info']},
                'exclude': bgp_exclude_keepalive}},
        config_info={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)','address_family_attr','(?P<af>.*)', 'af_maximum_paths_ebgp', 8]],
                'verify_conf': False,
                'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
        verify_ops={\
            'conf.bgp.Bgp': {
                'requirements': [\
                    ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)','_address_family_attr', '(?P<af>.*)', 'af_maximum_paths_ebgp', 8]],
                'exclude': bgp_exclude_keepalive}},
        num_values={'device': 1, 'bgp_id': 1, 'vrf': 1, 'instance': 1, 'af': 1})


class TriggerAddRemoveBgpNeighborAsOverride(TriggerAddRemove):
    """Apply the "as-override" to the dynamically learned BGP neighbor(s)
    which does not have "as-override" enabled, and remove the"""

    __description__ = """Apply the "as-override" to the dynamically learned BGP neighbor(s)
    which does not have "as-override" enabled, and remove the
    added "as-override" configurations.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP neighbor(s) if it does 
           not have "as-override" enabled,
           otherwise, SKIP the trigger.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of the "as-override" to learned
           BGP neighbor(s) from step 1 with BGP Conf object
        4. Verify the BGP neighbor(s) from step 3 has "as-override" configured
        5. Remove the "as-override" configurations from the learned
           BGP neighbor(s) from step 1
        6. Recover the device configurations to the one in step 2
        7. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'address_family',
                                                           '(?P<address_family>.*)',
                                                           NotExists('as_override')],
                                                          ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>^(?!default).*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'remote_as', Different('(?P<bgp_id>.*)')]],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr',
                                                      '(?P<vrf>.*)', 'neighbor_attr',
                                                      '(?P<neighbor>.*)', 'address_family_attr',
                                                      '(?P<address_family>^(?!vpnv).*)',
                                                      'nbr_af_as_override', True]
                                                    ],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                     'vrf', '(?P<vrf>.*)', 'neighbor',
                                                     '(?P<neighbor>.*)', 'address_family',
                                                     '(?P<address_family>.*)',
                                                     'as_override', True]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf': 1, 'instance': 1, 'neighbor': 1,
                                  'address_family': 1})


class TriggerAddRemoveBgpNeighborRouteReflectorClient(TriggerAddRemove):
    """Apply the "route-reflector-client" to the dynamically learned BGP neighbor(s)
    which does not have "route-reflector-client" enabled, and remove the"""

    __description__ = """Apply the "route-reflector-client" to the dynamically learned BGP neighbor(s)
    which does not have "route-reflector-client" enabled, and remove the
    added "route-reflector-client" configurations.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP neighbor(s) if it does 
           not have "route-reflector-client" enabled,
           otherwise, SKIP the trigger.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of the "route-reflector-client" to learned
           BGP neighbor(s) from step 1 with BGP Conf object
        4. Verify the BGP neighbor(s) from step 3 has "route-reflector-client" configured
        5. Remove the "route-reflector-client" configurations from the learned
           BGP neighbor(s) from step 1
        6. Recover the device configurations to the one in step 2
        7. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'address_family',
                                                           '(?P<address_family>.*)',
                                                           NotExists('route_reflector_client')],
                                                           ['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'remote_as',
                                                           '(?P<bgp_id>.*)'],
                                                           ['info', 'instance', '(?P<instance>.*)',
                                                           'bgp_id', '(?P<bgp_id>.*)'],
                                                           ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'session_state', 'established']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr',
                                                      '(?P<vrf>.*)', 'neighbor_attr',
                                                      '(?P<neighbor>.*)', 'address_family_attr',
                                                      '(?P<address_family>.*)',
                                                      'nbr_af_route_reflector_client', True]
                                                    ],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                     'vrf', '(?P<vrf>.*)', 'neighbor',
                                                     '(?P<neighbor>.*)', 'address_family',
                                                     '(?P<address_family>.*)',
                                                     'route_reflector_client', True]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf': 1, 'instance': 1, 'neighbor': 1,
                                  'address_family': 1, 'bgp_id': 1})


class TriggerAddRemoveBgpRedistributeConnected(TriggerAddRemove):
    """Apply the "redistribute direct " to the dynamically learned BGP vrf(s)
    which does not have "redistribute direct " enabled, and remove the
    added "redistribute direct " configurations."""

    __description__ = """Apply the "redistribute direct " to the dynamically learned BGP vrf(s)
    which does not have "redistribute direct " enabled, and remove the
    added "redistribute direct " configurations.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP vrf(s) if it does 
           not have "redistribute direct" enabled,
           otherwise, SKIP the trigger.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of the "redistribute direct" to learned
           BGP vrf(s) from step 1 with BGP Conf object
        4. Verify the BGP vrf(s) from step 3 has "redistribute direct" configured
        5. Remove the "redistribute direct" configurations from the learned
           BGP vrf(s) from step 1
        6. Recover the device configurations to the one in step 2
        7. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'conf.bgp.Bgp':{
                                          'requirements':[['device_attr', '{uut}', '_vrf_attr',
                                                      '(?P<vrf>.*)', '_address_family_attr',
                                                      '(?P<address_family>^(?!vpnv).*)', NotExists('af_redist_connected')]],
                                        'exclude': bgp_exclude},
                                    'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude},
                                    'ops.route_policy.route_policy.RoutePolicy':{
                                          'requirements':[['info', '(?P<route_policy>.*)',
                                                           '(?P<route_policy_info>.*)']],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr',
                                                      '(?P<vrf>.*)', 'address_family_attr',
                                                      '(?P<address_family>^(?!vpnv).*)',
                                                      'af_redist_connected', True],
                                                      ['device_attr', '{uut}', 'vrf_attr',
                                                      '(?P<vrf>.*)', 'address_family_attr',
                                                      '(?P<address_family>^(?!vpnv).*)',
                                                      'af_redist_connected_route_policy', '(?P<route_policy>.*)']
                                                    ],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                           'bgp_id', '(?P<bgp_id>.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude},
                                  'conf.bgp.Bgp':{
                                        'requirements':[['device_attr', '{uut}', '_vrf_attr',
                                                         '(?P<vrf>.*)', '_address_family_attr',
                                                         '(?P<address_family>.*)', 'af_redist_connected', True],
                                                        ['device_attr', '{uut}', '_vrf_attr',
                                                         '(?P<vrf>.*)', '_address_family_attr',
                                                         '(?P<address_family>.*)',
                                                         'af_redist_connected_route_policy', '(?P<route_policy>.*)']],
                                      'exclude': bgp_exclude},},
                      num_values={'vrf': 1, 'instance': 'all', 
                                  'address_family': 'all', 'route_policy': 1})


class TriggerAddRemoveBgpRedistributeStatic(TriggerAddRemove):
    """Apply the "redistribute static" to the dynamically learned BGP vrf(s)
      which does not have "redistribute static" enabled, and remove the
      added "redistribute static" configurations."""

    __description__ = """Apply the "redistribute static" to the dynamically learned BGP vrf(s)
    which does not have "redistribute static" enabled, and remove the
    added "redistribute static" configurations.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP vrf(s) if it does 
           not have "redistribute static" enabled,
           otherwise, SKIP the trigger.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of the "redistribute static" to learned
           BGP vrf(s) from step 1 with BGP Conf object
        4. Verify the BGP vrf(s) from step 3 has "redistribute static" configured
        5. Remove the "redistribute static" configurations from the learned
           BGP vrf(s) from step 1
        6. Recover the device configurations to the one in step 2
        7. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'conf.bgp.Bgp':{
                                          'requirements':[['device_attr', '{uut}', '_vrf_attr',
                                                      '(?P<vrf>.*)', '_address_family_attr',
                                                      '(?P<address_family>^(?!vpnv).*)', NotExists('af_redist_static')]],
                                        'exclude': bgp_exclude},
                                    'ops.bgp.bgp.Bgp':{
                                        'requirements':[\
                                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True, 
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude},
                                    'ops.route_policy.route_policy.RoutePolicy':{
                                          'requirements':[['info', '(?P<route_policy>.*)',
                                                           '(?P<route_policy_info>.*)']],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr',
                                                      '(?P<vrf>.*)', 'address_family_attr',
                                                      '(?P<address_family>^(?!vpnv).*)',
                                                      'af_redist_static', True],
                                                      ['device_attr', '{uut}', 'vrf_attr',
                                                      '(?P<vrf>.*)', 'address_family_attr',
                                                      '(?P<address_family>^(?!vpnv).*)',
                                                      'af_redist_static_route_policy', '(?P<route_policy>.*)']
                                                    ],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                           'bgp_id', '(?P<bgp_id>.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude},
                                  'conf.bgp.Bgp':{
                                        'requirements':[['device_attr', '{uut}', '_vrf_attr',
                                                         '(?P<vrf>.*)', '_address_family_attr',
                                                         '(?P<address_family>.*)', 'af_redist_static', True],
                                                        ['device_attr', '{uut}', '_vrf_attr',
                                                         '(?P<vrf>.*)', '_address_family_attr',
                                                         '(?P<address_family>.*)',
                                                         'af_redist_static_route_policy', '(?P<route_policy>.*)']],
                                      'exclude': bgp_exclude},},
                      num_values={'vrf': 1, 'instance': 'all', 
                                  'address_family': 'all', 'route_policy': 1})


class TriggerAddRemoveBgpRedistributeOspf(TriggerAddRemove):
    """Apply the "redistribute ospf opsf_pid" to the dynamically learned BGP vrf(s)
      which does not have "redistribute ospf opsf_pid" enabled, and remove the
      added "redistribute ospf opsf_pid" configurations."""

    __description__ = """Apply the "redistribute ospf opsf_pid" to the dynamically learned BGP vrf(s)
    which does not have "redistribute ospf opsf_pid" enabled, and remove the
    added "redistribute ospf opsf_pid" configurations.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP vrf(s) if it does 
           not have "redistribute ospf opsf_pid" enabled,
           otherwise, SKIP the trigger.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of the "redistribute ospf opsf_pid" to learned
           BGP vrf(s) from step 1 with BGP Conf object
        4. Verify the BGP vrf(s) from step 3 has "redistribute ospf opsf_pid" configured
        5. Remove the "redistribute ospf opsf_pid" configurations from the learned
           BGP vrf(s) from step 1
        6. Recover the device configurations to the one in step 2
        7. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(\
                requirements={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr', '(?P<address_family>(ipv4 unicast))', NotExists('af_redist_ospf')]],
                        'exclude': bgp_exclude},
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'ops.route_policy.route_policy.RoutePolicy':{
                        'requirements':[\
                            ['info', '(?P<route_policy>.*)', '(?P<route_policy_info>.*)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'ops.ospf.ospf.Ospf':{
                        'requirements':[\
                            ['info', 'vrf', '(?P<vrf_ospf>.*)', 'address_family', '(?P<address_family_ospf>(ipv4 unicast))', 'instance', '(?P<ospf_instance>.*)', '(?P<ospf_info>.*)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': ospf_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr', '(?P<address_family>(ipv4 unicast))', 'af_redist_ospf', '(?P<ospf_instance>.*)'],
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'address_family_attr', '(?P<address_family>(ipv4 unicast))', 'af_redist_ospf_route_policy', '(?P<route_policy>.*)']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements': [\
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr', '(?P<address_family>(ipv4 unicast))', 'af_redist_ospf', '(?P<ospf_instance>.*)'],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_address_family_attr', '(?P<address_family>(ipv4 unicast))', 'af_redist_ospf_route_policy', '(?P<route_policy>.*)']],
                        'exclude': bgp_exclude},
                    'ops.ospf.ospf.Ospf':{
                        'requirements':[\
                            ['info', 'vrf', '(?P<vrf_ospf>.*)', 'address_family', '(?P<address_family_ospf>(ipv4 unicast))', 'instance', '(?P<ospf_instance>.*)', '(?P<ospf_info>.*)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': ospf_exclude}},
                num_values={'vrf': 1, 'instance': 1, 'ospf_instance': 1, 'address_family': 1, 'route_policy': 1})


class TriggerAddRemoveBgpAfL2vpnEvpnRewriteEvpnRtAsn(TriggerAddRemove):
    """Apply the "rewrite-evpn-rt-asn" to the dynamically learned BGP vrf(s)
          which does not have "rewrite-evpn-rt-asn" enabled, and remove the
          added "rewrite-evpn-rt-asn" configurations."""

    __description__ = """Apply the "rewrite-evpn-rt-asn" to the dynamically learned BGP vrf(s)
                        which does not have "rewrite-evpn-rt-asn" enabled, and remove the
                        added "rewrite-evpn-rt-asn" configurations.

        trigger_datafile:
            Mandatory:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iterations when looping is needed,
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
                    interval (`int`): Wait time between iterations when looping is needed,
                                    in second. Default: 15

        steps:
            1. Learn BGP Ops object and store the BGP vrf(s) if it does
               not have "rewrite-evpn-rt-asn" enabled,
               otherwise, SKIP the trigger.
            2. Save the current device configurations through "method" which user uses
            3. Add the configuration of the "rewrite-evpn-rt-asn" to learned
               BGP vrf(s) from step 1 with BGP Conf object
            4. Verify the BGP vrf(s) from step 3 has "rewrite-evpn-rt-asn" configured
            5. Remove the "rewrite-evpn-rt-asn" configurations from the learned
                BGP vrf(s) from step 1
            6. Recover the device configurations to the one in step 2
            7. Learn BGP Ops again and verify it is the same as the Ops in step 1

        """

    mapping = Mapping(\
                requirements={ \
                    'conf.bgp.Bgp': {
                        'requirements': [ \
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_neighbor_attr',
                              '(?P<neighbor>.*)', '_address_family_attr', '(?P<af>.*)', NotExists('nbr_af_rewrite_evpn_rt_asn')]],
                        'exclude': bgp_exclude},
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            [['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)',
                             'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>^l2vpn +evpn$)',
                             'session_state', 'established']],
                            [['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                            [['info', 'instance', '(?P<instance>.*)', 'vrf',\
                             '(?P<vrf>.*)', 'neighbor','(?P<neighbor>.*)', 'remote_as', Different('(?P<bgp_id>.*)')]]],
                        'all_keys': True,
                        'kwargs':{'attributes':['info[instance][(.*)][bgp_id]',
                                    'info[list_of_vrfs]',
                                    'info[instance][(.*)][vrf][(.*)][neighbor]'
                                       '[(.*)][address_family][(.*)][session_state]',
                                     'info[instance][(.*)][vrf][(.*)][neighbor]'
                                       '[(.*)][remote_as]']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                             'neighbor_attr', '(?P<neighbor>.*)', 'address_family_attr', '(?P<address_family>.*)',\
                             'nbr_af_rewrite_evpn_rt_asn', True]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={ \
                    'conf.bgp.Bgp': {
                        'requirements': [ \
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', '_neighbor_attr',
                             '(?P<neighbor>.*)', '_address_family_attr', '(?P<af>.*)', 'nbr_af_rewrite_evpn_rt_asn', True]],
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1 , 'address_family': 1})
