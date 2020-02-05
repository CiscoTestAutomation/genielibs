'''Implementation for vxlan unconfigconfig triggers'''

import re
import logging
# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from pyats.utils.objects import Not,NotExists
from pyats import aetest
from collections import OrderedDict

# Which key to exclude for Vxlan Ops comparison
vxlan_base_exclude = ['maker','up_time']
evpn_exclude =['bytesrecvd','bytesent','elapsedtime','keepalive','tableversion',
               'keepaliverecvd','keepalivesent','lastread','totalnetworks',
               'lastwrite','msgrecvd','msgsent','updatesrecvd','rtrefreshsent',
               'totalpaths','numberattrs','updatesent','neighbortableversion',
               'memoryused','byteattrs','bytessent','updatessent', 'openssent']

interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts']

multisite_exclude = ['elapsedtime','keepalive','remoteport',
                     'keepaliverecvd','keepalivesent','lastread','lastwrite',
                     'msgrecvd','msgsent','neighbortableversion',
                     'tableversion','rtrefreshsent','updatesrecvd','updatessent',
                     'bytessent','bytesrecvd','localport','connsdropped',
                     'connsestablished','opensrecvd','openssent','prefixversion']

l2vpn_exclude = ['bytesattrs','memoryused','numberattrs','bestpathnr','totalnetworks','totalpaths','total_memory','prefixreceived']


class TriggerUnconfigConfigEvpn(TriggerUnconfigConfig):
    """Unconfigure evpn and reapply the whole configurations of dynamically learned Vxlan(s)."""
    
    __description__ = """Unconfigure evpn and reapply the whole configurations of dynamically learned Vxlan(s).

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
                address_family: `str`
                rd: `str`
                rd_vniid: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Vxlan Ops object and store the vni id under bgp_l2vpn_evpn
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the Evpn with Vxlan Conf object
        4. Verify the evpn from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan':{
                                        'requirements': [['bgp_l2vpn_evpn', 'instance', '(?P<instance>.*)','vrf',
                                                      '(?P<vrf>.*)', 'address_family', '(?P<address_family>.*)','rd','(?P<rd>.*)',
                                                      'rd_vniid','(?P<rd_vniid>.*)']],
                                        'kwargs': {'attributes': ['bgp_l2vpn_evpn']},
                                        'all_keys': True,
                                        'exclude': vxlan_base_exclude + evpn_exclude + ['prefixversion','pathnr','bestpathnr',
                                                                                        'advertisedto','prefix'] }},
                      config_info={'conf.vxlan.Vxlan':{
                                        'requirements':[['device_attr', '{uut}', 'evpn_attr','(.*)']],
                                        'verify_conf':False,
                                        'kwargs':{}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                        'requirements': [['bgp_l2vpn_evpn', 'instance', '(.*)']],
                                        'kwargs': {'attributes': ['bgp_l2vpn_evpn']},
                                        'exclude': vxlan_base_exclude + evpn_exclude }},
                      num_values={'instance':1 , 'vrf':1 , 'address_family':1 , 'rd':1})


class TriggerUnconfigConfigEvpnVni(TriggerUnconfigConfig):
    """Unconfigure evpn vni and reapply the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure evpn and reapply the whole configurations of dynamically learned Vxlan(s).

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

                    nve_name: `str`
                    nve_vni: `str`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                         OR
                         interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn Vxlan Ops object and store the vni state under nve
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the Evpn with Vxlan Conf object
            4. Verify the evpn from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1

        """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',
                                                                  'vni_state', 'up']],
                                                'kwargs': {'attributes': ['nve']},
                                                'all_keys':True,
                                                'exclude': vxlan_base_exclude + ['uptime']}},
                      config_info={'conf.interface.Interface': {
                                                'requirements': [['nve_vni','(?P<nve_vni>.*)']],
                                                'verify_conf': False,
                                                'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)','attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)', 'vni', NotExists('(?P<nve_vni>.*)')]],
                                                'kwargs': {'attributes': ['nve']},
                                                'exclude': vxlan_base_exclude +['uptime','active_vnis','cp_vni_up','cp_vni_count']}},
                      num_values={'nve_name': 1, 'nve_vni': 1})


class TriggerUnconfigConfigEvpnMsiteBgwDelayRestoreTime(TriggerUnconfigConfig):
    """Unconfigure evpn msite bgw delay restore time and reapply
        the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure evpn msite bgw delay restore time and reapply
                        the whole configurations of dynamically learned Vxlan(s).

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

                nve_name: `str`
                evpn_multisite_border_gateway: `int`
                delay_restore_time: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Vxlan Ops object and store the evpn msite bgw delay restore time under nve
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the evpn msite bgw delay restore time with Vxlan Conf object
        4. Verify the evpn msite bgw delay restore time from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [[['nve', 'evpn_multisite_border_gateway', '(?P<evpn_multisite_border_gateway>.*)']],
                                                                 [['nve', '(?P<nve_name>.*)','multisite_convergence_time',
                                                                  '(?P<delay_restore_time>.*)']]],
                                                'kwargs': {'attributes': ['nve']},
                                                'exclude': vxlan_base_exclude + ['uptime','prefixversion','pathnr','bestpathnr']}},
                      config_info={'conf.vxlan.Vxlan': {
                                                'requirements': [['device_attr','{uut}', 'evpn_msite_attr', '(?P<evpn_multisite_border_gateway>.*)',\
                                                                  'evpn_msite_bgw_delay_restore_time', '(?P<delay_restore_time>.*)']],
                                                'verify_conf': False,
                                                'kwargs': {}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)', 'multisite_convergence_time', 180]],
                                                'kwargs': {'attributes': ['nve']},
                                                'exclude': vxlan_base_exclude + ['uptime']}},
                      num_values={'nve_name': 1,'evpn_multisite_border_gateway': 1})


