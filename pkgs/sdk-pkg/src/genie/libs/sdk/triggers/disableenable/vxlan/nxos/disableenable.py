'''NXOS implementation for Vxlan disable/enable triggers'''

# import python
import time

from ats import aetest
# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.disableenable.disableenable import \
                                      TriggerDisableEnable

# Which key to exclude Ops comparison
vxlan_exclude = ['maker','uptime','up_time']

multisite_exclude = ['elapsedtime','keepalive','remoteport',
                     'keepaliverecvd','keepalivesent','lastread','lastwrite',
                     'msgrecvd','msgsent','neighbortableversion',
                     'tableversion','rtrefreshsent','updatesrecvd','updatessent',
                     'bytessent','bytesrecvd','localport','connsdropped',
                     'connsestablished','opensrecvd','openssent','prefixversion','fd']


class TriggerDisableEnableNveOverlay(TriggerDisableEnable):
    """Disable and enable feature nv overlay when it is enabled."""

    __description__ = """Disable and enable feature nv overlay when it is enabled.

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
        1. Learn Vxlan Ops object and verify if nv overlay is enabled, if not, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable nv overlay feature with command "no feature nve overlay"
           via Vxlan Conf object
        4. Verify the state of feature nv overlay is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature nv overlay is "enabled" and
           learn Vxlan Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', 'enabled_nv_overlay', True]],
                                                        'kwargs': {'attributes': ['nve','l2route']},
                                                        'all_keys': True,
                                                        'exclude': vxlan_exclude + ['tx_id','peer_id']}},
                    config_info={'conf.vxlan.Vxlan': {
                                    'requirements': [['device_attr', '{uut}', 'enabled_nv_overlay', True]],
                                    'verify_conf': False}},
                    verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                    'requirements': [['nve', 'enabled_nv_overlay', False]],
                                    'kwargs': {'attributes': ['nve','l2route']},
                                    'exclude': vxlan_exclude + ['l2route']}},
                    num_values={})

    feature_name = 'nve'

class TriggerDisableEnableVnSegmentVlanWithNvOverlay(TriggerDisableEnable):
    """Disable and enable feature vn Segment vlan when it is enabled."""

    __description__ = """Disable and enable feature vn Segment vlan when it is enabled.

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
        1. Learn Vxlan Ops object and verify if vn segment vlan is enabled, if not, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable vn segment vlan feature with these two commands "no feature nv overlay" and
            "no feature vn-segment-vlan-based" via Vxlan Conf object
        4. Verify the state of feature vn-segment-vlan-based is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature vn-segment-vlan-based is "enabled" and
           learn Vxlan Ops again and verify it is the same as the Ops in step 1

    """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', 'enabled_vn_segment_vlan_based', True]],
                                        'kwargs': {'attributes': ['nve','l2route','bgp_l2vpn_evpn']},
                                        'exclude': vxlan_exclude + multisite_exclude + ['tx_id','peer_id','flags','pathnr',
                                                                    'bestpathnr','totalpaths','prefix','advertisedto','resettime','resetreason']}},
                    config_info={'conf.vxlan.Vxlan': {
                                    'requirements': [['device_attr', '{uut}', 'enabled_vn_segment_vlan_based', True]],
                                    'verify_conf': False}},
                    verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                    'requirements': [['nve', 'enabled_vn_segment_vlan_based', False]],
                                    'kwargs': {'attributes': ['nve','l2route','bgp_l2vpn_evpn']},
                                    'exclude': vxlan_exclude + ['l2route','bgp_l2vpn_evpn']}},
                    num_values={})

    feature_name = 'vnseg_vlan'
