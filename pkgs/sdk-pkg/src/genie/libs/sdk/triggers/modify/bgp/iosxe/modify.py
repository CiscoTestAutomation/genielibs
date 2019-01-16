'''IOSXE Implementation for bgp modify triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'last_reset',
               'keepalives', 'total', 'total_bytes', 'up_time',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'route_reflector_client', 'capability',
               'distance_internal_as', 'bgp_neighbor_counters', 'memory_usage',
               'total_entries', 'routing_table_version', 'total_memory',
               'path', 'prefixes', 'cluster_id']


class TriggerModifyBgpNeighborAsn(TriggerModify):
    """Modify the neighbor remote_as configured under BGP and then restore the
      configuration by reapplying the whole running configuration"""

    __description__ = """Modify the neighbor remote_as configured under BGP and then restore the
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

                  instance: `str`
                  vrf: `str`
                  neighbor: `str`
                  remote_as: `int`
                  bgp_id: `int`

                  (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                        OR
                        interface: 'Ethernet1/1/1' (Specific value)
      Steps:
          1. Learn BGP Ops configured on device. SKIP the trigger if there
             is no BGP configured on the device.
          2. Save the current device configurations using "method" specified.
          3. Modify the remote-as learned in step 1 using Genie BGP Conf.
          4. Verify the change to remote_as config under BGP is
             reflected in device configuration.
          5. Restore the device configuration to the original configuration saved
             in step 2.
          6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
      """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'remote_as',
                                                           '(?P<remote_as>.*)'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                           'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                          'all_keys':True,
                                          'kwargs':{'attributes':['info']},
                                          'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                   'neighbor_attr','(?P<neighbor>.*)', 'nbr_remote_as',
                                                    88]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'remote_as', 88],
                                                  ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor',
                                                   '(?P<neighbor>.*)', 'session_state', 'idle']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1})


class TriggerModifyBgpNeighborCluster(TriggerModify):
    """Modify the cluster id configured under BGP and then restore the
      configuration by reapplying the whole running configuration"""

    __description__ = """Modify the cluster id configured under BGP and then restore the
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

                  instance: `str`
                  cluster_id: `str`
                  bgp_id: `int`

                  (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                        OR
                        interface: 'Ethernet1/1/1' (Specific value)
      Steps:
          1. Learn BGP Ops configured on device. SKIP the trigger if there
             is no BGP configured on the device.
          2. Save the current device configurations using "method" specified.
          3. Modify the cluster id learned in step 1 using Genie BGP Conf.
          4. Verify the change to cluster id config under BGP is
             reflected in device configuration.
          5. Restore the device configuration to the original configuration saved
             in step 2.
          6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)',
                                             'vrf', 'default', 'cluster_id', '(?P<cluster_id>.*)'],
                                                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                                    'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', 'default',
                                                 'cluster_id', '1.0.0.1']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                     'default', 'cluster_id', '1.0.0.1']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'instance':1, 'neighbor':1, 'address_family':1})


class TriggerModifyBgpNeighborRoutemapIn(TriggerModify):
    """Modify the neighbor inbound route map configured under BGP and then restore the
          configuration by reapplying the whole running configuration"""

    __description__ = """Modify the neighbor inbound route map configured under BGP and then restore the
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

                  instance: `str`
                  vrf: `vrf`
                  neighbor: `str`
                  address_family: `str`
                  route_map: `str`
                  bgp_id: `int`

                  (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                        OR
                        interface: 'Ethernet1/1/1' (Specific value)
      Steps:
          1. Learn BGP Ops configured on device. SKIP the trigger if there
             is no BGP configured on the device.
          2. Save the current device configurations using "method" specified.
          3. Modify the inbound route map learned in step 1 using Genie BGP Conf.
          4. Verify the change to inbound route map config under BGP is
             reflected in device configuration.
          5. Restore the device configuration to the original configuration saved
             in step 2.
          6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    # Create a name for router map in
    new_name = 'bgp_' + time.ctime().replace(' ', '_').replace(':', '_')

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                          '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>(?!:).*)',
                                                          'address_family', '(?P<address_family>.*)',
                                                          'route_map_name_in', '(?P<route_map>.*)'],
                                                         ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_in',
                                                    new_name]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_in', new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})


class TriggerModifyBgpNeighborRoutemapOut(TriggerModify):
    """Modify the neighbor outbound route map configured under BGP and then restore the
          configuration by reapplying the whole running configuration"""

    __description__ = """Modify the neighbor outbound route map configured under BGP and then restore the
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

                      instance: `str`
                      vrf: `vrf`
                      neighbor: `str`
                      address_family: `str`
                      route_map: `str`
                      bgp_id: `int`

                      (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                            OR
                            interface: 'Ethernet1/1/1' (Specific value)
          Steps:
              1. Learn BGP Ops configured on device. SKIP the trigger if there
                 is no BGP configured on the device.
              2. Save the current device configurations using "method" specified.
              3. Modify the outbound route map learned out step 1 using Genie BGP Conf.
              4. Verify the change to outbound route map config under BGP is
                 reflected in device configuration.
              5. Restore the device configuration to the original configuration saved
                 in step 2.
              6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
        """

    # Create a name for router map in
    new_name = 'bgp_' + time.ctime().replace(' ', '_').replace(':', '_')

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                         '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                         'address_family', '(?P<address_family>.*)',
                                                         'route_map_name_out', '(?P<route_map>.*)'],
                                                         ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_out',
                                                    new_name]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_out', new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})