class TriggerUnconfigConfigEvpnMsiteDciTracking(TriggerUnconfigConfig):
    """Unconfigure evpn msite dci tracking and reapply
            the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure evpn msite dci tracking and reapply
                            the whole configurations of dynamically learned Vxlan(s).

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

                    nve_name: `str`
                    dci_link: `str`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                         OR
                         interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn Vxlan Ops object and store the evpn msite dci tracking under nve
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the evpn msite dci tracking with Interface Conf object
            4. Verify the evpn msite dci tracking from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
        """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [[['nve', 'multisite', 'dci_links', '(?P<dci_link>.*)', 'if_state', 'up']],
                                                                 [['nve', '(?P<nve_name>.*)',\
                                                                  'multisite_bgw_if_oper_state', 'up']]],
                                                'kwargs': {'attributes': ['nve[(.*)][vni][(.*)][vni]',
                                                                          'nve[(.*)][multisite_bgw_if_oper_state]',
                                                                          'nve[multisite]']},
                                                'exclude': vxlan_base_exclude}},
                      config_info={'conf.interface.Interface': {
                                                'requirements': [['evpn_multisite_dci_tracking',True]],
                                                'verify_conf': False,
                                                'kwargs': {'mandatory': {'name': '(?P<dci_link>.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve','multisite', NotExists('dci_links')],
                                                                 ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if_oper_state', 'down']],
                                                'kwargs': {'attributes': ['nve[(.*)][vni][(.*)][vni]',
                                                                          'nve[(.*)][multisite_bgw_if_oper_state]',
                                                                          'nve[multisite]']},
                                                'exclude': vxlan_base_exclude}},
                      num_values={'dci_link': 'all','nve_name': 1 })

