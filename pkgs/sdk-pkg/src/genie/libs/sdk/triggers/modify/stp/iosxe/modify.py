'''IOSXE Implementation for spanning tree modify triggers'''

# import python
import logging
from functools import partial

# import ATS
from ats.log.utils import banner
from ats.utils.objects import find, R

# import genie.libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify
from genie.libs.sdk.libs.utils.normalize import GroupKeys


# Which key to exclude for STP Ops comparison
stp_exclude = ['maker', 'bpdu_sent', 'time_since_topology_change',
               'bpdu_received', 'forward_transitions', 'topology_changes']

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets', 'in_errors',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts','bandwidth','duplex_mode',
                     '(Tunnel.*)']

log = logging.getLogger(__name__)


def _verify_finds_root_interface(ops, requirements, **kwargs):
    '''Triggers in this file specified verify method. This is to check only 1 interface
    change to root after change the priority to highest
    '''
    log.info(banner("check only One interface change to root for each vlan"))
    ret = find([ops], R(requirements), filter_=False)
    if not ret:
        raise Exception('There is no Root interfaces after changing the priority')
    group_keys = GroupKeys.group_keys(reqs=[requirements], ret_num={}, source=ret)

    vlan_dict = {}
    for item in group_keys:
        vlan_dict.setdefault(item['vlan'], {}).setdefault(item['interface'], {})

    for vlan in vlan_dict:
        if len(vlan_dict[vlan].keys()) != 1:
            raise Exception('Expect ONE Root interface for vlan {v} but got {i}'
                .format(v=vlan, i=list(vlan_dict[vlan].keys())))
        else:
            log.info('Find ONE ROOT interface {i} for vlan {v}'
                .format(i=list(vlan_dict[vlan].keys())[0], v=vlan))

class TriggerModifyPvstDesgToRoot(TriggerModify):
    """Modify and revert the priority for dynamically learned 
    PVST Desg Forwarding instance to make it to Root."""

    __description__ = """Modify and revert the priority for dynamically learned 
    PVST Desg Forwarding instance to make it to Root

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
        1. Learn STP Ops object and store the PVST Desg FWD instance if has any,
           otherwise SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the priority of the learned STP instance priority from step 1 to
           the highest value with STP Conf object, to make this instance as Root
        4. Verify the priority of the learned PVST Desg instance from step 3
           changes to the modified value in step 3,
           verify the role of the learned instance change from "Desg" to "Root"
        5. Recover the device configurations to the one in step 2
        6. Learn STP Ops again and verify it is the same as the Ops in step 1

    """
    # check only 1 interface change to root    
    REQ = ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
           'interfaces', '(?P<interface>.*)', 'role', 'root']

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify

    mapping = Mapping(requirements={'ops.stp.stp.Stp': {
                                       'requirements':[['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'role', 'designated'],
                                                       ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'port_state', 'forwarding']],
                                       'kwargs':{'attributes':['info[pvst][(.*)][vlans][(.*)]']},
                                       'exclude': stp_exclude + ['designated_root_address', 'designated_cost', 'root_cost']}},
                      config_info={'conf.stp.Stp':{
                                     'requirements':[['device_attr', '{uut}', 'mode_attr',
                                                      'pvst', 'pvst_attr', '(?P<pvst_name>.*)',
                                                      'vlan_attr', '(?P<vlan>.*)', 'v_bridge_priority', 61440]],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.stp.stp.Stp':{
                                    'requirements':[['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'configured_bridge_priority', 61440],
                                                    ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'bridge_priority', 61440],
                                                    ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'designated_root_priority', '(\d+)'],
                                                    ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'designated_bridge_priority', '(\d+)'], 
                                                    ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'designated_root_priority', '(\d+)'],
                                                    ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'role', '(alternate|designated|root)'], 
                                                    ['info', 'pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'port_state', '(blocking|forwarding)'], 
                                                    [partial(_verify_finds_root_interface, requirements=REQ)], 
                                                    ],
                                    'kwargs':{'attributes':['info[pvst][(.*)][vlans][(.*)]']},
                                    'exclude': stp_exclude + ['designated_root_address', 'designated_cost',
                                                              'root_cost', 'designated_bridge_address', 'root_port']}},
                      num_values={'pvst_name': 1, 'interface': 'all', 'vlan': 1})


class TriggerModifyRapidPvstDesgToRoot(TriggerModify):
    """Modify and revert the priority for dynamically learned 
    Rapid-PVST Desg Forwarding instance to make it to Root."""

    __description__ = """Modify and revert the priority for dynamically learned 
    Rapid-PVST Desg Forwarding instance to make it to Root

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
        1. Learn STP Ops object and store the Rapid-PVST Desg FWD instance if has any,
           otherwise SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the priority of the learned STP instance priority from step 1 to
           the highest value with STP Conf object, to make this instance as Root
        4. Verify the priority of the learned Rapid-PVST Desg instance from step 3
           changes to the modified value in step 3,
           verify the role of the learned instance change from "Desg" to "Root"
        5. Recover the device configurations to the one in step 2
        6. Learn STP Ops again and verify it is the same as the Ops in step 1

    """
    # check only 1 interface change to root    
    REQ = ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
           'interfaces', '(?P<interface>.*)', 'role', 'root']

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.stp.stp.Stp': {
                                      'requirements':[['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'role', 'designated'],
                                                       ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'port_state', 'forwarding']],
                                       'kwargs':{'attributes':['info[rapid_pvst][(.*)][vlans][(.*)]']},
                                       'exclude': stp_exclude + ['designated_root_address', 'designated_cost', 'root_cost']}},
                      config_info={'conf.stp.Stp':{
                                     'requirements':[['device_attr', '{uut}', 'mode_attr',
                                                      'rapid-pvst', 'pvst_attr', '(?P<pvst_name>.*)',
                                                      'vlan_attr', '(?P<vlan>.*)', 'v_bridge_priority', 61440]],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.stp.stp.Stp':{
                                    'requirements':[['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'configured_bridge_priority', 61440],
                                                    ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'bridge_priority', 61440],
                                                    ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'designated_root_priority', '(\d+)'],
                                                    ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'designated_bridge_priority', '(\d+)'], 
                                                    ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'designated_root_priority', '(\d+)'],
                                                    ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'role', '(alternate|designated|root)'], 
                                                    ['info', 'rapid_pvst', '(?P<pvst_name>.*)', 'vlans', '(?P<vlan>.*)',
                                                     'interfaces', '(?P<interface>.*)', 'port_state', '(blocking|forwarding)'], 
                                                    [partial(_verify_finds_root_interface, requirements=REQ)], 
                                                    ],
                                    'kwargs':{'attributes':['info[rapid_pvst][(.*)][vlans][(.*)]']},
                                    'exclude': stp_exclude + ['designated_root_address', 'designated_cost',
                                                              'root_cost', 'designated_bridge_address', 'root_port']}},
                      num_values={'pvst_name': 1, 'interface': 'all', 'vlan': 2})
