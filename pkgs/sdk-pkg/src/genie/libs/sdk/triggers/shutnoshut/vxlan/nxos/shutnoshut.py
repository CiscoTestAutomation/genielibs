'''Nxos Implementation for Vxlan shutnoshut triggers'''

# ats
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut

# Which key to exclude for Vlan Ops comparison

interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'accounting']

multisite_exclude = ['elapsedtime','keepalive',
                     'keepaliverecvd','keepalivesent','lastread','lastwrite',
                     'msgrecvd','msgsent','neighbortableversion',
                     'tableversion','rtrefreshsent','updatesrecvd','updatessent',
                     'bytessent','bytesrecvd','localport','remoteport','connsdropped',
                     'connsestablished','fd','opensrecvd','openssent','prefixversion',
                     'bestpathnr','pathnr','advertisedto','tx_id','bytesattrs','memoryused','prefixreceived']

nve_exclude = ['maker', 'uptime','up_time']
l2route_exclude = ['total_memory','memory']

class TriggerShutNoShutNveOverlayInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Nve onverlay interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Nve onverlay interface(s).

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

    steps:
        1. Learn VxLan Ops object and verify if has any "up" Nve interface(s),
           otherwise, SKIP the trigger
        2. Shut the learned Nve interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Nve interface(s) from step 2 is "down"
        4. Unshut the Nve interface(s) with Interface Conf object
        5. Learn VxLan Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<name>.*)', 'if_state', 'up']],
                                                'kwargs': {'attributes': [
                                                                'nve[(.*)][if_state]',
                                                                'nve[(.*)][vni][(.*)][vni]','l2route']},
                                                'exclude': nve_exclude + ['peer_id','tx_id','total_memory','mac','prefix',
                                                                          'memory','objects','total_mem','total_obj']}},
                    config_info={'conf.interface.Interface': {
                                                'requirements': [['enabled', False]],
                                                'verify_conf': False,
                                                'kwargs': {'mandatory': {'name': '(?P<name>.*)',
                                                                         'attach': False}}}},
                    verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<name>.*)', 'if_state', 'down']],
                                                'kwargs': {'attributes': [
                                                    'nve[(.*)][if_state]',
                                                    'nve[(.*)][vni][(.*)][vni]','l2route']},
                                                'exclude': nve_exclude + ['l2route']}},
                    num_values={'name': 1})


class TriggerShutNoShutNveLoopbackInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Nve loopback interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Nve loopback interface(s).

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

    steps:
        1. Learn VxLan Ops object and verify if has any "up" Nve interface(s),
           otherwise, SKIP the trigger
        2. Shut the learned Nve interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Nve interface(s) from step 2 is "down"
        4. Unshut the Nve interface(s) with Interface Conf object
        5. Learn VxLan Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [[['nve', '(?P<nve_name>.*)', 'src_if_state', 'up']],
                                                         [['nve', '(?P<nve_name>.*)', 'source_if', '(?P<source_if>loopback.*)']]],
                                        'all_keys': True,
                                        'kwargs': {'attributes': ['nve', 'l2route', 'bgp_l2vpn_evpn']},
                                        'exclude': nve_exclude + multisite_exclude + l2route_exclude + ['peer_id','resetreason','resettime','totalpaths']}},
                    config_info={'conf.interface.Interface': {
                                        'requirements': [['enabled', False]],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<source_if>.*)',
                                                                 'attach': False}}}},
                    verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'src_if_state', 'down'],
                                                         ['nve', '(?P<nve_name>.*)', 'if_state', 'down'],
                                                         ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if_oper_state',
                                                          'down'],
                                                         ['nve', '(?P<nve_name>.*)', 'sm_state', 'nve-intf-init'],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(.*)', 'vni_state',
                                                          'down'],
                                                         ['nve', 'vni', 'summary', 'cp_vni_up', 0]],
                                        'kwargs': {'attributes': ['nve', 'l2route', 'bgp_l2vpn_evpn']},
                                        'exclude': nve_exclude + ['l2route', 'bgp_l2vpn_evpn','cp_vni_down'] }},
                    num_values={'nve_name': 'all', 'source_if': 1})