class TriggerUnconfigConfigEvpnMsiteFabricTracking(TriggerUnconfigConfig):
    """Unconfigure evpn msite fabric tracking and reapply
                the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure evpn msite Fabric tracking and reapply
                                the whole configurations of dynamically learned Vxlan(s).

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

                nve_name: `str`
                fabric_link: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Vxlan Ops object and store the evpn msite fabric tracking under nve
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the evpn msite fabric tracking with Interface Conf object
        4. Verify the evpn msite fabric tracking from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [[['nve', 'multisite', 'fabric_links', '(?P<fabric_link>.*)', 'if_state', 'up']],
                                                                 [['nve', '(?P<nve_name>.*)', \
                                                                   'multisite_bgw_if_oper_state', 'up']]],
                                                'kwargs': {'attributes': ['nve[(.*)][vni][(.*)][vni]',
                                                                          'nve[(.*)][multisite_bgw_if_oper_state]',
                                                                          'nve[multisite]',
                                                                          'bgp_l2vpn_evpn']},
                                                'exclude': vxlan_base_exclude + multisite_exclude +['fd','resetreason','resettime','prefixreceived',
                                                                                                    'bestpathnr','pathnr','advertisedto']}},
                      config_info={'conf.interface.Interface': {
                                                'requirements': [['evpn_multisite_fabric_tracking',True]],
                                                'verify_conf': False,
                                                'kwargs': {'mandatory': {'name': '(?P<fabric_link>.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve','multisite',NotExists('fabric_links')],
                                                                ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if_oper_state', 'down']],
                                                'kwargs': {'attributes': ['nve[(.*)][vni][(.*)][vni]',
                                                                          'nve[(.*)][multisite_bgw_if_oper_state]',
                                                                          'nve[multisite]',
                                                                          'bgp_l2vpn_evpn']},
                                                'exclude': vxlan_base_exclude +['bgp_l2vpn_evpn']}},
                      num_values={'fabric_link': 'all', 'nve_name': 1})

class TriggerUnconfigConfigNveAdvertiseVirtualRmac(TriggerUnconfigConfig):
    """Unconfigure virtual rmac advertised and reapply
       the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure virtual rmac advertised and reapply
                          the whole configurations of dynamically learned Vxlan(s).

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

                nve_name: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Vxlan Ops object and store the virtual rmac advertised under nve
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the virtual rmac advertised with Interface Conf object
        4. Verify the virtual rmac advertised from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)','if_state','up'],
                                                                 ['nve','(?P<nve_name>.*)','adv_vmac',True]],
                                                'kwargs': {'attributes': ['nve[(.*)][adv_vmac]',
                                                                          'nve[(.*)][if_state]',
                                                                          'nve[(.*)][vni]','l2route','bgp_l2vpn_evpn']},
                                                'all_keys':True,
                                                'exclude': vxlan_base_exclude + multisite_exclude + l2vpn_exclude +\
                                                           ['peer_id','tx_id','client_nfn','prefixversion']}},
                      config_info={'conf.interface.Interface': {
                                                'requirements': [['nve_adv_virtual_rmac', True]],
                                                'verify_conf': False,
                                                'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)','if_state','up'],
                                                                 ['nve','(?P<nve_name>.*)','adv_vmac',False]],
                                                'kwargs': {'attributes': ['nve[(.*)][adv_vmac]',
                                                                          'nve[(.*)][if_state]',
                                                                          'nve[(.*)][vni]','l2route','bgp_l2vpn_evpn']},
                                                'exclude': vxlan_base_exclude + ['l2route','bgp_l2vpn_evpn']}},
                      num_values={'nve_name': 1})

