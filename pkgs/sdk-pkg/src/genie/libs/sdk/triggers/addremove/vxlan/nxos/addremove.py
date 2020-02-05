'''NXOS Implementation for Vxlan addremove triggers'''

import logging
log = logging.getLogger(__name__)

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove
from pyats import aetest
from collections import OrderedDict
from functools import partial

# ATS
from pyats.utils.objects import NotExists, Not

vxlan_exclude =['maker','up_time']
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts']

multisite_exclude = ['bytesattrs','memoryused','elapsedtime','keepalive',
                     'keepaliverecvd','keepalivesent','lastread','lastwrite',
                     'msgrecvd','msgsent','neighbortableversion',
                     'tableversion','rtrefreshsent','updatesrecvd','updatessent',
                     'bytessent','bytesrecvd','localport','remoteport','connsdropped',
                     'connsestablished','fd','opensrecvd','openssent','prefixversion',
                     'bestpathnr','pathnr','advertisedto','tx_id','total_mem']


l2route_exclude = ['total_memory','memory']
class TriggerAddRemoveNveAdvertiseVirtualRmac(TriggerAddRemove):
    """Add Virtual rmac advertised under vxlan and then restore the
            configuration by reapplying the whole running configuration"""

    __description__ = """Add msite bgw delay restore time under Vxlan then restore the
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

                        (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                              OR
                              interface: 'Ethernet1/1/1' (Specific value)
           Steps:
               1. Learn Vxlan Ops configured on device. SKIP the trigger if there
                  is no vxlan configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add virtual rmac advertised that using Genie Interface Conf.
               4. Verify the newly Virtual rmac advertised under Vxlan is reflected in
                  device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1.
                   """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'if_state', 'up'],
                                                         ['nve', '(?P<nve_name>.*)', 'adv_vmac', False]],
                                        'kwargs': {'attributes': ['nve[(.*)][adv_vmac]',
                                                                  'nve[(.*)][if_state]',
                                                                  'nve[(.*)][vni]','bgp_l2vpn_evpn','l2route']},
                                        'all_keys': True,
                                        'exclude': vxlan_exclude + multisite_exclude + l2route_exclude}},
                        config_info={'conf.interface.Interface': {
                                        'requirements': [['nve_adv_virtual_rmac', True]],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'if_state','up'],
                                                         ['nve', '(?P<nve_name>.*)', 'adv_vmac', True]],
                                        'kwargs': {'attributes': ['nve[(.*)][adv_vmac]',
                                                                  'nve[(.*)][if_state]',
                                                                  'nve[(.*)][vni]','bgp_l2vpn_evpn','l2route']},
                                        'exclude': vxlan_exclude + ['bgp_l2vpn_evpn','l2route']}},
                        num_values={'nve_name': 1})

class TriggerAddRemoveEvpnMsiteBgwDelayRestoreTime(TriggerAddRemove):
    """Add msite bgw delay restore time under vxlan and then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add msite bgw delay restore time under Vxlan then restore the
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

                       evpn_multisite_border_gateway: `int`

                       (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                             OR
                             interface: 'Ethernet1/1/1' (Specific value)
           Steps:
               1. Learn Vxlan Ops configured on device. SKIP the trigger if there
                  is no Vxlan configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add msite bgw delay restore time that using Genie Vxlan Conf.
               4. Verify the newly msite bgw delay restore time under Vxlan is reflected in
                  device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1.
           """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', 'evpn_multisite_border_gateway', '(?P<evpn_multisite_border_gateway>.*)'],
                                                         ['nve', NotExists('multisite_convergence_time'), NotExists('(.*)')]],
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]',
                                                                  'nve[evpn_multisite_border_gateway]',
                                                                  'nve[multisite_convergence_time]','bgp_l2vpn_evpn','l2route']},
                                        'all_keys': True,
                                        'exclude': vxlan_exclude + multisite_exclude + ['flags'] }},
                    config_info={'conf.vxlan.Vxlan': {
                                        'requirements': [['device_attr', '{uut}', 'evpn_msite_attr', '(?P<evpn_multisite_border_gateway>.*)',\
                                                          'evpn_msite_bgw_delay_restore_time', 30]],
                                        'verify_conf': False,
                                        'kwargs': {}}},
                    verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', 'multisite_convergence_time', 30]],
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]',
                                                                  'nve[evpn_multisite_border_gateway]',
                                                                  'nve[multisite_convergence_time]','bgp_l2vpn_evpn','l2route']},
                                        'exclude': vxlan_exclude+ ['bgp_l2vpn_evpn','l2route'] }},
                    num_values={'nve_name': 1, 'nve_vni':1 ,'evpn_multisite_border_gateway':1 })