class TriggerUnconfigConfigNveVniAssociateVrf(TriggerUnconfigConfig):
    """Unconfigure nvi associated vrf and reapply
         the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure nvi associated vrf and reapply
                          the whole configurations of dynamically learned Vxlan(s).

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

              nve_name: `str`
              nve_vni: `str`

              (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)
    steps:
      1. Learn Vxlan Ops object and store the nvi associated vrf under nve
         if has any, otherwise, SKIP the trigger
      2. Save the current device configurations through "method" which user uses
      3. Unconfigure the nvi associated vrf with Interface Conf object
      4. Verify the nvi associated vrf from step 3 are no longer existed
      5. Recover the device configurations to the one in step 2
      6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
    """

    # associated vrf is shown as L3
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)','vni','(?P<nve_vni>.*)',\
                                                                  'type','(?P<type>L3.*)']],
                                                'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]']},
                                                'all_keys':True,
                                                'exclude': vxlan_base_exclude }},
                      config_info={'conf.interface.Interface': {
                                                'requirements': [['nve_vni','(?P<nve_vni>.*)']],
                                                'verify_conf': False,
                                                'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)','vni', NotExists('(?P<nve_vni>.*)')]],
                                                'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]']},
                                                'exclude': vxlan_base_exclude}},
                      num_values={'nve_name': 1, 'nve_vni':1})

class TriggerUnconfigConfigNveSourceInterfaceLoopback(TriggerUnconfigConfig):
    """Unconfigure nve source interface and reapply the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure nve source interface and reapply the whole configurations of dynamically learned Vxlan(s).

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

                  nve_name: `str`
                  source_if: `str`

                  (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                        OR
                        interface: 'Ethernet1/1/1' (Specific value)
       steps:
         1. Learn Vxlan Ops object and store the nve source interface under nve
            if has any, otherwise, SKIP the trigger
         2. Save the current device configurations through "method" which user uses
         3. Unconfigure the nve source interface with Interface Conf object
         4. Verify the nve source interface from step 3 are no longer existed
         5. Recover the device configurations to the one in step 2
         6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
       """

    @aetest.test
    def unconfigure(self, uut, abstract, steps):

        cmd = "interface (?P<nve_name>.*)\n" \
              " shutdown\n" \
              " no source-interface (?P<source_if>.*)"
        x = re.findall(r'\S+|\n', cmd)
        req = self.mapping._path_population([x], uut)
        req_str = []
        for item in req[0]:
            req_str.append(str(item))

        cmd = ' '.join(req_str)
        try:
            uut.configure(cmd)
        except Exception as e:
            self.failed("Unable to configure: '{c}'".format(c=cmd),
                        from_exception=e)

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)', 'source_if', '(?P<source_if>(L|l)oopback.*)'],
                                                                 ['nve', '(?P<nve_name>.*)', 'src_if_state', 'up']],
                                                'kwargs': {'attributes': ['nve[(.*)][vni][(.*)][vni]',
                                                                          'nve[(.*)][source_if]',
                                                                          'nve[(.*)][src_if_state]']},
                                                'all_keys':True,
                                                'exclude': vxlan_base_exclude}},
                      config_info={'conf.interface.Interface': {
                                                'requirements': [],
                                                'verify_conf': False,
                                                'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                                'requirements': [['nve', '(?P<nve_name>.*)', NotExists('source_if')]],
                                                'kwargs': {'attributes':  ['nve[(.*)][vni][(.*)][vni]',
                                                                          'nve[(.*)][source_if]',
                                                                          'nve[(.*)][src_if_state]']},
                                                'exclude': vxlan_base_exclude}},
                      num_values={'nve_name': 1, 'source_if': 1})