class TriggerAddRemoveNveVniMcastGroup(TriggerAddRemove):
    """Add mcast group under vxlan and then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add mcast group under Vxlan then restore the
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
                   nve_vni: `int`
                   mcast_group: `str`

                   (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                         OR
                         interface: 'Ethernet1/1/1' (Specific value)
       Steps:
           1. Learn Vxlan Ops configured on device. SKIP the trigger if there
              is no vxlan configured on the device.
           2. Save the current device configurations using "method" specified.
           3. Add mcast group that using Genie Interface Conf.
           4. Verify the newly mcast group under Vxlan is reflected in
              device configuration.
           5. Restore the device configuration to the original configuration saved
              in step 2.
           6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan':{
                                          'requirements':[['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',\
                                                           'mcast', '(?P<mcast>unconfigured.*)'],
                                                          ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',
                                                            'vni_state', 'down'],
                                                          ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', \
                                                           'associated_vrf', False ],
                                                          ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni_others>.*)', \
                                                           'mcast', '(?P<mcast_group>(?!unconfigured|n/a).*)$']],
                                          'kwargs':{'attributes':['nve[(.*)][vni][(.*)]']},
                                          'all_keys': True,
                                          'exclude': vxlan_exclude}},
                    config_info={'conf.interface.Interface': {
                                        'requirements': [['nve_vni', '(?P<nve_vni>.*)'],
                                                         ['nve_vni_mcast_group', '(?P<mcast_group>.*)'],
                                                         ['nve_vni_associate_vrf', False]],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                        'requirements':[['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',\
                                                         'mcast', '(?P<mcast_group>.*)'],
                                                        ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',
                                                        'vni_state', 'up']],
                                        'kwargs':{'attributes':['nve[(.*)][vni][(.*)]']},
                                        'exclude': vxlan_exclude}},
                      num_values={'nve_name': 1, 'nve_vni': 1, 'nve_vni_others': 1,\
                                  'mcast': 1, 'mcast_group': 1})

class TriggerAddRemoveNveVniMultisiteIngressReplication(TriggerAddRemove):
    """Add multisite ingress replication under vxlan and then restore the
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
                       nve_vni: `int`

                       (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                             OR
                             interface: 'Ethernet1/1/1' (Specific value)

           Steps:
               1. Learn Vxlan Ops configured on device. SKIP the trigger if there
                  is no vxlan configured on the device.
               2. Save the current device configurations using "method" specified.
               3. Add multisite ingress replication that using Genie Interface Conf.
               4. Verify the newly multisite ingress replication under Vxlan is reflected in
                  device configuration.
               5. Restore the device configuration to the original configuration saved
                  in step 2.
               6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1.
                   """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',\
                                                          NotExists('multisite_ingress_replication')],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'associated_vrf', False]],
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]']},
                                        'all_keys': True,
                                        'exclude': vxlan_exclude}},
                        config_info={'conf.interface.Interface': {
                                        'requirements': [['nve_vni', '(?P<nve_vni>.*)'],
                                                         ['nve_vni_multisite_ingress_replication', True],
                                                         ['nve_vni_associate_vrf', False]],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)',\
                                                          'multisite_ingress_replication', True]],
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]']},
                                        'exclude': vxlan_exclude}},
                        num_values={'nve_name': 1, 'nve_vni':1 })

class TriggerAddRemoveNveMultisiteBgwInterface(TriggerAddRemove):
    """Add multisite bgw interface under vxlan and then restore the
       configuration by reapplying the whole running configuration"""

    __description__ = """Add Add multisite bgw interface under Vxlan then restore the
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
                          source_if: `str`

                          (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                                OR
                                interface: 'Ethernet1/1/1' (Specific value)

              Steps:
                  1. Learn Vxlan Ops configured on device. SKIP the trigger if there
                     is no Vxlan configured on the device.
                  2. Save the current device configurations using "method" specified.
                  3. Add multisite bgw interface that using Genie Interface Conf.
                  4. Verify the newly multisite bgw interface under Vxlan is reflected in
                     device configuration.
                  5. Restore the device configuration to the original configuration saved
                     in step 2.
                  6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1.
              """

    # configuration steps callable
    # adding new value for multisite bgw interface
    def configure_multisite_bgw_interface(self, conf_obj, unconfig, **kwargs):
        ret = ""
        for key in self.keys:
            if key['source_if'] != key['intf_name']:
                ret = key['intf_name']

        self.keys[0]['multisite_bgw_intf'] = ret
        conf_obj.nve_multisite_bgw_intf = ret
        if not unconfig:
            conf_obj.build_config()
        else:
            conf_obj.build_unconfig(apply=True ,attributes={'nve_multisite_bgw_intf':ret})

        @aetest.test
        def verify_configuration(self, uut, abstract, steps):
            # modify self.keys to modify the multisite bgw interface value
            for item in self.mapping.keys:
                try:
                    ret = item['multisite_bgw_intf']
                    req = ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if']
                    req.insert(len(req), ret)
                    self.mapping._verify_ops_dict['ops.vxlan.vxlan.Vxlan']['requirements'].append(req)
                    log.info("\n\nVerifying the following requirements: {req}".format(req=req))
                except Exception as e:
                    self.failed('Failed to verify the '
                                'added feature', from_exception=e)

            super().verify_configuration(uut, abstract, steps)


    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan':{
                                            'requirements': [[['nve', '(?P<nve_name>.*)', 'source_if', '(?P<source_if>.*)']],
                                                             [['nve', '(?P<nve_name>.*)', NotExists('multisite_bgw_if')]]],
                                            'all_keys': True,
                                            'kwargs': {'attributes': ['nve']},
                                            'exclude': vxlan_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements': [['info', '(?P<intf_name>loopback.*)', 'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info']},
                                            'exclude': interface_exclude}},
                        config_info={'conf.interface.Interface': {
                                            'requirements': [[partial(configure_multisite_bgw_interface,\
                                                                      nve_multisite_bgw_intf='(?P<source_if>.*)')]],
                                            'verify_conf': False,
                                            'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                            'requirements': [],
                                            'kwargs': {'attributes': ['nve']},
                                            'exclude': vxlan_exclude}},
                        num_values={'nve_name':'all', 'source_if': 'all', 'intf_name':'all'})