class TriggerUnconfigConfigNvOverlayEvpn(TriggerUnconfigConfig):
    """Unconfigure nv overlay evpn and reapply the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure nv overlay evpn and reapply the whole configurations of dynamically learned Vxlan(s).

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
            address_family: `str`
            rd: `str`
            rd_vniid: `str`

            (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                  OR
                  interface: 'Ethernet1/1/1' (Specific value)
    steps:
    1. Learn Vxlan Ops object and store the vni id under bgp_l2vpn_evpn
       if has any, otherwise, SKIP the trigger
    2. Save the current device configurations through "method" which user uses
    3. Unconfigure the nv overlay evpn interface with Vxlan Conf object
    4. Verify the nv overlay evpn from step 3 are no longer existed
    5. Recover the device configurations to the one in step 2
    6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                            'requirements': [['bgp_l2vpn_evpn', 'instance', '(?P<instance>.*)', 'vrf',
                                                          '(?P<vrf>.*)', 'address_family', '(?P<address_family>.*)', 'rd', '(?P<rd>.*)',
                                                          'rd_vniid', '(?P<rd_vniid>.*)']],
                                            'kwargs': {'attributes': ['bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)]'
                                                                      '[address_family][(.*)][rd]','l2route']},
                                            'all_keys': True,
                                            'exclude': vxlan_base_exclude + ['sent_to','prefixversion','pathnr',
                                                                             'bestpathnr','advertisedto','client_nfn',
                                                                             'prefix','memory','objects','total_mem',
                                                                             'total_obj','total_memory','mac','mac_ip','seq_num']}},
                        config_info={'conf.vxlan.Vxlan': {
                                            'requirements': [['device_attr', '{uut}', 'enabled_nv_overlay_evpn', True]],
                                            'verify_conf': False,
                                            'kwargs': {}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                            'requirements': [[NotExists('bgp_l2vpn_evpn'), '']],
                                            'kwargs': {'attributes': ['bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)][address_family][(.*)][rd]','l2route']},
                                            'exclude': vxlan_base_exclude +['bgp_l2vpn_evpn','l2route']}},
                        num_values={'instance': 1, 'vrf': 1, 'address_family': 1, 'rd': 'all','rd_vniid': 'all'})

class TriggerUnconfigConfigNveVniMcastGroup(TriggerUnconfigConfig):
    """Unconfigure mcast group and reapply the whole configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure mcast group and reapply the whole configurations of dynamically learned Vxlan(s).

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

            nve_name: `str`
            nve_vni: `str`
            mcast: `str`

            (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                  OR
                  interface: 'Ethernet1/1/1' (Specific value)
    steps:
    1. Learn Vxlan Ops object and store the mcast group under nve
       if has any, otherwise, SKIP the trigger
    2. Save the current device configurations through "method" which user uses
    3. Unconfigure the mcast group with Interface Conf object
    4. Verify the mcast from step 3 are no longer existed
    5. Recover the device configurations to the one in step 2
    6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan':{
                                         'requirements':[['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'mcast', '(?P<mcast>.*)'],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'vni_state', 'up'],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'type', '(?P<type>L2.*)']],
                                         'kwargs':{'attributes':['nve[(.*)][vni]']},
                                         'all_keys': True,
                                         'exclude': vxlan_base_exclude}},
                        config_info={'conf.interface.Interface': {
                                        'requirements': [['nve_vni','(?P<nve_vni>.*)'],
                                                         ['nve_vni_mcast_group','(?P<mcast>.*)'],
                                                         ['nve_vni_associate_vrf',False]],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                         'requirements':[['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'mcast', 'unconfigured'],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'vni_state', 'down'],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', NotExists('repl_ip')]],
                                         'kwargs':{'attributes':['nve[(.*)][vni]']},
                                         'all_keys': True,
                                         'exclude': vxlan_base_exclude}},
                      num_values={'nve_name':1 , 'nve_vni':1 , 'mcast':1})

class TriggerUnconfigConfigNveVniMultisiteIngressReplication(TriggerUnconfigConfig):
    """Unconfig multisite ingress replication under vxlan and then restore the
            configuration by reapplying the whole running configuration"""

    __description__ = """Add multisite ingress replication under Vxlan then restore the
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
                   static:
                        The keys below are dynamically learnt by default.
                        However, they can also be set to a custom value when provided in the trigger datafile.

                        nve_name: `str`
                        nve_vni: `str`

                        (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                              OR
                              interface: 'Ethernet1/1/1' (Specific value)
           Steps:
               1. Learn Vxlan Ops configured on device. SKIP the trigger if there
                  is no vxlan configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add multisite ingress replication that using Genie Vxlan Conf.
               4. Verify the newly multisite ingress replication under Vxlan is reflected in
                  device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1.
                   """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',\
                                                          'multisite_ingress_replication',True],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'associated_vrf', False]],
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]']},
                                        'all_keys': True,
                                        'exclude': vxlan_base_exclude}},
                        config_info={'conf.interface.Interface': {
                                        'requirements': [['nve_vni','(?P<nve_vni>.*)'],
                                                         ['nve_vni_multisite_ingress_replication',True],
                                                         ['nve_vni_associate_vrf',False]],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'vni','(?P<nve_vni>.*)',\
                                                          NotExists('multisite_ingress_replication')]],
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]']},
                                        'exclude': vxlan_base_exclude}},
                        num_values={'nve_name': 1 ,'nve_vni':1 })

class TriggerUnconfigConfigEvpnMsiteBgw(TriggerUnconfigConfig):
    """Unconfigure evpn msite bgw and reapply the whole
        configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure evpn msite bgw and reapply the whole configurations of
                        dynamically learned Vxlan(s).

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

                evpn_multisite_border_gateway: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
      steps:
        1. Learn Vxlan Ops object and store the evpn msite bgw under nve
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the evpn msite bgw with Vxlan Conf object
        4. Verify the evpn msite bgw from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
      """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', 'evpn_multisite_border_gateway', '(?P<evpn_multisite_border_gateway>.*)']],
                                        'kwargs': {'attributes': ['nve','l2route']},
                                        'all_keys': True,
                                        'exclude': vxlan_base_exclude + ['uptime','peer_id','tx_id','flags']}},
                        config_info={'conf.vxlan.Vxlan': {
                                        'requirements': [['device_attr', '{uut}', 'evpn_msite_attr', '(?P<evpn_multisite_border_gateway>.*)']],
                                        'verify_conf': False,
                                        'kwargs': {}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', NotExists('evpn_multisite_border_gateway')]],
                                        'kwargs': {'attributes': ['nve','l2route']},
                                        'exclude': vxlan_base_exclude + ['l2route','uptime']}},
                        num_values={'evpn_multisite_border_gateway': 1 })


class TriggerUnconfigConfigNveMultisiteBgwInterface(TriggerUnconfigConfig):
    """Unconfigure multisite bgw interface and reapply the whole
            configurations of dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure multisite bgw interface and reapply the whole configurations of
                            dynamically learned Vxlan(s).

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

                    nve_name: `str`
                    multisite_bgw_if: `str`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                          OR
                          interface: 'Ethernet1/1/1' (Specific value)
          steps:
            1. Learn Vxlan Ops object and store the multisite bgw interface under nve.
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the multisite bgw interface with Vxlan Conf object
            4. Verify the multisite bgw interface from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
          """

    requirements = OrderedDict()
    requirements['ops.vxlan.vxlan.Vxlan'] = {
                        'requirements': [['nve', '(?P<nve_name>.*)', 'multisite_bgw_if',
                                          '(?P<multisite_bgw_if>.*)']],
                        'kwargs': {'attributes': ['nve']},
                        'exclude': vxlan_base_exclude + interface_exclude}

    requirements['ops.interface.interface.Interface'] = {
        'requirements': [['info', '(?P<multisite_bgw_if>(L|l)oopback.*)', 'oper_status', 'up']],
        'kwargs': {'attributes': ['info']},
        'exclude': vxlan_base_exclude + interface_exclude}

    mapping = Mapping(requirements=requirements,
                        config_info={'conf.interface.Interface': {
                                            'requirements': [['nve_multisite_bgw_intf', '(?P<multisite_bgw_if>.*)']],
                                            'verify_conf': False,
                                            'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                            'requirements': [['nve', '(?P<nve_name>.*)', NotExists('multisite_bgw_if')]],
                                            'kwargs': {'attributes': ['nve']},
                                            'exclude': vxlan_base_exclude + interface_exclude }},
                        num_values={'nve_name':1, 'multisite_bgw_if': 1 })
